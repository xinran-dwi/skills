Creator: [Vercel](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md)

More resources like this on: designwithai.co

# find-skills

## What it is

Searches the open skills ecosystem ([skills.sh](https://skills.sh/)) to find a Claude Code skill that matches what you need — so you don't have to build everything from scratch.

## When to use it

- You're about to ask Claude to do something and wonder "is there already a skill for this?"
- You ask "how do I do X?" and X might be a common task with an existing solution
- You want to discover installable skills for design, testing, deployment, documentation, or other domains
- You want to extend Claude Code's capabilities without writing a skill yourself
- You say things like "find a skill for X", "is there a skill that can...", or "I wish Claude could help me with Y"

## How to use it

### Install (one time)

**macOS / Linux**
```bash
mkdir -p ~/.claude/skills/find-skills
curl -fsSL https://raw.githubusercontent.com/xinran-dwi/skills/main/find-skills/SKILL.md -o ~/.claude/skills/find-skills/SKILL.md
```

**Windows (PowerShell)**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills\find-skills"
Invoke-WebRequest "https://raw.githubusercontent.com/xinran-dwi/skills/main/find-skills/SKILL.md" -OutFile "$env:USERPROFILE\.claude\skills\find-skills\SKILL.md"
```

Restart Claude Code.

### Step by step

1. **Trigger the skill** — type `/find-skills` or ask naturally:
   - "Find a skill for writing tests"
   - "Is there a skill that can help with React animations?"
   - "What skills exist for deployment?"
   - "How do I do X?" (Claude will check if a skill exists for it)

2. **Claude searches** — it checks the [skills.sh leaderboard](https://skills.sh/) for relevant skills matching your query

3. **Results are presented** — you see the skill name, what it does, install count, and the install command

4. **Read before you install** — skills are created by the community, so always read the skill description and its `SKILL.md` before installing. Don't install blindly — check what it does and whether it matches what you need.

5. **Install if it looks good** — run `npx skills add <package>` to install the skill globally

6. **Use it immediately** — restart Claude Code and the skill is available as a slash command

## Requirements

- [Claude Code](https://claude.ai/code)
- Node.js (for `npx skills` commands)
