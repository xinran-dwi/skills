Creator: Xinran Ma | designwithai.co

_Disclaimer: Work-in-progress personal tool._

# handoff

Pick up any project in 30 seconds. At the end of a session, `/handoff` saves a `HANDOFF.md` to your project capturing what you were building, what failed, next steps, and key files. Next session, Claude reads it, summarizes the state, and starts your dev server automatically.

## Requirements

- [Claude Code](https://claude.ai/code)

## Install (one time)

Open Terminal and run:

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/handoff ~/.claude/skills/
```

Restart Claude Code.

## How to use

### End of session — save your place

```
/handoff
```

Writes `./HANDOFF.md` in your project root with: current work, approaches tried (including failures), next steps, key file paths, and open questions.

### Start of session — resume from file

```
Read ./HANDOFF.md and continue from there
```

or say: `resume handoff`, `where was I`, `pick up where I left off`

Claude summarizes the state, starts the dev server, and asks where to begin.

### New project — cold start (no HANDOFF.md yet)

```
get me up to speed
```

or say: `cold start`, `what was I working on`, `what's this project`

Claude reads your git log, README, and config files, starts the dev server, and offers to create a `HANDOFF.md` for future sessions.

## How it differs from `/resume`

| | `/resume` (built-in) | `/handoff` (this skill) |
|---|---|---|
| Restores | Full conversation transcript | Curated 1-page project state |
| Stored in | Claude's internal session store | `HANDOFF.md` in your repo |
| Works on another machine | No | Yes |
| Captures failed approaches | Buried in conversation | Dedicated section |
| Dev server startup | No | Auto-detected and started |
| Human-readable without Claude | No | Yes |
