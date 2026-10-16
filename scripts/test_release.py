"""Regression coverage for release identity, isolation and publication guards."""

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        self.root.mkdir()
        for name in (*release.COMMON_FILES, "CHANGELOG.md", "mcp.json", *release.MANIFESTS.values()):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(release.ROOT / name, path)
        for name in (*release.COMMON_DIRS, "rules"):
            shutil.copytree(release.ROOT / name, self.root / name)
        self.output = Path(self.temp.name) / "output"
        self.version = (self.root / "VERSION").read_text().strip()

    def mock_git(self, root, *args):
        if args[0] == "status":
            return ""
        return "a" * 40

    def test_version_drift_fails_and_sync_preserves_metadata(self):
        path = self.root / release.MANIFESTS["codex"]
        manifest = release.read_json(path)
        manifest["version"] = "0.0.1"
        manifest["extensions"]["com.openai"]["review"]["demo_recording_url"] = "https://example.com/demo"
        path.write_bytes(release.json_bytes(manifest))
        with self.assertRaisesRegex(ValueError, "differs"):
            release.check(self.root)
        release.sync(self.root)
        self.assertEqual(release.check(self.root), self.version)
        self.assertEqual(release.read_json(path)["extensions"], manifest["extensions"])

    def test_invalid_manifest_does_not_partially_sync(self):
        before = (self.root / release.MANIFESTS["claude"]).read_bytes()
        (self.root / release.MANIFESTS["cursor"]).write_text("invalid JSON")
        with self.assertRaises(ValueError):
            release.sync(self.root, "99.0.0")
        self.assertEqual((self.root / release.MANIFESTS["claude"]).read_bytes(), before)

    def test_release_requires_clean_source_and_matching_tag(self):
        def dirty(root, *args):
            return " M skills/document-review/SKILL.md" if args[0] == "status" else "a" * 40
        with patch.object(release, "git", side_effect=dirty):
            with self.assertRaisesRegex(ValueError, "clean checkout"):
                release.build(self.root, self.output)
        def wrong_tag(root, *args):
            if args[0] == "status":
                return ""
            return ("b" if "refs/tags/" in args[1] else "a") * 40
        with patch.object(release, "git", side_effect=wrong_tag):
            with self.assertRaisesRegex(ValueError, "tag"):
                release.build(self.root, self.output)
        self.assertFalse(self.output.exists())

    def test_host_archives_share_skills_and_isolate_configuration(self):
        (self.root / ".env").write_text("SECRET=never-package")
        (self.root / ".app.json").write_text("private binding")
        with patch.object(release, "git", side_effect=self.mock_git):
            release.build(self.root, self.output)
            first = (self.output / "receiptor-openai.zip").read_bytes()
            release.build(self.root, self.output)
            self.assertEqual((self.output / "receiptor-openai.zip").read_bytes(), first)
        skills = []
        for host in ("claude", "openai", "cursor"):
            with zipfile.ZipFile(self.output / f"receiptor-{host}.zip") as archive:
                self.assertIsNone(archive.testzip())
                names = archive.namelist()
                self.assertFalse(any(name.endswith((".env", ".app.json", ".py")) for name in names))
                manifest_path = "plugin.json" if host == "openai" else release.MANIFESTS[host]
                manifest = json.loads(archive.read("receiptor/" + manifest_path))
                self.assertEqual(manifest["version"], self.version)
                info = json.loads(archive.read("receiptor/references/release-info.json"))
                self.assertEqual(info["sourceCommit"], "a" * 40)
                self.assertEqual(info["buildKind"], "release")
                for other, path in release.MANIFESTS.items():
                    if other != host:
                        self.assertNotIn("receiptor/" + path, names)
                transport = json.loads(archive.read("receiptor/mcp.json"))["mcpServers"]["receiptor"]["type"]
                self.assertEqual(transport, "streamable-http" if host == "openai" else "http")
                skills.append({name: archive.read(name) for name in names if name.endswith("SKILL.md")})
        self.assertEqual(len(skills[0]), 4)
        self.assertEqual(skills[0], skills[1])
        self.assertEqual(skills[1], skills[2])

    def test_preview_records_dirty_state_and_has_distinct_name(self):
        with patch.object(release, "git", side_effect=lambda root, *args: "dirty" if args[0] == "status" else "a" * 40):
            info = release.build(self.root, self.output, preview=True)
        self.assertTrue(info["sourceDirty"])
        self.assertTrue((self.output / "receiptor-claude-PREVIEW.zip").exists())
        self.assertFalse((self.output / "receiptor-claude.zip").exists())

    def test_public_app_bindings_are_rejected(self):
        path = self.root / release.MANIFESTS["codex"]
        manifest = release.read_json(path)
        manifest["extensions"]["com.openai"]["apps"] = "./.app.json"
        path.write_bytes(release.json_bytes(manifest))
        with patch.object(release, "git", side_effect=self.mock_git):
            with self.assertRaisesRegex(ValueError, "app bindings"):
                release.build(self.root, self.output, preview=True)
        self.assertFalse(self.output.exists())

    def test_same_version_with_shipped_changes_is_rejected(self):
        def base(root, *args):
            if args[0] == "ls-tree":
                return "VERSION"
            if args[0] == "show":
                return self.version
            return "skills/document-review/SKILL.md"
        with patch.object(release, "git", side_effect=base):
            with self.assertRaisesRegex(ValueError, "without a version bump"):
                release.check(self.root, "base")

    def test_preview_cannot_be_mixed_with_release_archives(self):
        with patch.object(release, "git", side_effect=self.mock_git):
            release.build(self.root, self.output)
            with self.assertRaisesRegex(ValueError, "separate output directory"):
                release.build(self.root, self.output, preview=True)

    def test_invalid_versions_and_downgrades_are_rejected(self):
        for version in ("01.1.1", "0.1", "0.1.1-dev", "0.0.1"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                release.sync(self.root, version)


if __name__ == "__main__":
    unittest.main()
