Creator: Xinran Ma

More resources like this on: designwithai.co

_Disclaimer: Work-in-progress personal tool_

# handoff

**What it is:** Pick up any project in 30 seconds. At the end of a session, `/handoff` saves a `HANDOFF.md` to your project capturing what you were building, what failed, next steps, and key files. Next session, Claude reads it, summarizes the state, and starts your dev server automatically.

## When to use it

- You're wrapping up a session and want to preserve context for next time
- You're starting a new session and want to get oriented fast without re-explaining everything
- You're coming back to a project after days away and can't remember where you left off
- You're cold-starting an unfamiliar project and want a quick lay of the land
- You want a human-readable project summary that works across machines and doesn't depend on Claude's session memory

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/handoff ~/.claude/skills/
```

Restart Claude Code.

### Step by step

**At the end of a session — save your place:**

1. Type `/handoff` (or say "save handoff", "wrap up")
2. Claude writes `./HANDOFF.md` in your project root with: what's being built, approaches tried (including failures), next steps, key file paths, and open questions
3. Commit it to git so it travels with the project

**At the start of a session — resume from file:**

1. Say "pick up where I left off", "resume handoff", or "where was I"
2. Claude reads `HANDOFF.md`, summarizes the state in 2–3 sentences, and starts your dev server
3. It asks where you want to start — top next step or something else

**Cold start — no HANDOFF.md yet:**

1. Say "get me up to speed", "cold start", or "what was I working on"
2. Claude reads your git log, README, and config files to piece together what the project is
3. It starts the dev server, summarizes the project, and offers to create a `HANDOFF.md` for future sessions

### How it differs from `/resume`

| | `/resume` (built-in) | `/handoff` (this skill) |
|---|---|---|
| Restores | Full conversation transcript | Curated 1-page project state |
| Stored in | Claude's internal session store | `HANDOFF.md` in your repo |
| Works on another machine | No | Yes |
| Captures failed approaches | Buried in conversation | Dedicated section |
| Dev server startup | No | Auto-detected and started |
| Human-readable without Claude | No | Yes |

## Requirements

- [Claude Code](https://claude.ai/code)
