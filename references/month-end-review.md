# Interactive month-end review

Use this when the host can render a private interactive artifact or an existing Receiptor MCP App. The skill supplies review instructions; it does not itself install an app or grant new permissions. Use the host's documented APIs and available tools. Do not invent a connection, submission callback or write capability.

## Review contents

Build the interface from the same structured proposals used for the pack, with workspace, period, scope and snapshot time visible. Each proposal keeps a stable decision ID and the exact record IDs and values from its reviewed snapshot.

- Start with a compact list of the most consequential questions. Allow expansion to see all affected documents, original evidence, current/proposed values and known merge effects. Keep source text as text, not executable content.
- Offer approve, change/reply, decline and leave unresolved. Nothing is approved by default. Context answers and lasting memories/intake rules are separate choices; leaving one blank must not silently select another.
- For business context, allow another business, mixed use and unresolved where relevant. Do not turn a yes/no answer into a broader action.
- Show a summary of selected changes before submission. Include a separate **Prepare draft with unresolved items** route. A selected checkbox or edited field is local draft state until explicitly submitted.

Keep the presentation simple: a readable light surface, restrained emerald actions, clear labels, keyboard-accessible controls and expandable evidence. Avoid animation that obscures changes or makes approval feel automatic.

## Submit and execute

Use a real, supported submission channel when available. The submitted decision must identify the selected proposal IDs, exact record IDs, proposed values and any user edits; it is not blanket authority over a refreshed search. Check the current records against that snapshot before executing and surface material drift. Preserve Receiptor's existing authorization and approval flow.

If the artifact cannot return decisions to the conversation, provide a working copy/download summary for the user to submit in chat. Label it **Copy decisions for Claude**, not **Apply in Receiptor**. Do not claim that local selection saved or changed anything. Never bypass approval-required tools by moving execution into an artifact or weakening connector permissions.

Keep production evidence private. Do not publish the artifact or put customer data in shared storage as part of preparing a pack. Collect only the evidence needed for the review and never embed credentials or access tokens.

After execution, show verified, partial, pending or failed outcomes against the same decision IDs. Generate the workbook, originals and handoff from the refreshed source snapshot. The interactive review supplements those deliverables; it does not replace them.
