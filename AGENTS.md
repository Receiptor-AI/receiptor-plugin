# receiptor-plugin agent guide

## Engineering principles

Apply these principles to implementation and review. Follow the repository-specific architecture and validation instructions below.

- **KISS and YAGNI:** Choose the simplest design that meets the current requirement. Reuse existing libraries and components; avoid speculative abstractions, configuration and dependencies.
- **DRY with clear ownership:** Keep each business rule in its owning module and reuse it across callers. Extract genuine shared logic; do not couple unrelated behavior just because it looks similar.
- **Durable fixes:** Fix the root cause. Preserve domain invariants, tenant boundaries, financial accuracy and public contracts. Prefer a deliberate migration over permanent compatibility patches; remove obsolete paths when safe.
- **Readable boundaries:** Use descriptive names, small cohesive units and explicit dependencies. Validate untrusted inputs at boundaries; keep business decisions out of transport and presentation layers. Explain non-obvious rules and tradeoffs in comments.
- **TDD for behavior changes:** For new behavior and bug fixes, first write the smallest meaningful failing test, confirm it fails for the intended reason, implement the change, then refactor with tests passing. Test observable behavior and important failure cases, not implementation shape or mocks alone. For behavior-preserving refactors, use existing regression coverage. Documentation and cosmetic-only changes need appropriate artifact checks, not artificial unit tests. If the failing-test step cannot be run, explain the limitation and the alternative validation used.
- **Reliable execution:** Make failures visible; do not turn errors into empty or successful results. Bound expensive work and use pagination, timeouts, resource cleanup and idempotent retries where relevant. Verify performance with representative data before claiming scalability.
- **Focused verification:** Run the affected tests and relevant lint/type/build or render checks. Expand scope for shared contracts or cross-cutting changes; do not default to the full suite. Report actual results, existing failures and unverified paths.
- **Review before handoff:** Recheck duplication, unnecessary complexity, compatibility and edge cases. Remove temporary code. State remaining risks precisely; do not claim durability or production readiness beyond the evidence.

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
