Creator: Xinran Ma | designwithai.co

_Disclaimer: It is a work-in-progress personal tool._

# find-skills — how to use

**What it is:** Searches the open skills ecosystem ([skills.sh](https://skills.sh/)) to find a Claude Code skill that matches what you need. Helps you discover installable skills for common tasks so you don't have to build everything from scratch.

## Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/find-skills ~/.claude/skills/
```

Restart Claude Code.

## Use it

In Claude Code, type `/find-skills` or ask naturally — e.g.

- "Find a skill for writing tests"
- "Is there a skill that can help with React animations?"
- "What skills exist for deployment?"
- "How do I do X?" (Claude will check if a skill exists for it)

## How it works

1. You describe what you're trying to do
2. Claude checks the [skills.sh leaderboard](https://skills.sh/) for relevant skills
3. If a match is found, it gives you the install command
4. You run `npx skills add <package>` to install

## Requirements

- [Claude Code](https://claude.ai/code)
- Node.js (for `npx skills` commands)
