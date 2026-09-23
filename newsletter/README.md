Creator: Xinran Ma

More resources like this on: designwithai.co

# newsletter

## What it is

Turns something you just built or tested into a finished Design with AI newsletter issue, written in your voice and aimed at designers who don't code. It ships the article as an HTML page with copy buttons that hand Substack clean, schema-correct markup, so headings, bold, quotes, numbered steps and images all survive the paste instead of arriving as a mangled draft you have to reformat by hand.

## When to use it

- You just finished building or testing something with AI and want to write it up
- You have a draft that reads too technical and needs to work for designers who don't code
- You want an article you can paste into Substack without losing the formatting
- You need the real token and time cost of an AI session, measured rather than estimated
- You're fixing an existing draft's voice so it sounds like the rest of your newsletter

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/newsletter ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Run it** — type `/newsletter` in the session where you did the work. It pulls the details from the conversation rather than interviewing you about something you both just watched happen.

2. **Confirm the audience** — the default is designers who use AI tools and have never written code. Every readability problem traces back to writing for engineers instead, so it checks before drafting.

3. **Get the real numbers** — if the piece covers an AI session, `scripts/session_stats.py` reads the transcript and reports per-task turns, tool calls, minutes and tokens. Nothing is estimated.

4. **Review the draft** — it follows a fixed running order: overview, setup early, what you did, how it works, what it cost, what you got wrong. Setup comes near the front on purpose, since a reader deciding whether to try something wants the cost of entry before the story.

5. **Open the paste page** — the article plus a small toolbar, written to `newsletter/substack-paste.html` next to your work. Renders are inlined as data URIs and the originals stay in `images/`.

6. **Copy into Substack** — click Copy for the title and subtitle, paste them into Substack's own fields, then click Copy article body and paste. Use the buttons rather than Cmd+A, which grabs the toolbar too.

7. **Publish the link** — the same page gets published as an artifact, so you have a link instead of a local file to hunt down next time.

## Requirements

- [Claude Code](https://claude.ai/code)
- Python 3 (for the session stats script)
- macOS for image resizing via `sips`, or any equivalent tool
