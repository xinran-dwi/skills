Creator: Xinran Ma

More resources like this on: designwithai.co

# parallel-projects

## What it is

A setup skill for anyone running Claude Code on more than one project at the same time. Instead of cycling through terminal windows hunting for the one that paused on an approval prompt, you get a single dashboard showing every session and which one needs you, a notification when a session needs input or finishes, and the option to check in and reply from your phone when you step away. The dashboard and phone access are built into Claude Code. Notifications use a few lines of hooks in your `~/.claude/settings.json`, because Claude Code's built-in notification toggles didn't fire in testing. Nothing else gets installed.

## When to use it

- You have three Claude Code windows open and keep switching between them to find the one that's paused
- You want to be told when a long-running task finishes instead of checking on it
- You want to approve a tool call without being at your desk
- You're about to step away and want to keep steering a session from your phone
- You're setting someone else up to work across several projects at once

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/parallel-projects ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Run the skill** — type `/parallel-projects`. It checks your terminal and your Claude Code setup before recommending anything, and tells you plainly if part of the workflow won't work in your environment.

2. **Open the dashboard** — run `claude agents` in any terminal. Every Claude Code session on your machine appears in one list, grouped by state, no matter which project it belongs to. Sessions name themselves from the task you gave them. Press `Space` to peek at one's output, `Enter` to jump into it.

3. **Turn on notifications** — the skill adds hooks to `~/.claude/settings.json` that play one sound when a session finishes and a different one when it needs your input, so you can tell them apart without looking. It then runs a tiny background session to prove the hooks actually fire, rather than assuming. Optionally, it can also send the alerts to your phone through the free ntfy app. (It skips the `/config` notification toggles: in testing they never fired.)

4. **Connect your phone** — install the Claude app, sign in, then type `/rc` in any session you want reachable. That session shows up under the **Code** tab on your phone, where you can read output, answer permission prompts, and send new instructions.

5. **Walk away and come back** — there is only ever one session, running on your machine. Your phone is a second keyboard on it. Instructions you send from the phone run against your local files, and the same terminal window is waiting with all of it when you return.

## Requirements

- [Claude Code](https://claude.ai/code)
- A Pro, Max, Team, or Enterprise plan for the phone step — API key logins are not supported
- The Claude mobile app (iOS or Android) for the phone step
