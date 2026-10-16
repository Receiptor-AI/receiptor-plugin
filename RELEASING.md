# Release the plugin

Tracking: TECH-1006. The plugin repository owns this process, independently of the monorepo. Python 3.10+ and Git are required; no Python packages are needed.

## Prepare one shared version

`VERSION` is the version source. From the plugin repository:

```sh
python3 scripts/release.py sync 0.1.1
python3 scripts/release.py check
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/release.py build --preview
```

For subsequent releases, choose a greater stable semantic version and add its entry to CHANGELOG.md. Use patch releases for fixes/instruction refinements, minor releases for new workflows, and major releases for breaking contracts. Sync updates all three host versions, the source release reference and OpenAI release notes from that changelog entry. Package names, MCP endpoints and other review/publication metadata are preserved.

Preview filenames contain PREVIEW. Their release-info.json records the source commit and whether uncommitted changes were present; a dirty preview is not reproducible from the commit alone. Source installations report an unknown commit unless the host can verify the installed checkout. Do not use the current repository tip as evidence of what an older session loaded.

CI checks matching versions and requires a bump when shipped files differ from the PR base. Maintenance-only build scripts and workflows do not require a plugin version bump. Protect the release check in repository branch settings if it must block merging; adding the workflow does not configure branch protection.

## Publish a source release

The engineer reviews, commits and pushes the plugin changes through the repository's normal process, then creates and pushes tag `v<VERSION>` on the clean release commit. Agents do not perform these Git actions. The tag workflow validates the source, builds all three host archives, and creates a GitHub release with hashes and source metadata. An existing release is not overwritten on rerun.

Stable assets are `receiptor-claude.zip`, `receiptor-openai.zip` and `receiptor-cursor.zip`. Each contains only that host's manifest, shared skills/references/assets and its MCP configuration. OpenAI uses a portable manifest and streamable-http transport; Claude keeps http. Public bundles exclude private app bindings, marketplace manifests, build scripts and release workflows. Existing OpenAI review/publication metadata is copied from the Codex source manifest, including any subsequently supplied demo URL. A built ZIP can still lack review materials; building is not submission approval.

The website uses:

https://github.com/Receiptor-AI/receiptor-plugin/releases/latest/download/receiptor-claude.zip

**Publish the first tagged release before deploying the updated website link.** The URL will not work until that asset exists. It follows future releases automatically. For a pinned historical build, replace `latest/download` with `download/v<VERSION>`.

## Submit and verify each host

Upload the corresponding archive to the existing listing, keeping its identity. Claude/Grok/Cursor Git-based submissions must reference the same release tag/commit where the portal supports it. Recheck the revision actually scanned or installed; a listing following main can move ahead of a release. Marketplace review may lag GitHub releases. Never change a recorded approval/version just because source was bumped.

Record these fields for each release in the tracking issue, with evidence URLs and dates:

| Host | Prepared version + commit | Submitted/scanned version + commit | Approved version | Installed/tested version + commit |
| --- | --- | --- | --- | --- |
| Claude | Record from release-info.json | Record from portal | Unknown until verified | Record from installed package |
| OpenAI | Record from release-info.json | Record from portal | Unknown until verified | Record from installed package |
| Cursor / Grok Bot | Record from release-info.json | Record from portal | Unknown until verified | Record from installed package |

Grok availability is separate from submission eligibility. Keep unverified statuses unknown. The old private OpenAI package numbered 1.0.1 has a separate generated identity; it is not the public release version. Retire that archive for future public submissions. If continuing an existing private plugin with its own version sequence, retain its identity and monotonically increasing package version and record its tested source release/commit separately. Never downgrade it or replace its private app binding to force matching numbers.

## Verify the monthly pack

The workbook Overview and handoff note should identify the installed plugin's version, source commit when available, and preview/dirty state. If the host cannot read that information, record unknown and continue useful preparation. Old January/August/September outputs are not retroactively stamped with a guessed revision.
