# Workspace checks

Use these checks before a Receiptor task, or when the user asks whether a workspace is ready for that task. They use existing MCP tools and apply across hosts. Read the connected server's schemas; do not assume a tool or argument is available because it appears in these instructions.

## Access and scope

- Call `workspace_get_context` to confirm authentication, the active workspace and role. Reuse a successful check within the same task/session unless the workspace changes or an authorization error occurs.
- If disconnected or unauthorized, explain how to connect Receiptor MCP and complete OAuth in the current host. If no workspace is selected or it differs from the user's requested workspace, use `workspaces_list` and `workspace_switch`, then confirm the context. Ask only if the intended workspace is ambiguous.
- Confirm the document, period and own-business/entity scope needed by the task. Workspace access does not establish write permission; honor tool permission failures and approval requirements. Readiness checks do not authorize setup changes or document edits.

## Check what the task needs

- **Document review:** verify the search/detail tools required for the requested inspection. An empty search is a result, not proof of broken setup or a missing receipt.
- **Document analysis:** verify aggregate tools and, when calculating native-currency totals or establishing the full population, supported filter-only search and pagination. Missing aggregation/pagination can limit the report; do not extrapolate from a sample.
- **Categorization review:** use `context_readiness` for the existing business-profile, location/tax, chart-of-accounts and entity readiness assessment. Use its missing fields and actions as evidence. Its score measures context completeness, not document correctness, permission or accounting-close readiness. Inspect relevant saved guidance with `memories_recall`; use `rules_list` when automation policy matters. Missing context can require a question before a proposed classification, but does not prevent inspecting documents or applying an explicitly specified, supported correction. Do not invent business or tax facts to fill gaps.
- **Month-end document pack:** check document/review tools and host file-generation/download support as described in that skill. If interpreting or changing categorization, also check `context_readiness`. Missing file support limits deliverables; missing write actions do not prevent read-only preparation.
- **Collection coverage:** when the task concerns inbox monitoring, capture coverage or a period pack, call `sources_email_list` with `includeInactive: true` so disconnected sources are visible. Current status does not establish historical coverage. Disabled monitoring is a collection risk, not a reason to block analysis of captured records; uploads or other sources may still work.
- **Accounting exports:** only when the requested task depends on an accounting destination, inspect `integrations_list` with `category: "accounting"` and relevant `exports_list`/`exports_get` records. Existing documents and draft packs do not require an accounting integration, automation rules or previous exports. Export history does not prove current successful posting.

## Report the result

State whether the requested task can proceed, any concrete blocker or coverage limitation, and the next step if needed. When evidence is unavailable, report it as unknown rather than ready. Continue supported work with disclosed limitations; stop only the part that depends on a missing prerequisite. Do not run every diagnostic for every task or require a globally "complete" workspace.
