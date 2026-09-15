# Verifying against a design export

The other ground-truth path. Read this instead of Phase 1 and Phase 2 of `SKILL.md` when the
original isn't running code. Everything else in the main file still applies — the region walk,
fix-scoping in Phase 3, re-verification in Phase 4, honest reporting, offering the comparison.

## When you're on this path

The thing being rebuilt exists only as a picture: a Figma frame export, a PNG spec, a design
handoff. There is no component source to fetch, no live demo to open, and no DOM on the other
side to query.

## Why this isn't the "last resort screenshot" case

Phase 1(c) of the main file treats a screenshot as a degraded substitute for the real thing,
and rightly so — there, a screenshot is a stale picture of code that has since moved on. Here
the export *is* the spec. Nothing more current exists. Staleness is still worth asking about,
but it's a question about which version of the design you were handed, not about the medium.

That flips the posture: you're not squinting at a lossy record of the truth, you're measuring
the truth. So measure it. Which leads to the rule this whole path exists to enforce:

> **Never read a color with your eyes.** Two dark navies, `#0a0e41` and `#050a36`, are
> indistinguishable when you flip between two screenshots — and obviously different to whoever
> opens the build next to the design. Every color that reaches a token comes from a sampled
> measurement. A value you estimated and labeled "approximate" in the report is not a
> measurement; it is the same wrong pixel with a disclaimer attached.

## Inputs

- **The export file itself, on disk.** If it was pasted into the conversation rather than saved,
  it is still a file somewhere — agent harnesses cache pasted images (Claude Code keeps them in
  `~/.claude/image-cache/<session-id>/`). Look there, look in the obvious export folders, and
  ask the user before concluding you can't have it. "The reference wasn't available so colors
  were estimated" is a failure report, not a constraint.
- **The design size each export represents** — the artboard's own dimensions (390×844, 1440×931).
  Every measurement below is normalized to these, so they compare directly to CSS.

Copy the exports into the project (`design-refs/`) rather than reading them from a temp path.
They are the spec; the repo should carry them.

## Phase 1 — Establish ground truth

1. **Locate the artboard.** The export usually includes canvas around the frame. Find the frame
   bounds and derive the scale from them:
   `python3 <skill>/scripts/measure-ref.py locate design-refs/mobile.png --design 390x844`
   Sanity-check the reported design size against what you expect — if it comes back 480×952 for
   a 390×844 frame, the mask caught a caption or a drop shadow and every later number is skewed.
2. **Separate the design from the artboard chrome.** Exports carry things that are not UI: frame
   title captions, annotation badges, status chips, collaborator cursors and avatars parked over
   the canvas. These are the export's furniture. Do not build them, and say in the report which
   ones you identified, so the next reader doesn't file them as missing elements.
3. **Write `samples.json`** next to the exports — the views and the points the comparison runs
   on:

   ```json
   {
     "mobile": {
       "design": [390, 844],
       "points": { "page-top": [195, 20], "card-row1": [45, 552], "cta-fill": [60, 800] }
     }
   }
   ```

   Choosing points is the skilled part: each one must sit **inside a flat region of one
   surface** — off text strokes, off photography, off a rounded corner, off the 3px of padding
   at the edge of a pill. A point that lands on a glyph measures antialiasing, and it will move
   the moment either side's text metrics change, which makes the check flap for no reason.
   Cover: each surface at top/middle/bottom (gradients hide there), each card fill, each accent,
   each badge.

## The four traps

Each of these silently produces confident, wrong numbers.

**1. Color profile.** Screenshots from design tools carry a display ICC profile. Their raw
pixel values are not sRGB — reading them directly is 5-10 levels off per channel, which is
enough to build a whole palette wrong *after* you started measuring. Convert to sRGB before
reading anything (the script does this in `load_srgb`; if you sample any other way, do it
there too).

**2. Scale.** The frame is at some arbitrary zoom. Work in design pixels, never image pixels,
or nothing you measure compares to a CSS value.

**3. Density banding under-measures.** To find an element's box, scan a center line outward for
the color transition. Counting how many pixels per row match a fill *feels* more robust and
isn't: antialiased rounded corners fail the match, so the first and last rows get dropped and
every card comes out ~8px short — with the missing height reappearing as phantom gap between
rows. This exact error produced a "measured" grid with cards too short and gaps too large.

**4. Noise floor.** A flat surface in an export varies by about ±5 per channel between adjacent
pixels. One sampled pixel is therefore not a color:
- take **region medians** for surfaces (`measure-ref.py medians <img> --view v --region x,y,w,h`)
- set the comparison tolerance **above** the noise (5 works for screenshot exports, tighter for
  lossless ones) and stop there — below it you are fitting compression artifacts
- state the floor in the report, so a future reader knows why the tolerance is what it is

## Phase 2 — Structured discrepancy pass

Same goal as the main file: an itemized list, walked region by region. Two of the three passes
change.

**a) The render pass.** Both sides must be made comparable first: normalize the export to its
design size and the build screenshot to the same, then write them out as one side-by-side or
flip image and *look at it*. This catches the class of thing measurement never will — a corner
radius that should be a full stadium, an invented border, an icon at the wrong weight, type
that is simply too big. Take the build screenshot at the exact design viewport (390×844,
1440×931), not at a nearby one.

**b) There is no source pass.** The export has no styling layer to diff — that half of the main
file's Phase 2 doesn't exist here. Say so in the report rather than leaving a reader wondering
whether it was skipped. Its weight moves onto (c).

**c) The measurement pass — color first, then geometry.**

```bash
python3 <skill>/scripts/measure-ref.py compare design-refs/mobile.png shots/mobile.png \
  --view mobile --tolerance 5
```

It prints every sample point as design-file vs build with per-channel deltas, flags anything
past tolerance, and exits non-zero — so it can gate a commit, and so "I checked the colors"
becomes a reproducible claim instead of an assurance.

Then rects, via `edges` on the export and `getBoundingClientRect()` on the build: the repeated
element (card, row, tile) width and height, its internal padding, grid gaps, the main
containers' origins, and the primary action's box. Put the pairs in the report as numbers.

Two things worth measuring explicitly because they are easy to get wrong by eye and cheap to
check: **corner radius** (walk the edge inset at several offsets from the top — if it reaches
full width at half the height, it's a stadium, not a rounded rectangle) and **type size** (an
ink-width comparison of the same string on both sides is a more reliable read than cap height).

### Sort what you find

`FIDELITY_REPORT.md`, same as the main file, but the four buckets become three — "wrong
mapping" and "styling dropped" both presume component source:

1. **Missing** — an element the design has and the build doesn't.
2. **Invented** — an element the build has and the design doesn't. Watch for the compensating
   case: a border added to fake a fill that was never sampled.
3. **Wrong value** — the right element with a measured-wrong color, size, radius, gap, or type
   scale. Record design value next to build value; this bucket is where an export-based check
   earns its keep, and it is invisible to a props-level review.

## The export is also your asset source

Don't ship placeholder art next to a design you can crop. Photography, logos and thumbnails come
straight out of the export at source resolution:

```bash
python3 <skill>/scripts/measure-ref.py crop design-refs/mobile.png --view mobile \
  --rect 0,133,390,320 --out public/img/hero.jpg
```

A placeholder gradient where the design has a photograph makes every side-by-side ambiguous —
you cannot tell a surface mismatch from the absence of an image.

## Phase 4 — Re-verify

As the main file, plus: **re-run `compare`**. Editing tokens invalidates the previous run. A
geometry re-measure with no color re-run leaves exactly the hole this path exists to close.

Done means: the comparison passes at a stated tolerance, the numbers are in the report, the
remaining approximations are named individually with the reason each one is still an estimate,
and the side-by-side is there for the user to open.
