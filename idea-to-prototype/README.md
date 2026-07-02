Creator: Xinran Ma

More resources like this on: designwithai.co

# idea-to-prototype

## What it is

Turns a rough product idea into a structured design spec (markdown) ready to paste into a prototyping tool — Figma Make, v0, Stitch, Pencil, or similar. Bridges the gap between "I have an idea" and "I have something to show."

## When to use it

- You have a product idea — even just one sentence — and want to turn it into a visual prototype quickly
- You want a structured spec to paste into Figma Make, v0, Stitch, or Pencil and get clickable screens back
- You're a designer or PM starting a new product and want to move from idea to prototype without writing a full PRD
- You want to explore what a product could look like before committing to any design tool
- You say things like "I want to build an app that...", "help me design...", or "I have an idea for..."

## How to use it

### Install (one time)

**macOS / Linux**
```bash
mkdir -p ~/.claude/skills/idea-to-prototype
curl -fsSL https://raw.githubusercontent.com/xinran-dwi/skills/main/idea-to-prototype/SKILL.md -o ~/.claude/skills/idea-to-prototype/SKILL.md
```

**Windows (PowerShell)**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\idea-to-prototype"
Invoke-WebRequest "https://raw.githubusercontent.com/xinran-dwi/skills/main/idea-to-prototype/SKILL.md" -OutFile "$env:USERPROFILE\.claude\skills\idea-to-prototype\SKILL.md"
```

Restart Claude Code.

### Step by step

1. **Trigger the skill** — type `/idea-to-prototype` or describe your idea naturally:
   - "I want to build an app that helps people track habits"
   - "Help me design a mobile onboarding flow for a budgeting app"
   - "I have an idea for a tool that connects freelancers with clients"
   - "Create a design spec for a plant care reminder app"

2. **Answer 3 short questions** — Claude asks one at a time:
   - **Core objective:** What is the main goal of your product?
   - **Target users:** Who is this for?
   - **Platform:** Mobile, web, or desktop?

3. **Claude writes the spec** — you get a structured markdown doc with: problem statement, key screens, user flows, and component notes

4. **Paste into your prototyping tool** — copy the spec into Figma Make, v0, Stitch, or Pencil and generate clickable screens from it

5. **Iterate** — refine the spec in conversation and re-paste to update the prototype

## Requirements

- [Claude Code](https://claude.ai/code)
- A rough product idea (one sentence is enough to start)
