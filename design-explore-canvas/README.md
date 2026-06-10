Creator: Xinran Ma | designwithai.co

_Disclaimer: It is a work-in-progress personal tool

# design-explore-canvas — how to use

**What it is:** Generates 4 meaningfully distinct design directions from a single base design (screenshot, Figma URL, code file, or description), each with bullet-point rationale explaining the *why*. Outputs an interactive HTML viewer to compare options side by side, and appends every generation to a per-project visual canvas — like version control for design ideas.

## Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/design-explore-canvas ~/.claude/skills/
```

Restart Claude Code.

## Use it

In Claude Code, type `/design-explore-canvas` or ask naturally — e.g.

- "Give me 4 options for this header section"
- "Show me a few directions for this checkout screen"
- "What could this dashboard look like?"
- "Revise V2-Option3 with a softer feel"
- "Iterate on the minimalist one"

## How it works

1. You provide a base design (screenshot, Figma URL, code file, or text description)
2. Claude generates 4 distinct directions — structurally different, not just color tweaks
3. Each direction comes with a rationale panel explaining the design decisions
4. An interactive HTML viewer lets you toggle between options
5. Every generation is saved to `explore-design-canvas/canvas.html` inside your project — scroll back through past explorations and fork from any previous option by referencing its ID (e.g. "V2-Option3")

## Requirements

- [Claude Code](https://claude.ai/code)
- A base design to explore from (screenshot, Figma URL, component file, or written description)
