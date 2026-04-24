---
name: setup-readiness
description: Review whether a Receiptor workspace is actually ready for bookkeeping work through Receiptor MCP. Use this skill whenever the user wants to confirm OAuth and workspace context, inspect connected integrations, verify monitored intake sources, review automation and export readiness, or identify setup gaps before intake, close, or tax-prep work.
---

# Setup Readiness

Use this skill before operational bookkeeping work when the question is "is this workspace ready?" rather than "where is this document?"

## Core MCP Flow

1. Call `workspace_get_context` to confirm the authorized workspace.
2. If the workspace is wrong or missing, use `workspaces_list` and then `workspace_switch` to move the current MCP session to the target workspace.
3. Call `integrations_list` with `category: "email"` to review intake sources.
4. Call `integrations_list` with `category: "accounting"` to review downstream export targets.
5. Call `rules_list` to see whether automation rules exist.
6. Call `exports_list` to understand whether export activity has happened at all.

## What To Confirm

- OAuth completed and a workspace is actually authorized
- email integrations exist
- monitored intake sources are present and active enough for automatic collection
- accounting integrations exist if downstream export is expected
- automation rules exist where cleanup or routing is expected
- export history exists if the user expects downstream sync

## Interpretation

- If `workspace_get_context` fails or returns the wrong workspace, fix authorization first.
- If `integrations_list` for email returns nothing useful, the workspace is not ready for automatic intake.
- If accounting integrations are absent, intake may still work, but downstream export workflows are not ready.
- If rules and exports are both empty, the workspace may still be at an early setup stage even if sources are connected.

## Limits

This skill is good for operational readiness, not every product-level configuration detail.

If the user asks about state that is not surfaced through MCP yet, say so explicitly and avoid guessing.
