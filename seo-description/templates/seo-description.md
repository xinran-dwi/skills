# SEO Meta Description Template

Rules for generating an SEO meta description for a Design with AI newsletter.

## Hard requirements

- **Length: 140–160 characters** (inclusive). Count characters including spaces and punctuation. Return the exact count next to each option.
- **3 options** per article, labeled `Option 1`, `Option 2`, `Option 3`.
- **Truthful** — must accurately reflect the article's content. No clickbait that doesn't pay off in the body.
- **Active voice**, present tense where possible.

## What a strong description does

1. **Front-loads the keyword**. The primary keyword should appear in the first ~60 characters (above the fold in SERPs).
2. **States the specific value** — what the reader learns or gets, not just the topic. ("Learn how to set up the Figma → Cursor workflow…" beats "A post about Figma and Cursor.")
3. **Implies an outcome** — speed, clarity, a working setup, a new capability.
4. **Ends with momentum** — a verb or hook that earns the click. Avoid trailing into a soft summary.

## Keyword guidance for the Design with AI niche

Primary keyword candidates depend on the article's topic. Common ones in this newsletter:

- `AI design workflow`, `design-to-code workflow`, `vibe coding`
- `Figma to Cursor`, `Figma MCP`, `design system AI`
- `prompt-driven design`, `AI for product designers`, `Magic Patterns`, `Stitch`, `Google AI Studio`
- Audience nouns: `product designers`, `UX designers`, `design teams`

Pick **one primary keyword** that matches the article's actual subject, and one secondary if it fits naturally. Don't keyword-stuff.

## Format to return

```
Option 1 (NNN chars): <description>
Option 2 (NNN chars): <description>
Option 3 (NNN chars): <description>
```

Each option should feel meaningfully different — vary the angle (outcome-led, problem-led, curiosity-led), not just the wording.

## After the user picks one

Write the chosen description to `<article-path>.seo.md` with just the chosen text (no labels, no character count) so it's copy-paste ready for Substack / publishing.
