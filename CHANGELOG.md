# Changelog

## 0.1.3

- Leave the VERSION file out of the Claude package, because Anthropic's plugin directory refuses files without an accepted type. The plugin manifest still carries the version. Skills and the Receiptor connection are unchanged.

## 0.1.2

- Use a PNG listing icon for Anthropic's plugin directory, which does not accept SVG icons.
- Publish the Claude package to a dedicated branch that contains only the plugin's own files.

## 0.1.1

- Record the plugin version and available source revision in monthly document packs.
- Build Claude, OpenAI and Cursor packages from the same tagged source, with separate preview downloads.
- Keep host versions aligned and reject shipped changes that reuse an existing version.

## 0.1.0

Initial plugin with document search and review, document summaries, category-change previews, and draft monthly document packs. Several early test revisions shared this version; it does not uniquely identify their instructions.
