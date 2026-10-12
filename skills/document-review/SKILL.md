---
name: document-review
description: Find receipts and invoices in Receiptor AI and check their details. Use when searching by supplier or date, checking amounts, investigating possible duplicates, or checking whether a document was sent to accounting software.
---

# Document review

Use this skill to find and inspect documents already captured by Receiptor.

## Before starting

Read [workspace checks](../../references/workspace-checks.md) and apply the access, scope and document-review checks. Check source health only when collection coverage is relevant.

## Core MCP Flow

1. Call `documents_search` with the user's query and the narrowest practical filters.
2. Use `where.conditions` for typed filters such as `docDate` (`gte`/`lt`), `docType` (`eq`) or merchant (`regex`). Use top-level `exportStatus` for that filter. For a complete register, set `useSearch: false` and paginate with `limit` and `offset`; `totalCount` is the returned page size.
3. For a single document, call `documents_get` or `documents_inspect` using the returned document id.
4. If the user suspects repeated uploads or repeated scans, call `documents_list_duplicates`.
5. For the app's review rules, use `reviewStatus: "needs-review"` in filter-only searches. Read `documents_get.review` for evidence and supported actions. Saved `linkedTo` IDs and proposed relationship repairs are different states.

## Good Search Patterns

- Merchant or vendor lookups
- Date-bounded searches
- Receipt versus invoice filtering
- Export status review
- Full-field inspection for a single candidate document

## Reporting Guidance

When you summarize results, include:

- document id
- merchant
- amount
- date
- category
- export state when relevant

Do not claim a document is missing details until you have inspected it with `documents_get` or `documents_inspect`.
