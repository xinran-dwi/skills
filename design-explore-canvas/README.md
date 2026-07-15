Creator: Xinran Ma

More resources like this on: designwithai.co

_Disclaimer: It is a work-in-progress personal tool_

# design-explore-canvas

<video src="assets/demo_designcanvas-small.mp4" autoplay loop muted playsinline width="100%"></video>

## What it is

Generates 4 meaningfully distinct design directions from a single base design (screenshot, Figma URL, code file, or description), each with bullet-point rationale explaining the *why*. Appends every generation to a per-project visual canvas — like version control for design ideas — so you can scroll back, compare, and fork from any previous option.

## When to use it

- You want to see multiple distinct visual directions for a UI, not pixel tweaks of the same idea
- You have a base design (screenshot, Figma URL, code file, or a description) and want to explore what it could become
- You want each option to come with a written rationale explaining *why* the design made those choices
- You want to fork and iterate — reference any past option by its ID (e.g. "V2-Option3") and explore variations from there
- You're early in ideation and want to pick a direction before committing to implementation

## How to use it

### Install (one time)

**macOS / Linux**
```bash
mkdir -p ~/.claude/skills/design-explore-canvas
curl -fsSL https://raw.githubusercontent.com/xinran-dwi/skills/main/design-explore-canvas/SKILL.md -o ~/.claude/skills/design-explore-canvas/SKILL.md
```

**Windows (PowerShell)**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\design-explore-canvas"
Invoke-WebRequest "https://raw.githubusercontent.com/xinran-dwi/skills/main/design-explore-canvas/SKILL.md" -OutFile "$env:USERPROFILE\.claude\skills\design-explore-canvas\SKILL.md"
```

Restart Claude Code.

### Step by step

1. **Trigger the skill** — type `/design-explore-canvas` or ask naturally:
   - "Give me 4 options for this header section"
   - "Show me a few directions for this checkout screen"
   - "What could this dashboard look like?"
   - "Revise V2-Option3 with a softer feel"
   - "Iterate on the minimalist one"

2. **Provide a base design** — paste a screenshot, share a Figma URL, point at a component file, or just describe it in words. The skill adapts to whatever you have.

3. **Claude plans 4 distinct directions** — structurally different, not color tweaks. Each direction gets a short evocative name (e.g. "Editorial Calm", "Data Dense") and 4–7 rationale bullets written before any code.

4. **The canvas updates** — in Next.js projects, open `localhost:3000/canvas` to see all options. In other projects, open `explore-design-canvas/canvas.html`.

5. **Toggle and compare** — use the tab bar (or keys `1`–`5`) to switch between Base and the four options. The rationale panel updates per option.

6. **Fork any option** — reference its ID in a follow-up: "revise V2-Option3 with a softer feel" and Claude forks a new generation from that point, preserving lineage.

## Requirements

- [Claude Code](https://claude.ai/code)
- A base design to explore from (screenshot, Figma URL, component file, or written description)