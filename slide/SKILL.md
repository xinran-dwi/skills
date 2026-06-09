---
name: slide
description: Turn content into a modern, sleek, design-led presentation deck as a single self-contained HTML file in a "Modern Swiss Editorial" style (serif display headlines, grotesque sans body, disciplined grid, generous whitespace). The output has live keyboard toggles to cycle 4 font pairings, 3 color styles, and 4 slide-transition modes, plus a slide-overview nav drawer. Use this whenever the user wants to "make slides", "build a deck", "create a presentation", "turn this into slides", "make a pitch deck", or pastes notes/an outline/an article and wants it presented. Prefer this over generic slide generation whenever taste and visual polish matter.
---

# Slide

Generate a presentation deck as one portable HTML file with genuine design taste: editorial serif headlines, a disciplined Swiss grid, generous negative space, and a quiet sense of art direction. The deck ships with live controls so the user can audition typography and color in the browser.

## What makes this skill different

Most slide generators clone a template or copy whatever example they were shown, producing rigid, samey decks. This skill does the opposite: it carries a strong, reusable design *system* (the chrome, the type scale, the surfaces, the motion) and composes each slide's layout from the content in front of it. The system guarantees coherence; the composition keeps it from feeling templated.

Two principles sit underneath everything:
- **Structure carries the design.** Grid, typography, hairlines, and whitespace do the work. Decoration is earned, never default.
- **One idea per slide.** A slide that says one thing clearly beats a slide that says four things at once.

## Workflow

### 1. Understand the content
Read what the user gave you (notes, outline, article, bullets, a doc). Identify the spine: what's the opener, what are the sections, what's the data, what's the close. If they handed you raw prose, distill it. Headlines become short phrases, body becomes tight. If the content is thin or ambiguous about structure, ask one or two clarifying questions rather than padding with filler.

Note any brand input (a brand color, a company name, a logo) so you can fold it in.

### 2. Plan the deck
Decide the slide sequence and which **surface** each slide uses for rhythm (see `references/slide-patterns.md`). Rotate surfaces so the deck breathes: a typical cadence is brand opener, accent section break, paper/ink content slides, occasional accent break, brand or accent closer. Don't run five identical-looking slides in a row.

Map each slide to a pattern (title, agenda, stat cards, timeline, etc.) but feel free to adapt or invent layouts when the content calls for it. Vary which side the headline sits on. Avoid making every slide structurally identical.

### 3. Build the file
Start from `references/scaffold.html`. It is the portable shell and contains everything that must not be reinvented:
- All Google Fonts preloaded (so the file works offline-of-your-repo, anywhere with a network)
- The **4 font presets** and **3 color themes** as CSS variables
- The **F / C keyboard toggles**, arrow-key navigation, the on-screen indicator, and the 16:9 scaled stage
- The full component CSS (typography scale, surfaces, cards, timeline, lists, motion)

Compose slides into the region between `<!-- SLIDES:START -->` and `<!-- SLIDES:END -->`, using the patterns in `references/slide-patterns.md`. Replace the `__PLACEHOLDER__` tokens (title, presenter, etc.). Keep the first slide marked `is-active`. Wrap one or two lead elements per slide in `class="rise"` for the entry animation — not every element.

**Do not** rewrite the toggle logic, the theme tokens, or the font preset definitions unless the user explicitly asks to change them. Those are the load-bearing features.

### 4. Verify before declaring done
Open the file in a browser and check:
- It renders at a clean 16:9 and scales with the window
- `F` cycles the four font pairings, `C` cycles the three color styles, and every slide stays legible in all three palettes (this is the most common failure: a text color that vanishes on one theme)
- `M` cycles the four transition modes (Push, Fade, Slide, Zoom) and each navigates cleanly in both directions
- `O` opens the left slide-overview nav and `O` or `Esc` closes it; clicking a thumbnail jumps to that slide; the current slide is highlighted
- Arrow keys / space navigate; the page indicator updates
- Motion stays subtle, never a distracting cascade

Fix anything that breaks, especially legibility across themes. Then tell the user where the file is and remind them of the F / C / M / O / arrow controls.

## The design system at a glance

**Typography.** Serif display for headlines and numerals, grotesque sans for body and labels, ALL-CAPS letter-spaced sans for kickers. The presets (toggle `F`): Editorial Classic (Newsreader + Inter, default), Contrast Modern (Fraunces + Inter Tight), Refined Light (Instrument Serif + Geist), Literary (Playfair Display + Work Sans).

**Color.** Four semantic surfaces (paper, ink, brand, accent) that the theme maps to real colors, so the toggle (`C`) recolors the whole deck coherently. Styles: Verdant (forest + chartreuse, default), Noir (near-black + cobalt), Terra (warm charcoal + clay).

**Layout.** Header band (caps kicker left, page number right, hairline under), big serif headline, asymmetric headline/content split, hairline dividers, numbered pages, lots of negative space.

**Motion.** Four slide-transition modes, toggled live with `M`: Push (cinematic — the outgoing slide recedes and softly blurs as the incoming slide pushes in full-bleed from the edge, direction-aware, default), Fade (crossfade plus a per-element rise stagger), Slide (the whole slide drifts horizontally, direction-aware), and Zoom (the slide scales in). All are eased and never attention-seeking. The per-element rise stagger is the signature of Fade; in Push, Slide, and Zoom the slide moves as one unit, so rise is intentionally disabled to avoid double motion.

## Anti-patterns (what wrecks the taste)

- Cloning a provided example deck's exact layouts, or reusing one template for every slide
- Centering everything; ignoring the grid
- Bullet walls and paragraphs longer than ~3 lines
- Filling whitespace just because it exists
- Clip art, heavy drop shadows, stocky corporate gradients, neon
- Animating every element, or using showy transitions
- Sans-serif numerals where a serif numeral would read as editorial

## Files

- `references/scaffold.html` — the portable shell. Always start here. Read it before composing.
- `references/slide-patterns.md` — the layout library (title, agenda, overview+team, stat cards, milestones, timeline, next steps, Q&A, section break) plus composition guidance.
