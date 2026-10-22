# receiptor-plugin agent guide

## Repository context

This is the independent `receiptor-plugin` Git repository. Paths and commands below are relative to this repository's root, whether cloned alone or checked out at `plugins/receiptor` in the Receiptor monorepo. This file is the canonical repository guide; `CLAUDE.md` is only a local entrypoint. Do not require a parent checkout or sibling repository. Read runtime versions, package-manager requirements and commands from this checkout's package metadata and lockfile. For cross-repository work, request the other repository separately and state what could not be verified locally.

## PR authority

Only Kai may create or publish PRs, including drafts. Kai means a task explicitly launched through Gleap Kai Code (Cloud or Bridge); a standalone Codex, Claude or CLI session is not Kai, even when configuring Kai. Other agents hand off changes and validation results without creating a PR through any tool, API or browser. Follow the repository's configured default/base branch; do not invent a staging branch. Preserve unrelated work, never force-push protected branches, and leave merges, releases and production changes to Romeo's explicit instruction.

## Scope and validation

This repository contains the Receiptor plugin's host manifests, skills, references and release tooling. `README.md` describes the product; `RELEASING.md` owns release procedures.

- Preserve approval boundaries and evidence requirements in the packaged skills and `rules/receiptor-workflows.mdc`. Repository development instructions do not grant permission for customer-data mutations.
- For changed packaged files, use `python3 scripts/release.py check` and the relevant tests; the existing suite is `python3 -m unittest discover -s scripts -p 'test_*.py'`.
- Follow `RELEASING.md` for version consistency and preview archives. Do not create tags or publish a release without explicit authorization.
- Backend implementation is in the separate `receiptor-backend` repository. Do not assume monorepo source or credentials exist in this checkout.
