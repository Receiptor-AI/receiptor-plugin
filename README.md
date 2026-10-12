# Receiptor AI

Get your receipts and invoices ready for your accountant. Find documents, check expense categories, and prepare a draft monthly pack for review.

Receiptor AI collects and organizes receipts and invoices from connected email accounts, WhatsApp, and uploads. This plugin lets you work with those saved documents in Claude, Codex, or Cursor.

Ask for what you need in your own words. Your assistant helps you find documents, check unclear details, and prepare files to hand over, with less searching and sorting by hand.

## What you can do

| Task | How it helps |
| --- | --- |
| Find and check documents | Look up a receipt or invoice by supplier or date. Check its amount, details, possible duplicates, or whether it was sent to accounting software. |
| Review expense categories | Check how documents are categorized and preview corrections before approving changes. |
| Summarize your documents | See document counts and totals by supplier, category, or month. Your assistant explains limits that affect the totals. |
| Prepare a monthly document pack | Gather a draft spreadsheet, available original files, and questions for your accountant to review. |

## What is in a monthly pack?

- **A spreadsheet** listing the month's documents, totals by currency, and items that need review.
- **A ZIP of available original files**, such as receipts and invoices.
- **A file checklist** showing what was included and which originals could not be retrieved.
- **A handoff note** explaining the scope, gaps, and decisions still needed.

The pack covers documents saved in Receiptor. Your assistant checks for disconnected inboxes and other known gaps, and reports what it could not verify. You or your accountant review the draft and make the accounting decisions.

The monthly pack is currently in testing. Creating its files requires an assistant that can build spreadsheets and download files. Preparing documents is one part of month-end bookkeeping; bank reconciliation and completing the books remain separate tasks.

## Get started

1. Install the plugin in your AI assistant.
2. Connect your Receiptor AI account and choose the workspace you want to use.
3. Ask for the task you need. For example:

> Prepare September's document pack for my accountant to review.

> Find my receipts from a supplier and check their dates and amounts.

> Check this supplier's expense categories and show me any suggested changes.

> Show this month's document totals by supplier, with each currency separate.

A Receiptor AI account is required. You can get started without a subscription, run retroactive extractions, and work with saved documents. Ongoing document collection requires a Receiptor AI subscription.

Preparing a pack reads your existing records. Changes to records, saved business guidance, accounting exports, and sharing require your permission and any approvals Receiptor requires.

## Your data

Your assistant connects to Receiptor's server at `https://mcp.receiptor.ai` using the account and workspace you authorize. This connection uses MCP, the standard AI assistants use to work with other services, and OAuth for sign-in.

When you ask for a task, the assistant sends Receiptor the details needed to carry it out. These may include search terms, document IDs, dates, business filters, information you provide, and proposed changes.

Receiptor returns data from your authorized workspace. This may include receipt and invoice details, connected email addresses and inbox status, expense categories, review questions, accounting export status, saved business guidance, and links to original files. Your assistant processes these responses under its provider's data-handling terms.

To build a pack, your assistant downloads originals from the file-storage links Receiptor provides and creates files in its own file environment. These files can contain financial and personal information. You decide whether to share them with your accountant.

The plugin contains instructions and connection settings. It has no bundled programs, automatic scripts, or separate analytics. See [Receiptor's privacy policy](https://receiptor.ai/privacy) for how Receiptor handles your data.

## Help and support

- [Help center](https://help.receiptor.ai)
- [Connection documentation](https://docs.receiptor.ai/api/mcp/introduction)
- [Privacy policy](https://receiptor.ai/privacy)
- [Terms of service](https://receiptor.ai/terms)
- Contact: info@receiptor.ai

<details>
<summary>Technical setup and plugin files</summary>

Source repository: https://github.com/Receiptor-AI/receiptor-plugin

Test locally in Claude Code:

```bash
claude --plugin-dir .
```

Add the plugin marketplace in Codex:

```bash
codex plugin marketplace add Receiptor-AI/receiptor-plugin
```

The package includes Claude, Codex, and Cursor manifests, four skills, shared workspace checks, and Cursor operating rules. The Claude and Codex manifests explicitly reference the shared `mcp.json` connection configuration:

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

Complete OAuth after installation. Confirm the active workspace with `workspace_get_context`; use `workspaces_list` and `workspace_switch` to change it.

Each skill reads `references/workspace-checks.md` for the checks its task needs. Tools such as `context_readiness`, `sources_email_list`, and `integrations_list` remain available to other MCP clients. Clients that do not load this plugin need the skill instructions supplied separately.

The skills are `document-review`, `categorization-review`, `document-analysis`, and `month-end-document-pack`. They use live Receiptor data and preserve the service's authorization and approval requirements.

</details>
