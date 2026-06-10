Creator: Xinran Ma
More resources like this on: designwithai.co

_Disclaimer: It is a work-in-progress personal tool_

# design-exploration

## What it is

Runs a structured design sprint for a specific UI section, grounded in a PRD and user research. Produces N explorations — each addressing a *different* cluster of research findings, not just visual tweaks — and renders them in a live toggle UI with the full page context visible.

## When to use it

- You have a UI section to redesign and want multiple distinct directions, not just color tweaks
- You have a PRD and user research doc and want explorations that are actually grounded in them
- You want to compare redesign approaches side by side with full surrounding page context still visible
- You're running a design sprint and need to generate options quickly from existing briefs
- You want each exploration to address a *different* user research insight, not variations of one idea

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/design-exploration ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Trigger the skill** — type `/design-exploration` or ask naturally:
   - "Run a design exploration for the checkout summary section"
   - "Create 3 explorations for the hero component"
   - "Explore redesigns for the About This Home section"

2. **Confirm the brief** — Claude will ask which section to redesign, how many explorations (default: 3), and where your brief files live. It looks in `_brief/`, `docs/`, and `brief/` automatically.

3. **Claude reads your context** — it reads your PRD, user research file, current screenshot, and the existing component before planning anything.

4. **Explorations are planned** — each exploration is assigned a *different* research insight as its anchor. Two explorations won't feel like cousins.

5. **Components are written** — each exploration becomes a separate file: `SectionV1.tsx`, `V2.tsx`, `V3.tsx`, etc.

6. **Toggle UI is added** — `ExplorationToggle.tsx` lets you switch between explorations in the browser with the full surrounding page context still visible.

## Requirements

- [Claude Code](https://claude.ai/code)
- React + Tailwind CSS project
- A PRD or product context doc
- A user research doc (usability findings, pain points)
- A screenshot of the current design
- The current component file for the section being redesigned
