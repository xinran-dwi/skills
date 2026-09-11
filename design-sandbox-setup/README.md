Creator: Xinran Ma

More resources like this on: designwithai.co

# design-sandbox-setup

## What it is

`design-sandbox-setup` scaffolds a small, disposable app built on your team's *real* design system, so designers, PMs, and engineers can prototype with an AI coding agent using actual production components instead of components the AI invented from memory. It's adapted from the workflow in ["How to build a design sandbox for your team to prototype with real code"](https://designwithai.substack.com/p/how-to-build-a-design-sandbox-for-your-team-to-prototype-with-real-code), turning that article's four core steps into a repeatable skill you can run against any design system and any codebase.

## When to use it

- You want a safe place to prototype UI without touching your production app, auth, or real data.
- Your AI coding agent keeps hand-rolling buttons, cards, or tables that look close to your design system but don't actually match it.
- You want an index (`COMPONENTS.md`) that tells an AI agent exactly which real component to use for a given job, and what not to build instead.
- You want an AI rules file that forces "check the real component first, then ask" instead of "guess and build something custom."
- You want to recreate one real production screen in isolation, using fake data, to iterate on design changes quickly.

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/design-sandbox-setup ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Describe your target** — tell Claude Code what you want, e.g. "set up a design sandbox for our design system" or "I want to prototype using our real components instead of made-up ones." No exact phrasing required — it also triggers on more literal asks like "stop Claude making up buttons that don't match our design system."

2. **Point it at your design system** — have ready either an npm package name, or a local folder/monorepo package path (e.g. `@repo/ui`). If you don't mention it, it will ask rather than guess.

3. **Phase 1 — components get set up** — it installs the design system as a package if possible, or falls back to copying component source, adopting shadcn/ui and theming it, or converting Figma designs to code — whichever actually applies to your setup. It verifies with one default-styled component before moving on.

4. **Phase 2 — it builds `COMPONENTS.md`** — a table of your ~20 most-used real components, each with what it's for, what it isn't, and the exact "wrong move → right move" swap for anything an AI might otherwise hand-roll.

5. **Phase 3 — it writes `CLAUDE.md`** — one hard rule: check `COMPONENTS.md` and the real component source before writing any UI, and stop and ask instead of inventing something custom. No exceptions for "simple" cases.

6. **Phase 4 — it recreates one core screen** — give it a path to an existing production app and a screen name, and it rebuilds that screen with real components and fake data only, no data-fetching or auth code included. No production app? Describe the screen instead and it builds from that.

7. **Keep iterating** — you end up with a standalone app you (or anyone on the team) can keep prototyping in with an AI agent, safely separated from production. Re-run the skill again later against a different design system or repo — it isn't hardcoded to any one.

8. **Check it against the real thing** — once Phase 4 is done, run the companion skill [`design-sandbox-verify`](../design-sandbox-verify/). It renders the real screen's current source live next to your rebuild and produces an itemized list of what's actually different — because a first pass usually looks about right without being right, and "about right" is what this whole sandbox exists to eliminate.

This version deliberately stops at those four phases — it does not build the article's optional chat panel/inspect tool/share features, the "Custom UI" escape hatch, or follow-on maintenance skills like `sandbox-check`. It was validated with a side-by-side eval (a real Untitled UI monorepo and a fresh shadcn/ui project): runs using this skill reliably produced the `COMPONENTS.md`/`CLAUDE.md` guardrail files that runs without it skipped entirely. See [`evals/`](./evals/) to run those yourself.

## Requirements

- [Claude Code](https://claude.ai/code)
- A design system to point it at (an installable package, or component source you can read)
