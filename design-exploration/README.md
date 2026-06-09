Creator: Xinran Ma | designwithai.co

_Disclaimer: It is a work-in-progress personal tool._

# design-exploration — how to use

**What it is:** Runs a structured design sprint for a specific UI section, grounded in a PRD and user research. Produces N explorations — each addressing a *different* cluster of research findings, not just visual tweaks — and renders them in a live toggle UI with the full page context visible.

## Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/design-exploration ~/.claude/skills/
```

Restart Claude Code.

## Use it

In Claude Code, type `/design-exploration` or ask naturally — e.g.

- "Run a design exploration for the checkout summary section"
- "Create 3 explorations for the hero component"
- "Explore redesigns for the About This Home section"

## How it works

1. You specify which UI section to redesign and how many explorations (default: 3)
2. Claude reads your PRD, user research file, current screenshot, and the existing component
3. It plans N distinct explorations — each grounded in a different user research insight
4. Each exploration becomes a separate component file (`SectionV1.tsx`, `V2.tsx`, `V3.tsx`)
5. A toggle UI (`ExplorationToggle.tsx`) lets you switch between explorations with full surrounding page context still visible

## Requirements

- [Claude Code](https://claude.ai/code)
- React + Tailwind CSS project
- A PRD or product context doc
- A user research doc (usability findings, pain points)
- A screenshot of the current design
- The current component file for the section being redesigned
