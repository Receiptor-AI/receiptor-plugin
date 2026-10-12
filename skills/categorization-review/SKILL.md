---
name: categorization-review
description: Review and fix categorization quality across receipts and invoices using Receiptor MCP. Use this skill when the user wants to recategorize expenses, normalize merchant names, apply category fixes in bulk, or clean up classification issues across multiple documents.
---

# Categorization Review

Use `documents_bulk_edit` for controlled bulk cleanup.

For existing categorization questions, first use `context_requests_list` (paginate the queue) or `context_requests_group` (a returned subset), then `context_requests_resolve` or `context_requests_bulk_resolve` for selected requests. Submit explicit user context, distinguish proposals from confirmed decisions, and follow the same authorization and approval rules as other mutations. `provide_context` may queue recategorization; re-read the document before reporting success. Save lasting guidance with `saveAsMemory` or `memories_save` only when authorized, and do not turn one document's explanation into a workspace-wide rule.

## Required Workflow

1. Preview first with `documents_bulk_edit` in dry-run mode.
2. Review the preview payload with the user:
   - total matching documents
   - sample affected documents
   - proposed changes
   - available merchants and categories when provided
3. Only execute with `dryRun: false` after explicit user confirmation.
4. If execution returns `approval_required`, resolve it with `approvals_get` and then `approvals_approve` or `approvals_reject`.

## Good Uses

- fix a misspelled merchant across many documents
- recategorize one merchant or query result set
- normalize category usage before reporting or close

## Safety Rules

- Never skip preview for bulk edits.
- Never assume the preview and execute scopes are identical if you changed filters between calls.
- When reporting the outcome, include matched count, modified count, and the exact change set that was applied.
