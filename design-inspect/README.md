Creator: Xinran Ma | designwithai.co

_Disclaimer: Work-in-progress personal tool

# design-inspect

Click any element in your running app, type what you want changed, and Claude Code finds the exact line and edits it — no describing elements in words.

## Requirements

- [Claude Code](https://claude.ai/code)
- A Next.js project running locally (`npm run dev` or similar)

## Install (one time)

Open Terminal and run:

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/design-inspect ~/.claude/skills/
```

Restart Claude Code.

## How to use

1. Make sure your app is running in the browser (e.g. `http://localhost:3000`)
2. In Claude Code, type `/design-inspect` (or say "inspect mode" / "design mode")
3. Claude opens your app and copies the overlay script to your clipboard
4. In the browser, open DevTools Console (⌥⌘J on Mac) → paste → Enter
5. Click **◎ Inspect Mode** in the bottom-right corner
6. Hover over elements to see a blue outline — click to select (you can pick multiple)
7. Type your change in the popup → hit Enter or **Copy to clipboard**
8. Paste back into Claude Code — it makes the edit

## Optional: skip the paste step

Install the included `userscript.user.js` in [Tampermonkey](https://www.tampermonkey.net/). The overlay will auto-load on every `localhost` page so you can skip steps 3–4 above.
