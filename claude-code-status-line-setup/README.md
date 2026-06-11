Creator: Xinran Ma

More resources like this on: designwithai.co

# claude-code-status-line-setup

## What it is

A one-time setup skill that installs a custom 4-line footer in Claude Code. The footer shows your current folder, git branch, active model, context window usage, and live 5-hour and 7-day plan limits with exact reset times — all pulled from Anthropic's usage API and cached locally so it stays fast.

## When to use it

- You want to see your Claude plan usage at a glance without opening a browser
- You're hitting rate limits and want to know exactly when your quota resets
- You want your context window percentage always visible in the footer
- You want the current git branch and model name in the status bar without switching windows
- You're setting up a new machine and want to replicate your Claude Code footer

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/claude-code-status-line-setup ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Invoke the skill** — Type `/claude-code-status-line-setup` or say "set up my status line"

2. **Claude detects your OS** — It writes the right script for your platform: a bash script on macOS/Linux, a PowerShell script on Windows

3. **Script is installed** — The script lands at `~/.claude/statusline-command.sh` (or `.ps1` on Windows) and is made executable automatically

4. **settings.json is updated** — Claude merges the `statusLine` config into your existing `~/.claude/settings.json` without touching your other settings

5. **Restart Claude Code** — The 4-line footer appears immediately on next launch

## What the footer looks like

```
📂 my-project  |  🌿 Branch: main (2)  |  ★ Claude Sonnet 4.5
Context: ████████░░░░░░░  52%
5h: ██████░░░░  61%  resets 1:00 am
7d: ███░░░░░░░  32%  resets jun 18, 5:00 pm
```

## Requirements

- [Claude Code](https://claude.ai/code)
- Active Claude.ai subscription (for 5h/7d usage bars — free tier shows `—`)
- macOS: usage bars work out of the box via Keychain
- Linux: usage bars show `—` (no Keychain equivalent); folder, branch, model, and context % still work
- Windows: usage bars are best-effort — depends on Claude storing the token at `%APPDATA%\Claude\credentials`
