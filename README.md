# Claude Skills

A collection of custom skills (slash commands) for [Claude Code](https://claude.ai/code). Each skill is a specialized workflow that extends what Claude Code can do.

## What are skills?

Skills are modular instruction files that give Claude Code a focused capability, just like a receipe or mini playbook that you can reuse. It helps for repeatable workflows.

## Skills

| Skill | Command | When to use | What it does |
|-------|---------|-------------|--------------|
| [claude-code-status-line-setup](./claude-code-status-line-setup/) | `/claude-code-status-line-setup` | Setting up the Claude Code footer | Install a 4-line footer showing context window %, git branch, active model, and live 5h/7d plan usage bars with reset times. Runs once; works on macOS, Linux, and Windows. |
| [design-explore-canvas](./design-explore-canvas/) | `/design-explore-canvas` | Exploring visual directions | Generate 4 distinct design directions from a base design (screenshot, Figma URL, or description). Interactive HTML viewer with rationale + a per-project canvas to track all explorations over time. |
| [design-exploration](./design-exploration/) | `/design-exploration` | Running a research-grounded design sprint | Structured design sprint for a UI section, grounded in a PRD and user research. Produces N explorations (each addressing a different research cluster) with a live toggle UI. |
| [design-inspect](./design-inspect/) | `/design-inspect` | Clicking an element to edit it | Click-to-edit overlay for your running Next.js app. Click any element, type a change, and Claude Code locates the exact JSX line and makes the edit. |
| [figma-to-claude-code](./figma-to-claude-code/) | `/figma-to-claude-code` | Converting a Figma design to a live prototype | Reads a Figma frame via MCP, plans the implementation, builds a pixel-faithful Next.js + Tailwind CSS prototype, verifies it in the browser, then guides revision or new-page iteration. |
| [find-skills](./find-skills/) | `/find-skills` | Finding a skill that does X | Search the open skills ecosystem for a skill that matches what you need. |
| [images-to-video](./images-to-video/) | `/images-to-video` | Turning diagrams into an animated trailer | Assemble SVG scenes or images into a self-playing, looping HTML trailer in the monochrome hairline style — each element draws, fades, or pops in individually. Screen-record one loop to get a video or GIF. |
| [github-readme](./github-readme/) | `/github-readme` | Documenting a new skill | Write a README.md for a Claude Code skill in Xinran's standard format — creator header, What it is, When to use it, and step-by-step How to use it sections. |
| [handoff](./handoff/) | `/handoff` | Wrapping up or resuming a session | Save and restore project context between sessions. Writes a `HANDOFF.md` with current work, failed approaches, next steps, and key files. Starts your dev server automatically on resume. |
| [newsletter-diagram](./newsletter-diagram/) | `/newsletter-diagram` | Making a minimalist diagram or UI mockup | Create a clean monochrome hairline+monospace diagram — git/branch, timeline, flow, or UI mockup — and export it as a downloadable PNG. The opposite of the colorful pastel-pill "generated" look. |
| [idea-to-prototype](./idea-to-prototype/) | `/idea-to-prototype` | Turning an idea into a prototype spec | Turn a rough product idea into a structured design spec ready to paste into a prototyping tool (Figma Make, v0, Stitch, etc.). |
| [slide](./slide/) | `/slide` | Turning content into a presentation | Turn any content into a polished presentation deck — a single self-contained HTML file in a Modern Swiss Editorial style, with live font, color, and transition toggles. |

## Installation

Install any skill:

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/<skill-folder> ~/.claude/skills/
```

Then restart Claude Code and invoke with the slash command shown above.

See each skill's `README.md` for detailed usage instructions.

## Requirements

- [Claude Code](https://claude.ai/code) — CLI or desktop app
- Design skills (`design-exploration`, `design-inspect`) assume a **Next.js + Tailwind** project

## License

MIT
