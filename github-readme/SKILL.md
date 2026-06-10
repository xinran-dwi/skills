---
name: github-readme
description: Write a README.md for a new Claude Code skill using Xinran's standard format — creator header, What it is, When to use it, and step-by-step How to use it sections. Use this whenever the user wants to document a new skill, says "write a README for this skill", "create a readme for X skill", or invokes /github-readme.
---

# GitHub README

Write a README.md for a new Claude Code skill using the standard format established across Xinran's skill library at github.com/xinran-dwi/skills.

## Step 1 — Gather input

Determine what you're working from. In order of preference:

1. **Existing SKILL.md** — if the user points at a SKILL.md file or a skill directory, read it. The `description` frontmatter field and the body steps are your primary source of truth.
2. **User description** — if no SKILL.md exists yet, ask the user:
   - What does the skill do? (one sentence)
   - What phrases or situations should trigger it?
   - What are the steps to use it?
   - What are the requirements?

Don't ask more than necessary. If the SKILL.md is thorough, derive everything from it without asking.

## Step 2 — Write the README

Use this exact template. Do not deviate from the structure or heading levels.

```markdown
Creator: Xinran Ma

More resources like this on: designwithai.co

# <skill-name>

## What it is

<2–3 sentences. What the skill does and the core problem it solves. No bullet points here — prose only.>

## When to use it

- <specific trigger situation, written as a "you" statement>
- <specific trigger situation>
- <specific trigger situation>
- <specific trigger situation>
- <specific trigger situation>

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/<skill-name> ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **<Step name>** — <what the user does and what happens>

2. **<Step name>** — <what the user does and what happens>

3. <continue for all meaningful steps>

## Requirements

- [Claude Code](https://claude.ai/code)
- <any other hard requirements>
```

## Formatting rules — follow these exactly

These rules exist because GitHub Markdown collapses adjacent lines and renders bold inline text differently from headings. Breaking them causes the rendered page to look wrong.

1. **Blank line between the two header lines.** `Creator: Xinran Ma` and `More resources like this on: designwithai.co` must have a blank line between them — otherwise they render as one paragraph on GitHub.

2. **`## What it is` is a heading, not bold text.** Write `## What it is` on its own line, not `**What it is:**` inline. This gives it the same visual weight as `## When to use it` and `## How to use it`.

3. **All section headings are `##`.** `What it is`, `When to use it`, `How to use it`, `Requirements` are all `##`. Sub-sections under "How to use it" (`Install`, `Step by step`) are `###`.

4. **No disclaimer line** unless the skill is experimental or unfinished — in that case add `_Disclaimer: Work-in-progress personal tool_` after the header block and before the title.

5. **"When to use it" bullets are "you" statements.** Each bullet describes a situation the reader self-identifies with. Not "the skill does X" — "You want to X" or "You're doing X and Y".

6. **Step names in "Step by step" are bold.** Use `1. **Step name** — description` format. The name should be 2–4 words.

7. **Install command always uses the same pattern** — `git clone https://github.com/xinran-dwi/skills.git` then `mv skills/<skill-name> ~/.claude/skills/` then `Restart Claude Code.`

8. **No trailing content** after Requirements. Don't add notes, tips, or extra sections.

## Step 3 — Write the file

Write the README to `README.md` inside the skill's directory. If the skill directory doesn't exist yet, write it wherever makes sense and tell the user where it landed.

Confirm in one line: the file path written and a one-sentence summary of what the README covers.
