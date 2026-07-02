Creator: Xinran Ma

More resources like this on: designwithai.co

# figma-to-claude-code

## What it is

A Claude Code skill that converts any Figma frame into a fully working Next.js + Tailwind CSS prototype — pixel-faithful, with real design tokens wired up, and running live in your browser. It also guides you through iterating on the design or building new consistent pages afterward.

## When to use it

- You have a Figma design and want to see it running as real code in the browser
- You want to turn a static mockup into a clickable, interactive prototype
- You're a designer handing off to engineers and want a high-fidelity reference implementation
- You want to iterate on a design by sending focused Figma frame URLs back to Claude
- You want to build additional pages that stay visually consistent with an existing prototype

## How to use it

### Install (one time)

**macOS / Linux**
```bash
mkdir -p ~/.claude/skills/figma-to-claude-code
curl -fsSL https://raw.githubusercontent.com/xinran-dwi/skills/main/figma-to-claude-code/SKILL.md -o ~/.claude/skills/figma-to-claude-code/SKILL.md
```

**Windows (PowerShell)**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\figma-to-claude-code"
Invoke-WebRequest "https://raw.githubusercontent.com/xinran-dwi/skills/main/figma-to-claude-code/SKILL.md" -OutFile "$env:USERPROFILE\.claude\skills\figma-to-claude-code\SKILL.md"
```

Restart Claude Code.

### Step by step

1. **Check Figma MCP** — Claude verifies Figma is connected silently; if not, it walks you through setup

2. **Paste your Figma URL** — In Figma, right-click your main frame → Copy as → Copy link to selection, then paste it into Claude Code

3. **Set up your project** — Claude checks for an existing Next.js + Tailwind project; if none exists, it offers to create one for you

4. **Review the plan** — Claude reads the design (layout, tokens, components) and writes a plain-language plan before writing any code; you approve it or request changes

5. **Watch it build** — Claude implements the design file by file, following your Figma tokens and layout exactly, then starts the dev server automatically

6. **See it live** — Claude opens the prototype in a browser, compares it against the Figma screenshot, and fixes anything that doesn't match

7. **Iterate or expand** — Choose to refine a specific area (using a scoped Figma URL or a screenshot markup) or build a new consistent page from the same codebase

## Requirements

- [Claude Code](https://claude.ai/code)
- [Figma MCP](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server) connected in Claude Code
- A Figma file with your design
