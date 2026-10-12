---
name: spend-analysis
description: Analyze spending totals, grouped breakdowns, and financial patterns using Receiptor MCP. Use this skill whenever the user asks about totals, category summaries, merchant breakdowns, or reporting-oriented spend analysis that should use full aggregate data instead of ad hoc document sampling.
---

# Spend Analysis

Use `documents_count` for aggregate reporting.

## Core MCP Flow

1. Call `documents_count` with the narrowest possible filter set.
2. Add `groupBy` when the user wants a breakdown by merchant, category, date, or another supported field.
3. If the result suggests an anomaly, drill into the underlying documents with `documents_search`.

## Good Uses

- document counts and recorded totals across all matching documents
- grouped document totals by merchant or category
- date-bounded document analysis for a reporting period
- focused analysis for one merchant, category, or document type

## Reporting Guidance

- Use typed `where.conditions` for date/entity/document filters. Use aggregate counts to check the full population; do not extrapolate a search sample.
- Totals count documents, including both sides of linked invoice/receipt pairs. Establish a defensible purchase population before describing totals as spending or expenses.
- State the grouping field you used.
- `documents_count` totals may be converted to the authenticated user's currency even when grouped by original currency. Preserve the returned currency label. For native-currency totals, paginate the complete register and calculate separately by currency with code; never add currencies.
- If a grouped result needs investigation, follow up with `documents_search` rather than speculating about what is inside the group.
