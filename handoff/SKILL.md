---
name: handoff
description: Save and restore project context between Claude Code sessions. Invoke when the user says "/handoff", "save handoff", "update handoff", or wants to wrap up / end a session. Also invoke when the user wants to resume or get oriented: "read handoff", "continue from handoff", "Read ./HANDOFF.md and continue from there", "where was I", "pick up where I left off", "get me up to speed", "what was I working on", "cold start". Works in three modes — Write (saves current session state to HANDOFF.md), Resume (reads existing HANDOFF.md and starts dev server), Cold start (no HANDOFF.md exists, explores project via git log and config files then starts dev server).
---

## Mode Detection

First, determine which mode applies:

- User triggered write mode (`/handoff`, "save handoff", "update handoff", "wrap up") → **Write mode**
- `./HANDOFF.md` exists and user wants to resume → **Resume mode**
- `./HANDOFF.md` does not exist and user wants orientation → **Cold start mode**

---

## Write Mode

1. **Detect the dev server startup command** by checking in order:
   - `package.json` → `scripts.dev`, then `scripts.start`, then `scripts.serve`
   - `Makefile` → look for a `dev`, `start`, or `serve` target
   - `docker-compose.yml` → note the relevant service and command
   - `pyproject.toml` → common Python server patterns
   - If nothing found, write `N/A`

2. **Gather context from the current session** — scan the conversation to identify:
   - The main thing being worked on right now
   - What was tried, especially failures (this is the most valuable section)
   - What remains to be done
   - Files that were touched or are central to the work
   - Unresolved decisions or open questions

3. **Write `./HANDOFF.md`** using this exact template:

```markdown
# Handoff — [project name] — [YYYY-MM-DD]

## Dev server
[startup command, or N/A]

## What I'm currently working on
[2-4 sentences on the active task and its goal]

## Approaches already tried and their results
- [bullet list — include failures, this section is the most valuable part]

## Next steps
1. [most important first]
2.
3.

## Key file paths
[relative/path/to/file — one-line description]

## Open questions
- [unresolved decisions that need attention next session]
```

4. Confirm in one line: `Handoff saved → next session: "Read ./HANDOFF.md and continue from there"`

---

## Resume Mode

Triggered when `./HANDOFF.md` exists and the user wants to continue.

1. Read `./HANDOFF.md`
2. Summarize the state in 2-3 sentences: what's being built, where it stands, what's next
3. If the dev server command is not `N/A`, start it immediately in the background via Bash. Tell the user it's running and on which port.
4. State the top next step and ask: "Want to start there, or is there something else first?"

---

## Cold Start Mode

Triggered when `./HANDOFF.md` does not exist and the user wants orientation.

1. **Gather project context** (run in parallel where possible):
   - `git log --oneline -30` to understand recent work (skip if no git repo)
   - Read `README.md` if present
   - Read `package.json`, `pyproject.toml`, `Cargo.toml`, or `go.mod` for project name and description
   - `find . -maxdepth 2 -type f -name "*.md" | head -10` to find any other documentation

2. **Detect the dev server command** (same logic as Write mode)

3. **Start the dev server** in the background if found. If it fails, show the error and the command the user can run manually with `! <command>`.

4. **Summarize** in 3-5 sentences: what the project is, what was recently being worked on (from git log commits), and the most obvious next steps.

5. Offer: "No HANDOFF.md yet — want me to create one now to make future sessions faster?"
