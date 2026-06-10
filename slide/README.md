Creator: Xinran Ma
Website: designwithai.co

_Disclaimer: It is a work-in-progress personal tool

# Slide skill — how to use

**What it is:** A Claude Code skill that turns notes / outlines / articles into a polished HTML presentation deck (Modern Swiss Editorial style) with live keyboard controls for fonts, color, and motion.

## Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/slide ~/.claude/skills/
```

Restart Claude Code.

## Use it

In Claude Code, just ask naturally — e.g.

- "Make slides from this: [paste notes]"
- "Turn this article into a deck"
- "Build a pitch deck about X"

Claude will auto-trigger the skill and produce a single self-contained `.html` file.

## Keyboard controls (in the generated deck)

- `←` / `→` / `Space` — navigate
- `F` — cycle 4 font pairings
- `C` — cycle 3 color themes
- `M` — cycle 4 motion / transition modes (Push, Fade, Slide, Zoom)
- `O` — open / close slide overview
- `Esc` — close overview

The file is fully portable — open it in any browser, no install or internet required after first load.
