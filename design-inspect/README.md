Creator: Xinran Ma | designwithai.co

_Disclaimer: It is a work-in-progress personal tool._

# design-inspect — how to use

**What it is:** Opens your running Next.js app with a click-to-edit inspect overlay — like Cursor's Design Mode. Click one or more elements on the page, type what you want changed, and Claude Code locates the exact JSX line and makes the edit.

## Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/design-inspect ~/.claude/skills/
```

Restart Claude Code.

## Use it

In Claude Code, type `/design-inspect` or say — e.g.

- "Open inspect mode"
- "I want to click the thing I want to change"
- "Design mode"
- "Let me point at an element"

## How it works

1. Claude confirms a Next.js dev server is running (or starts one)
2. Opens the app in your browser
3. An overlay appears — click `◎ Inspect Mode` in the bottom-right corner
4. Hover over any element to see a blue outline with its component name
5. Click elements to add them as chips (you can select multiple)
6. Type your change request in the popup and hit Enter or "Copy to clipboard"
7. Paste the payload back into Claude Code — it locates the exact JSX and makes the edit

## Optional: Auto-load the overlay

Install the included userscript (`userscript.user.js`) in a browser extension like Tampermonkey. The overlay will then auto-load on every `localhost` page — no manual paste needed.

## Requirements

- [Claude Code](https://claude.ai/code)
- A Next.js project with `next dev` running
