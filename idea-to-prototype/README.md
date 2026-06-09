Creator: Xinran Ma | designwithai.co

# idea-to-prototype — how to use

**What it is:** Turns a rough product idea into a structured design spec (markdown) ready to paste into a prototyping tool — Figma Make, v0, Stitch, Pencil, or similar. Bridges the gap between "I have an idea" and "I have something to show."

## Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/idea-to-prototype ~/.claude/skills/
```

Restart Claude Code.

## Use it

In Claude Code, type `/idea-to-prototype` or say — e.g.

- "I want to build an app that helps people track habits"
- "Help me design a mobile onboarding flow for a budgeting app"
- "I have an idea for a tool that connects freelancers with clients"
- "Create a design spec for a plant care reminder app"

## How it works

1. Claude asks you 3 short questions: core objective, target users, and platform
2. Based on your answers, it generates a structured design spec in markdown
3. The spec includes: problem statement, key screens, user flows, and component notes
4. Paste the spec directly into your preferred prototyping tool to generate a visual prototype

## Requirements

- [Claude Code](https://claude.ai/code)
- A rough product idea (one sentence is enough to start)
