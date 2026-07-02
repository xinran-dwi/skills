Creator: Xinran Ma

More resources like this on: designwithai.co

_Disclaimer: It is a work-in-progress personal tool_

# slide

## What it is

Turns notes, outlines, or articles into a polished HTML presentation deck in a "Modern Swiss Editorial" style — serif display headlines, grotesque sans body, disciplined grid, generous whitespace. Ships with live keyboard controls to cycle fonts, colors, and slide transitions in the browser.

## When to use it

- You have notes, an outline, or an article and want to turn it into a presentation without touching design software
- You're building a pitch deck and want something that looks genuinely designed, not templated
- You want a portable, self-contained deck that opens in any browser with no install required
- You want to audition different typography and color combinations after the deck is generated
- You say things like "make slides from this", "turn this into a deck", or "build a presentation about X"

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git /tmp/xinran-skills
mkdir -p ~/.claude/skills
mv /tmp/xinran-skills/slide ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Trigger the skill** — just ask naturally (no slash command required):
   - "Make slides from this: [paste notes]"
   - "Turn this article into a deck"
   - "Build a pitch deck about X"

2. **Claude reads the content** — it structures the material into a slide-by-slide outline, one idea per slide, before writing any HTML

3. **A single HTML file is generated** — fully self-contained, no external dependencies after first load. Open it in any browser

4. **Customize live in the browser** using keyboard controls:
   - `←` / `→` / `Space` — navigate slides
   - `F` — cycle 4 font pairings
   - `C` — cycle 3 color themes
   - `M` — cycle 4 motion/transition modes (Push, Fade, Slide, Zoom)
   - `O` — open/close slide overview
   - `Esc` — close overview

5. **Iterate** — if you want to restructure, add slides, or change the tone, describe the change to Claude and it updates the file

## Requirements

- [Claude Code](https://claude.ai/code)
- Content to present (notes, outline, article, bullet points — any format works)
