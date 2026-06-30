# Export Policy

The public package must be generic.

## Include

- generic skill instructions
- generic references
- configurable scripts
- synthetic examples
- schemas
- small text fixtures

## Exclude

- proprietary PDK files
- foundry decks
- private layouts
- private schematics
- solver outputs
- real screenshots
- textbook PDFs
- OCR output or full-text textbook extraction
- copied textbook paragraphs, tables, figures, or long derivations
- local absolute paths
- private repository URLs
- user tokens or credentials

## Redaction Checks

Before publishing:

```text
search for local absolute paths
search for private repository URLs
search for EDA database extensions
search for PDF/OCR/textbook dumps
search for private PDK/foundry names
search for tokens or credentials
```

Every hit must be a placeholder, synthetic example, or removed.

Textbook-derived material is allowed only as original summaries, chapter-level
source labels, reading maps, and agent checklists.
