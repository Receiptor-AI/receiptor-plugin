"""Keep host versions aligned and build isolated, traceable plugin archives.

Release builds require a clean tagged checkout. Preview builds disclose dirty
source and never use the stable download filenames. No third-party packages.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = {
    host: f".{host}-plugin/plugin.json" for host in ("claude", "codex", "cursor")
}
COMMON_FILES = ("README.md", "LICENSE", "VERSION")
COMMON_DIRS = ("skills", "references", "assets")
SHIPPED_PATHS = (*COMMON_FILES, *COMMON_DIRS, "rules", "mcp.json", *MANIFESTS.values())


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def read_json(path):
    return json.loads(path.read_text())


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode()


def version_parts(version):
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version):
        raise ValueError("Use a stable semantic version such as 0.1.1")
    return tuple(map(int, version.split(".")))


def source_info(version):
    return {"version": version, "sourceCommit": None, "sourceDirty": None, "buildKind": "source"}


def release_notes(root, version):
    changelog = (root / "CHANGELOG.md").read_text()
    match = re.search(rf"^## {re.escape(version)}\n(.*?)(?=^## |\Z)", changelog, re.MULTILINE | re.DOTALL)
    if not match or not match[1].strip():
        raise ValueError(f"Add release notes for {version} to CHANGELOG.md")
    return match[1].strip()


def sync(root, version=None):
    previous = (root / "VERSION").read_text().strip()
    version = previous if version is None else version
    if version_parts(version) < version_parts(previous):
        raise ValueError("Release versions cannot go backwards")
    # Read every manifest before writing, so malformed inputs fail without a partial sync.
    manifests = {path: read_json(root / path) for path in MANIFESTS.values()}
    notes = release_notes(root, version)
    manifests[MANIFESTS["codex"]]["extensions"]["com.openai"]["publication"]["release_notes"] = notes
    for path, manifest in manifests.items():
        manifest["version"] = version
        (root / path).write_bytes(json_bytes(manifest))
    (root / "VERSION").write_text(version + "\n")
    (root / "references/release-info.json").write_bytes(json_bytes(source_info(version)))


def check(root, base_ref=None):
    version = (root / "VERSION").read_text().strip()
    version_parts(version)
    for path in MANIFESTS.values():
        manifest = read_json(root / path)
        if manifest.get("name") != "receiptor" or manifest.get("version") != version:
            raise ValueError(f"{path}: identity/version differs from VERSION; run sync")
    if read_json(root / "references/release-info.json") != source_info(version):
        raise ValueError("Source release-info.json is stale; run sync")
    publication = read_json(root / MANIFESTS["codex"])["extensions"]["com.openai"]["publication"]
    if publication.get("release_notes") != release_notes(root, version):
        raise ValueError("OpenAI release notes differ from CHANGELOG.md; run sync")
    if base_ref:
        base_files = git(root, "ls-tree", "--name-only", base_ref).splitlines()
        base_path = "VERSION" if "VERSION" in base_files else MANIFESTS["claude"]
        raw = git(root, "show", f"{base_ref}:{base_path}")
        previous = raw if base_path == "VERSION" else json.loads(raw)["version"]
        if version_parts(version) < version_parts(previous):
            raise ValueError("Release versions cannot go backwards")
        changed = git(root, "diff", "--name-only", base_ref, "HEAD", "--", *SHIPPED_PATHS)
        if changed and version_parts(version) <= version_parts(previous):
            raise ValueError("Shipped plugin files changed without a version bump")
    return version


def common_files(root):
    files = {name: (root / name).read_bytes() for name in COMMON_FILES}
    for directory in COMMON_DIRS:
        for path in sorted((root / directory).rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Do not package symlinks: {path}")
            if path.is_file():
                if any(part.startswith(".") for part in path.relative_to(root).parts):
                    raise ValueError(f"Unexpected hidden resource: {path}")
                files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def package_files(root, host, info):
    files = common_files(root)
    files["references/release-info.json"] = json_bytes(info)
    mcp = read_json(root / "mcp.json")
    if host == "openai":
        source = read_json(root / MANIFESTS["codex"])
        if "apps" in source or "hooks" in source:
            raise ValueError("Public OpenAI packages cannot contain app bindings or hooks")
        fields = ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")
        manifest = {key: copy.deepcopy(source[key]) for key in fields if key in source}
        extension = copy.deepcopy(source.get("extensions", {}).get("com.openai", {}))
        extension["interface"] = copy.deepcopy(source["interface"])
        if "apps" in extension or "hooks" in extension:
            raise ValueError("Public OpenAI packages cannot contain app bindings or hooks")
        manifest["$schema"] = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
        manifest["extensions"] = {"com.openai": extension}
        files["plugin.json"] = json_bytes(manifest)
        mcp["$schema"] = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
        for server in mcp["mcpServers"].values():
            if server.get("type") != "http" or not server.get("url", "").startswith("https://"):
                raise ValueError("Expected a remote HTTPS MCP server")
            server["type"] = "streamable-http"
    else:
        path = MANIFESTS[host]
        files[path] = (root / path).read_bytes()
        if host == "cursor":
            for path in sorted((root / "rules").rglob("*.mdc")):
                if path.is_symlink():
                    raise ValueError(f"Do not package symlinks: {path}")
                files[path.relative_to(root).as_posix()] = path.read_bytes()
    files["mcp.json"] = json_bytes(mcp)
    return files


def build(root, output, preview=False):
    version = check(root)
    output = output.resolve()
    if output == root.resolve() or output in root.resolve().parents:
        raise ValueError("Build output cannot replace the source directory")
    if output.is_relative_to(root.resolve()) and output.relative_to(root.resolve()).parts[0] != "dist":
        raise ValueError("Build inside dist/ or outside the source tree")
    commit = git(root, "rev-parse", "HEAD")
    dirty = bool(git(root, "status", "--porcelain", "--untracked-files=all"))
    if not preview:
        if dirty:
            raise ValueError("Release builds require a clean checkout; use --preview for local testing")
        tag_commit = git(root, "rev-parse", f"refs/tags/v{version}^{{commit}}")
        if tag_commit != commit:
            raise ValueError(f"Release builds require tag v{version} at HEAD")
    info = {"version": version, "sourceCommit": commit, "sourceDirty": dirty,
            "buildKind": "preview" if preview else "release"}
    existing_info = output / "release-info.json"
    if existing_info.exists():
        previous = read_json(existing_info)
        if any(previous.get(key) != info[key] for key in ("version", "buildKind")):
            raise ValueError("Use a separate output directory for each version and preview/release kind")
    # Prepare everything before creating output; fail without publishing a partial bundle.
    packages = {host: package_files(root, host, info) for host in ("claude", "openai", "cursor")}
    expected_archives = {
        f"receiptor-{host}-PREVIEW.zip" if preview else f"receiptor-{host}.zip" for host in packages
    }
    if any(path.name not in expected_archives for path in output.glob("*.zip")):
        raise ValueError("Output contains archives from another build; choose a separate directory")
    output.mkdir(parents=True, exist_ok=True)
    inventory = {}
    for host, files in packages.items():
        name = f"receiptor-{host}-PREVIEW.zip" if preview else f"receiptor-{host}.zip"
        archive = output / name
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for path, content in sorted(files.items()):
                entry = zipfile.ZipInfo(f"receiptor/{path}", date_time=(2020, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = 0o100644 << 16
                bundle.writestr(entry, content)
        inventory[name] = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "release-info.json").write_bytes(json_bytes({**info, "archives": inventory}))
    (output / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in inventory.items()))
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sync_args = sub.add_parser("sync")
    sync_args.add_argument("version", nargs="?")
    check_args = sub.add_parser("check")
    check_args.add_argument("--base-ref")
    build_args = sub.add_parser("build")
    build_args.add_argument("--preview", action="store_true")
    build_args.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    try:
        if args.command == "sync":
            sync(ROOT, args.version)
            print(f"Synced {check(ROOT)}")
        elif args.command == "check":
            print(f"Versions aligned: {check(ROOT, args.base_ref)}")
        else:
            print(json.dumps(build(ROOT, args.output, args.preview), indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Release check failed: {error}\n")


if __name__ == "__main__":
    main()
