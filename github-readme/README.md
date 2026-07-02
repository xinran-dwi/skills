Creator: Xinran Ma

More resources like this on: designwithai.co

# github-readme

## What it is

Writes a `README.md` for a new Claude Code skill using the standard format established across Xinran's skill library. Give it a SKILL.md or describe the skill in words, and it produces a properly formatted README — creator header, What it is, When to use it, and step-by-step How to use it — ready to push to GitHub.

## When to use it

- You've built a new skill and need a README to go with it
- You want to document an existing skill whose README is missing or inconsistent with the rest of the library
- You say things like "write a README for this skill", "create a readme for X", or "document this skill"
- You want the README to match the format of the other skills at github.com/xinran-dwi/skills without doing it manually
- You're adding a skill to GitHub and want the page to look consistent with the rest of the library

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git /tmp/xinran-skills
mkdir -p ~/.claude/skills
mv /tmp/xinran-skills/github-readme ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Trigger the skill** — type `/github-readme` or ask naturally:
   - "Write a README for this skill"
   - "Create a readme for the design-inspect skill"
   - "Document this new skill"

2. **Point at a SKILL.md or describe the skill** — if you have a `SKILL.md` already written, share the path. If not, describe what the skill does, when to use it, and the steps to use it in a sentence or two.

3. **Claude writes the README** — it follows the exact format used across the skills library: creator header on separate lines, `## What it is` as a heading, `## When to use it` with "you" statement bullets, and a numbered `### Step by step` section.

4. **README is saved** — written to `README.md` inside the skill's directory. Claude confirms the path.

5. **Push to GitHub** — commit and push the new file to `xinran-dwi/skills` to make it live.

## Requirements

- [Claude Code](https://claude.ai/code)
