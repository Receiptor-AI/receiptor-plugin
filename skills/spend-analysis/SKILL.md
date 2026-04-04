---
name: spend-analysis
description: Analyze spending totals, grouped breakdowns, and financial patterns using Receiptor MCP in Cursor. Use this skill whenever the user asks about totals, category summaries, merchant breakdowns, or reporting-oriented spend analysis that should use full aggregate data instead of ad hoc document sampling.
---

# Spend Analysis

Use `documents_count` for aggregate reporting.

## Core MCP Flow

1. Call `documents_count` with the narrowest possible filter set.
2. Add `groupBy` when the user wants a breakdown by merchant, category, date, or another supported field.
3. If the result suggests an anomaly, drill into the underlying documents with `documents_search`.

## Good Uses

- total spend across all matching documents
- grouped spend by merchant
- grouped spend by category
- date-bounded spend analysis for a reporting period
- focused analysis for one merchant, category, or document type

## Reporting Guidance

- Prefer aggregate outputs from `documents_count` over hand-built math from search results.
- State the grouping field you used.
- Call out currency handling when totals may reflect preferred-currency conversion.
- If a grouped result needs investigation, follow up with `documents_search` rather than speculating about what is inside the group.
