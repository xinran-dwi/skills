---
name: parallel-projects
description: Set up a workflow for running Claude Code on several projects at once — one dashboard showing which session needs your input, notifications when a session needs approval or finishes, and the ability to check in and reply from your phone. Use when someone is juggling multiple Claude Code windows, keeps switching terminals to find which one is paused, wants to be told when a long task finishes, wants to steer a session while away from their desk, or asks things like "which window needs me", "too many terminal windows", "can I check Claude from my phone", or "how do I run several projects at once". Also triggers on /parallel-projects.
---

# Running Claude Code on several projects at once

Everything here is **built into Claude Code**. Nothing gets installed, no scripts, no
config files to maintain. The whole workflow is three things:

```
claude agents         one dashboard for every project
/config  (once)       get told when a session needs you or finishes
/rc      (per window) put this session on your phone
```

None of it is per-project. The notification settings are user-level, so they apply to every
project you ever open — including ones that don't exist yet. `claude agents` is machine-wide
and picks up sessions in any directory automatically. The only per-session action is `/rc`.

## Important: you cannot type slash commands for the user

`/config`, `/rc`, and `/mobile` are interactive commands in the user's own session. You cannot
run them. Your job is to **check their environment, tell them exactly what to type, and verify
the result afterward**. Never claim to have configured something you only recommended.

---

## Step 1 — The dashboard

Tell the user to run this in any terminal:

```bash
claude agents
```

It lists every Claude Code session on the machine, grouped by state, regardless of which
project each one is in. Sessions name themselves from the task they were given.

States shown: **Working** (animated), **Needs input** (yellow — waiting for approval or an
answer), **Idle**, **Completed**, **Failed**, **Stopped**.

Keys: `↑`/`↓` move · `Space` peek at output without leaving the dashboard · `Enter` or `→`
attach · `Ctrl+T` pin a session so its process isn't reclaimed · `Ctrl+X` stop · `?` all shortcuts.

For scripting or for checking state yourself, use:

```bash
claude agents --json
```

It returns `{sessionId, cwd, name, status}` per session. Status values: `busy`, `waiting`
(this is what the dashboard shows as "Needs input"), `idle`, `completed`, `blocked`, `paused`.

Sessions can be started detached so they show up here without occupying a window:

```bash
claude --bg "the task"     # then: claude attach <id> / logs <id> / stop <id>
```

**Say this plainly:** Agent View is a **research preview** — its interface and keyboard
shortcuts may change in future versions.

---

## Step 2 — Notifications

First detect the terminal, because the notification channel depends on it:

```bash
echo "$TERM_PROGRAM"
```

- `iTerm.app`, WezTerm, Ghostty, Kitty → recommend **`iterm2_with_bell`** (rich notification + bell)
- `Apple_Terminal` or anything else → **`terminal_bell`** is what will work; a macOS banner is
  not available on Apple Terminal. Mention that phone push (Step 3) is the dependable signal
  for them, and that switching terminals is optional, not required.

Then tell the user to run `/config` and turn on:

- **input needed** — fires when a session is waiting for approval or an answer
- **task complete** — fires when a turn finishes

Afterward, verify rather than assume:

```bash
jq '{inputNeededNotifEnabled, taskCompleteNotifEnabled, preferredNotifChannel, agentPushNotifEnabled}' ~/.claude/settings.json
```

Then **test it for real** — start a background session that parks on a question and confirm
something actually fired. Report what you observed, not what was configured.

---

## Step 3 — The phone

This one has a real tradeoff. **State it before recommending it**, not after.

### What it does

`/rc` (or `/remote-control`) connects the session to the Claude mobile app and claude.ai/code.
There is still only **one session**, running on the local machine. The phone is a second
keyboard on it: instructions sent from the phone are executed by the local process against the
local files, and the terminal window updates live. Walk back to the desk and the same window
has everything. Nothing to merge or pull down.

From the phone you can read output, answer permission prompts, send new instructions, and
attach photos.

### What the user is opting into

- **Privacy:** while Remote Control is connected, the session transcript — messages, replies,
  tool activity — is stored on Anthropic servers. That storage is *how* the sync works. A plain
  local session never sends that text. Code execution and file access stay local either way.
- **Security:** their claude.ai account becomes a way to run commands on their machine. Trusted
  Devices (biometric step-up) is Team/Enterprise only, so on a personal plan **account 2FA is
  the real control**. `disableRemoteControl` in settings.json is a hard off switch.
- **Scope:** opt-in per session. Nothing is reachable until they type `/rc` in that window, and
  it stops being reachable when the session ends. Do not recommend `remoteControlAtStartup`
  unless they ask — always-on is a bigger commitment than the problem requires.

### Check eligibility first

Remote Control will not work in these cases — check before walking them through setup:

```bash
for v in DISABLE_TELEMETRY DO_NOT_TRACK CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC \
         DISABLE_GROWTHBOOK ANTHROPIC_BASE_URL CLAUDE_CODE_USE_BEDROCK CLAUDE_CODE_USE_VERTEX; do
  printf '%-45s %s\n' "$v" "${!v:-<unset>}"
done
jq -r '.disableRemoteControl // "not set"' ~/.claude/settings.json
```

- Any of the first four set → disables the feature-flag evaluation Remote Control depends on.
  Unset it in the shell **and** in the `env` block of settings.json.
- `ANTHROPIC_BASE_URL` pointing anywhere but `api.anthropic.com`, or Bedrock / Vertex /
  Foundry → not supported.
- Requires a Pro, Max, Team, or Enterprise login. **API keys are not supported.**
- On Team/Enterprise, an Owner must enable the Remote Control toggle in admin settings first.

### Setup

Tell the user to do this once:

1. Install the Claude app (iOS/Android). `/mobile` in Claude Code shows a QR code.
2. Sign in with the same account. Confirm 2FA is on first.
3. Accept the OS notification permission prompt.
4. `/config` → enable **Push when Claude decides** and/or **Push when actions required**.
5. In whichever session they want reachable: `/rc`. The terminal prints a session URL.
6. On the phone: **Code** tab → the session appears with a computer icon and a green dot.

Troubleshooting: if `/config` says **No mobile registered**, opening the app once refreshes its
push token. On iOS, Focus modes and notification summaries can suppress pushes — check
Settings → Notifications → Claude.

Note that push is deliberately skipped while they're focused on the connected terminal, so
"no notification while I was sitting there" is correct behavior, not a fault.

---

## Things worth telling them

- **Each session uses subscription quota independently.** Three projects in parallel burns
  roughly three times as fast. This is the real cost — not CPU.
- **Sessions idle for about an hour** have their process stopped to free resources. The
  conversation survives; replying or attaching resumes it. `Ctrl+T` pins one to keep it alive.
- **Background sessions that edit files** move into isolated git worktrees (`.claude/worktrees/`)
  so parallel sessions don't collide. Deleting such a session from the dashboard **deletes its
  worktree, including uncommitted changes** — use `claude rm` to keep them. Sessions that only
  read files don't create a worktree at all. Set `worktree.bgIsolation: "none"` to turn it off.

## Adjacent things, if they ask

`/loop` (run a task on a repeating interval) · `--teleport` (pull a cloud session down into the
terminal) · cross-session messaging: `/list-agents`, `@session-name`, `/notify_when_idle`.
