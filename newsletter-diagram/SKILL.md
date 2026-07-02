---
name: newsletter-diagram
description: >-
  Create clean, minimalist MONOCHROME diagrams and UI mockups in a hairline +
  monospace style, exported as a downloadable PNG (not an inline HTML widget).
  The look: a single ink color on white, thin hairline strokes, monospace
  lowercase labels, near-square corners, and lots of whitespace — the opposite
  of the colorful pastel-pill "generated" look. Use this skill WHENEVER the user
  asks for a diagram, flowchart, timeline, git/branch diagram, architecture
  sketch, or a UI/app mockup AND wants it (a) in a minimalist / monochrome /
  hairline / "not-AI-looking" style, or (b) as a downloadable PNG / image file
  they can drop into a newsletter, slides, doc, or Figma — even if they only say
  "make it a png", "minimalist diagram", "monospace diagram", "for my
  newsletter", "the same diagram style", or "downloadable image". Prefer this
  over inline HTML/SVG widgets any time a saved image file is wanted.
---

# Newsletter Diagram

Produce a polished, intentional-looking diagram or UI mockup in a strict
monochrome-hairline-monospace style, then rasterize it to a high-resolution
**PNG file** the user can download and reuse.

The whole point of this style is to *not* look auto-generated: no pastel fills,
no rounded pill badges, no icon chips. Just one ink, thin lines, monospace type,
and air. Information is carried by **form** (solid vs hollow, solid vs dashed, a
small ✕) rather than by color.

## When to use this

Trigger this skill for any of:
- "Make a minimalist / monochrome / hairline diagram"
- "Same diagram style as before" (in a thread already using this look)
- "Turn this into a downloadable PNG / image"
- Diagrams or mockups intended for a newsletter, slide, doc, README, or Figma
- Git/branch/merge diagrams, timelines, simple flows, small UI mockups

If the user wants an *interactive* inline widget instead of a saved file, this
skill does not apply — use the normal visualizer. This skill always ends in a
PNG on disk.

## The fixed palette (PNG = no theme switching)

Because the output is a static PNG, colors are fixed hex (dark ink on white) —
do NOT use CSS theme variables, they only work in live widgets.

| Role            | Hex       | Use |
|-----------------|-----------|-----|
| ink (primary)   | `#1b1b19` | main strokes, primary text, solid dots |
| secondary text  | `#6c6b64` | sub-labels, body lines |
| tertiary        | `#a3a199` | faint annotations, disabled/locked, marker lines |
| hairline-light  | `#e2e0d8` | dividers, locked button borders |
| hairline-medium | `#c9c7be` | panel borders, line-number text |
| active border   | `#9a988f` | the one button/element you want noticed |
| background      | `#ffffff` | canvas fill (always paint it; PNG needs a bg) |

Font: `'DejaVu Sans Mono','Liberation Mono',monospace` (DejaVu Sans Mono is
installed). At font-size F, a monospace glyph advances ~`0.6 * F` px — use this
to place text and size boxes (e.g. 15px → ~9px/char).

## The visual vocabulary

Keep it spare. Distinguish things by shape, not color:
- **Solid dot** = something landed / committed / established. **Hollow dot**
  (`fill="none"` + 1px stroke) = in-progress / branch / draft.
- **Solid line** = the main / established path. **Dashed line**
  (`stroke-dasharray="4 4"`) = an attempt, a proposal, in-progress, or blocked.
- **✕** (two crossed 1.5px strokes) = conflict / error / blocked.
- **Triangle outline + `!`** = a warning.
- Labels: monospace, **lowercase**, `letter-spacing` ~0.04em. Primary labels in
  ink; annotations in tertiary.
- Strokes are thin (1px; 0.5px reads even finer). Corners near-square: `rx="6"`
  for panels, `rx="2"–"4"` for chips/buttons, never pill-shaped.
- Leave generous margins. Whitespace is what signals "designed", not "templated".

See `references/style.md` for ready-to-adapt SVG snippets (panel frame, dot
timeline with branch+merge, code block with conflict markers, button row,
triangle warning, ✕ mark). Read it before assembling — copying a known-good
snippet is faster and avoids layout mistakes.

## Workflow

1. **Decide the layout.** Diagram (timeline / flow / branch) or UI mockup
   (panel with header, body, actions). Sketch coordinates mentally on an 900px-
   wide canvas with ~40px margins. Keep it to a few elements — this style lives
   on restraint.

2. **Build the SVG as a string** using the palette + vocabulary above. Hand-
   place coordinates; monospace makes widths predictable. Always paint a white
   background rect first. Escape `<`, `>`, `&` in any literal text (e.g. git
   conflict markers become `&lt;&lt;&lt;...`).

3. **Render to PNG at 2× scale** with the bundled script:
   ```bash
   python3 scripts/render_png.py --svg-file diagram.svg \
     --out /mnt/user-data/outputs/<name>.png --scale 2
   ```
   The script installs `cairosvg` if missing, reads width/height from the SVG,
   renders at the given scale on a white background, and writes the PNG. You can
   also pipe SVG via stdin: `... | python3 scripts/render_png.py --out ...`.

4. **Verify and deliver.** `view` the PNG to check alignment (a common slip is a
   side-label sitting one line off its target). Fix and re-render if needed.
   Then `present_files` the PNG and give a one or two sentence summary — no long
   postamble.

## Quality checklist before delivering

- White background painted; everything monochrome (no stray theme colors).
- All text monospace, lowercase, with light letter-spacing.
- Distinctions are by shape (solid/hollow, solid/dashed, ✕), not color.
- Corners near-square; borders hairline-thin.
- Labels aligned to the elements they annotate (re-check after viewing).
- Output is a real PNG in `/mnt/user-data/outputs/`, presented to the user.
