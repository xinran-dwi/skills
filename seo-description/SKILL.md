---
name: seo-description
description: Generate 3 SEO meta description options (140-160 characters) for a Design with AI newsletter article — draft or published. Use when the user wants an SEO description, meta description, or search-snippet for an article and provides a path or just-finished draft.
---

# SEO Description

Generate 3 SEO meta description options for a newsletter article, following the rules in `templates/seo-description.md`.

## Step 1 — Get the article path

If the user provided a path, use it. Otherwise ask: "Which article? (path to a file in `drafts/` or `newsletters/`)"

Read the article in full.

## Step 2 — Load the rules

Read `templates/seo-description.md`. The rules there are authoritative — follow them exactly:
- 140–160 characters per option (inclusive).
- 3 options, meaningfully different angles (outcome / problem / curiosity).
- Front-load the primary keyword.
- No clickbait the article doesn't deliver on.

## Step 3 — Return options

Format:

```
Option 1 (NNN chars): <description>
Option 2 (NNN chars): <description>
Option 3 (NNN chars): <description>
```

Count characters carefully (spaces and punctuation count). If any option is outside 140–160, regenerate it before showing.

## Step 4 — Wait for the pick, then write

Ask: "Which one? (1/2/3 — or want me to revise?)"

When the user picks, write **only the chosen description text** (no label, no count) to `<article-path>.seo.md`. Example: if the article is `drafts/2026-05-23-foo.md`, write to `drafts/2026-05-23-foo.seo.md`.

If the file already exists, overwrite it (the user explicitly picked a new one).

Report the output path. Done.
