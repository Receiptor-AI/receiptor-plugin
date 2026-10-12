# Receiptor Claude Code, Codex, and Cursor Plugin

[![smithery badge](https://smithery.ai/badge/receiptor-ai/receiptor-mcp)](https://smithery.ai/servers/receiptor-ai/receiptor-mcp)

Shared plugin package for Receiptor bookkeeping workflows in Claude Code, Codex, and Cursor.

Source repository: https://github.com/Receiptor-AI/receiptor-plugin

Test locally in Claude Code with:

```bash
claude --plugin-dir .
```

Install in Codex with:

```bash
codex plugin marketplace add Receiptor-AI/receiptor-plugin
```

## Included

- `.claude-plugin/plugin.json`: Claude Code plugin manifest
- `.codex-plugin/plugin.json`: Codex plugin manifest
- `.cursor-plugin/plugin.json`: Cursor plugin manifest
- `.agents/plugins/marketplace.json`: standalone Codex marketplace for installs from this public plugin
- `mcp.json`: Receiptor MCP server config for `https://mcp.receiptor.ai`
- `rules/receiptor-workflows.mdc`: default operating rules for approval-aware bookkeeping work
- `references/workspace-checks.md`: shared task-specific workspace checks, read by every bundled skill
- `skills/document-review/`: search and inspect receipts and invoices
- `skills/categorization-review/`: preview and approve bulk categorization changes
- `skills/document-analysis/`: analyze document counts, recorded totals, and grouped breakdowns
- `skills/month-end-document-pack/`: prepare a draft accountant-review workbook, available originals, file manifest and handoff note

The month-end skill is prepared for private testing. Its complete review workflow requires the backend release with filter-only pagination, canonical review filtering/detail, null-date filters and `documents_respond_review`. Check the connected server's schemas before testing; these source changes do not themselves deploy MCP. Pack preparation is read-only by default. Test the installed plugin on two representative periods before public promotion.

## Design

This plugin is intentionally MCP-first and shares the same MCP + skill layer across supported hosts.

- Live operational data should come from Receiptor MCP tools, not hardcoded assumptions.
- Mutations should preview first and follow Receiptor approval flow when execution requires it.
- Skills are adapted from the Receiptor CLI workflow for agent-driven MCP usage.
- Every bundled skill checks workspace access and the prerequisites relevant to its task. Existing MCP tools, including `workspace_get_context`, `context_readiness`, `sources_email_list` and `integrations_list`, remain available without a standalone readiness skill. Other MCP clients can use these tools too; plugin instructions must be separately made available in hosts that do not load this bundle.

## MCP

The bundled MCP config is:

```json
{
  "mcpServers": {
    "receiptor": {
      "type": "http",
      "url": "https://mcp.receiptor.ai"
    }
  }
}
```

After installing the plugin in Codex or Cursor, complete OAuth for the Receiptor MCP server and select the workspace you want to authorize.
Use `workspace_get_context` to confirm the active workspace and `workspace_switch` if you need to change it later in the same MCP session.

## Support and policy links

- MCP docs: https://docs.receiptor.ai/api/mcp/introduction
- CLI docs: https://docs.receiptor.ai/api/cli/introduction
- Privacy: https://receiptor.ai/privacy
- Help center: https://help.receiptor.ai
- Contact: info@receiptor.ai
