# Claude Code Skills

A collection of custom skills (slash commands) for [Claude Code](https://claude.ai/code). Each skill is a specialized workflow that extends what Claude Code can do.

## What are skills?

Skills are modular instruction files that give Claude Code a focused capability — like running a design sprint, building a presentation deck, or generating design explorations. Install a skill once and invoke it with a slash command.

## Skills

| Skill | Command | What it does |
|-------|---------|--------------|
| [design-explore-canvas](./design-explore-canvas/) | `/design-explore-canvas` | Generate 4 distinct design directions from a base design (screenshot, Figma URL, or description). Shows an interactive HTML viewer with rationale and a per-project canvas to track all explorations over time. |
| [design-exploration](./design-exploration/) | `/design-exploration` | Run a structured design sprint for a UI section, grounded in a PRD and user research. Produces N distinct explorations (each addressing a different cluster of research findings) with a live toggle UI. |
| [design-inspect](./design-inspect/) | `/design-inspect` | Open your running Next.js app with an inspect overlay — click any element, type a change request, and Claude Code locates the exact JSX line and makes the edit. |
| [find-skills](./find-skills/) | `/find-skills` | Search the open skills ecosystem for a skill that matches what you need. Uses the [skills.sh](https://skills.sh/) registry. |
| [idea-to-prototype](./idea-to-prototype/) | `/idea-to-prototype` | Turn a rough product idea into a structured design spec ready to paste into a prototyping tool (Figma Make, v0, Stitch, etc.). |
| [slide](./slide/) | `/slide` | Turn any content into a polished presentation deck — a single self-contained HTML file in a Modern Swiss Editorial style, with live font, color, and transition toggles. |
| [stitch-brainstorm](./stitch-brainstorm/) | `/stitch-brainstorm` | Turn a rough product idea into clickable visual design directions using the Stitch MCP. Generates 3–5 variants to compare quickly. |

## Installation

Install any skill using the Claude Code CLI:

```bash
# Install a single skill
claude skill install https://github.com/xinran-dwi/skills/tree/main/design-explore-canvas

# Or clone the repo and install from local path
git clone https://github.com/xinran-dwi/skills.git
claude skill install ./skills/design-explore-canvas
```

Then invoke it in Claude Code with the slash command shown in the table above.

## Requirements

- [Claude Code](https://claude.ai/code) — CLI or desktop app
- Most design skills assume a **Next.js + Tailwind** project
- `design-inspect` requires a running dev server
- `stitch-brainstorm` requires the [Stitch MCP](https://stitch.withgoogle.com/) configured

## License

MIT
