# Receiptor Cursor Plugin

Cursor Marketplace plugin for Receiptor bookkeeping workflows.

## Included

- `mcp.json`: Receiptor MCP server config for `https://mcp.receiptor.ai`
- `rules/receiptor-workflows.mdc`: default operating rules for approval-aware bookkeeping work
- `skills/setup-readiness/`: verify OAuth, workspace context, integrations, rules, and export readiness
- `skills/receipt-intake/`: search and inspect receipts and invoices
- `skills/categorization-review/`: preview and approve bulk categorization changes
- `skills/spend-analysis/`: aggregate spend totals and grouped breakdowns

## Design

This plugin is intentionally MCP-first.

- Live operational data should come from Receiptor MCP tools, not hardcoded assumptions.
- Mutations should preview first and follow Receiptor approval flow when execution requires it.
- Skills are adapted from the Receiptor CLI workflow but rewritten for Cursor MCP usage.

## MCP

The bundled MCP config is:

```json
{
  "mcpServers": {
    "receiptor": {
      "url": "https://mcp.receiptor.ai"
    }
  }
}
```

After installing the plugin in Cursor, complete OAuth for the Receiptor MCP server and select the workspace you want to authorize.
Use `workspace_get_context` to confirm the active workspace and `workspace_switch` if you need to change it later in the same MCP session.

## Support and policy links

- MCP docs: https://docs.receiptor.ai/api/mcp/introduction
- CLI docs: https://docs.receiptor.ai/api/cli/introduction
- Privacy: https://receiptor.ai/privacy
- Help center: https://help.receiptor.ai
- Contact: info@receiptor.ai
