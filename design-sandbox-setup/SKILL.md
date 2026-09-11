---
name: design-sandbox-setup
description: Scaffold a code-based "design sandbox" on a REAL design system so designers/PMs can prototype with an AI agent using actual components, not AI-invented lookalikes. Four phases — install/copy the design system into a fresh app, build a COMPONENTS.md index ("wrong move → right move" guidance), write a CLAUDE.md rule forcing real-component checks before writing UI, and recreate one real screen with fake data. Works with any design system (npm package, monorepo source, or nothing installable) and any codebase — meant to be rerun on different design systems/repos. Use when the user wants to build a design sandbox or prototyping playground, prototype on a real design system, generate an AI component index, stop AI inventing components that drift from the design system, or wants this repeatable across repos — even unsaid, e.g. "mock up screens using our actual components" or "stop Claude making up buttons that don't match our design system."
---

# Design Sandbox Setup

## Why this exists

Production codebases are usually too complex and too gated (auth, permissions, data-fetching) for a designer or PM to safely poke at directly. Figma is safe to poke at, but it can't express real interaction, and it drifts from what the code actually looks like. A design sandbox splits the difference: a small, disposable app that uses the *real* design system components — not lookalikes an AI invented from memory — so anyone with an AI coding agent can explore real screens without touching production.

The single biggest failure mode this guards against is an AI coding agent quietly hand-rolling a `<div>` that looks like a button instead of using the design system's actual `Button`. Every phase below exists to make that mistake hard to make.

## Inputs

Gather these before starting. Don't ask for anything you can just find by looking at the working directory or the paths already given to you — only ask where genuinely ambiguous.

- **Target sandbox folder** — where the sandbox app will live. Default to the current directory if it's empty or clearly new; otherwise ask.
- **Design system** — an npm package name, or a local source/workspace path (e.g. a monorepo package like `@repo/ui`, or a folder of component source files). If you weren't told this and can't tell from the working directory, ask.
- **Production app + screen to recreate** (optional, needed for Phase 4) — a path to an existing app plus which screen to rebuild. If this wasn't given, you'll ask the user to describe the screen instead when you get to Phase 4 — don't skip the phase for lack of it.
- **Figma reference** (optional) — a Figma file/frame to validate against visually, if one exists.

## The discipline that makes this work

Test at roughly 80% through each phase, not once at the very end. A wrong component pick in Phase 1 or a vague row in Phase 2 compounds into every screen built afterward — catch it early, while it's still cheap to fix.

Everything below assumes `[design system]`, `[target folder]`, `[production app path]`, `[screen name]` etc. are the actual values you gathered above, not literal placeholders — by the time you write a file to disk, every path in it should be real.

---

## Phase 1 — Set up components

**Goal**: get the design system's real components rendering standalone in the target folder, so nothing downstream is guessing at what they look like.

First, work out whether the design system installs as its own package: look at `[design system]`'s setup instructions (its README, its `package.json`, or its docs) and determine whether it can be installed as its own package in a brand-new, empty project.

**If it can** — set up a new blank React app in `[target folder]` using Vite, frontend only, install `[design system package name]`, and delete the starter app's own default styling and placeholder page. Vite is the right default here because it's lighter than Next.js and this sandbox doesn't need server-side rendering; only reach for Next.js if the design system itself specifically depends on Next (server components, its own routing conventions, etc.) — that adds real complexity, so don't take it on for free.

**If it can't** — this is common; plenty of design systems (including source-available kits like Untitled UI React) are meant to be copied in, not installed. Don't guess which fallback applies — ask, unless it's already obvious from what you were told:
- Copy the ~20 most-used component source files into the sandbox (ask an engineer for help finding them if you're not sure which files matter).
- Use shadcn/ui as a base and theme it to match the product's design system.
- If only Figma designs exist and no real component code, use the Figma MCP to convert the designs to code first.

**Verify before moving on**: add a single button from the design system to the page, using its default look — nothing custom, nothing else on the page.

Then check it **automatically, against the design system's own token source** — not against its documentation, and not by eye. Docs and screenshots go stale; the installed package can't. Run the check yourself and report the result; it isn't homework for the user:

1. Render the page and read the button's real computed values — `backgroundColor`, `color`, `borderRadius`, `height`, plus the page background — via `getComputedStyle()`.
2. Convert each to the notation the design system stores (usually hex) and **grep the installed package for that literal value** to find the token it belongs to (e.g. `grep -rn '3d71d9' node_modules/<pkg>/…` landing on `blueDarkMain: "#3d71d9"`).
3. Report each as a pass only when a rendered value traces to a real named token. A value that appears nowhere in the package is the failure signal — it means something is falling back to a browser default or an unthemed stylesheet.

This is worth doing exactly rather than approximately, because "close enough" here is invisible and compounds: a missing theme provider, a stylesheet that never loaded, or a font that 404s will each produce a page that looks plausible and measures wrong. Every screen built afterward inherits it, and any later fidelity check is then measuring the wrong baseline.

If a value doesn't trace to a token, something is wrong with the install/copy — fix that now, before it's buried under three more phases of work built on top of it. Assets are the usual culprit: many design systems expect the host app to serve their icons and fonts, so check for 404s in the console before assuming the package is at fault.

---

## Phase 2 — Build the component index (`COMPONENTS.md`)

**Goal**: give yourself (and any future AI session working in this sandbox) a fast, accurate reference so you reach for the right real component instead of inventing one.

Read the design system's components at `[design system package name / folder path]` and, if a production app path was given, look through its important screens. Count roughly which components get used most. Take the top 20 and write a file called `COMPONENTS.md` at the root of the sandbox, containing a table with four columns: **Component**, **Import**, **Use for**, and **Wrong move → right move**.

- For **Use for**, write what the component is for, then the nearest thing it isn't — this matters most for components that overlap, where it'd be easy to pick the wrong one (e.g. a `Card`-like `Container` vs. an actual `Card`, or a `Table` vs. a `DataGrid`).
- For **Wrong move → right move**, name what might get built manually instead, paired with the exact real setting that replaces it. Check every setting you write down against the real component source — don't write a prop or variant name you haven't confirmed exists.
- If you can't tell which design system is in use, or a rule depends on team preference you can't read from the code, **don't guess — ask.** A wrong guess here poisons every screen built on top of it.

Before building this from scratch, check for a shortcut: does the team already have a current Storybook, or an existing component-usage guideline doc? If so, use it as a cleaner source than inferring everything from raw component code.

---

## Phase 3 — Write the AI rules file (`CLAUDE.md`)

**Goal**: make the Phase 2 index actually get used, automatically, on every future edit in this sandbox — not just this once.

Create a `CLAUDE.md` file at the root of the sandbox. Start with one rule: before writing any component code, read `COMPONENTS.md` to find the right component, then check that component's real source code (at its real, actual path in this project — fill in the real path now that you know it, don't leave a placeholder) to confirm the settings you're about to use actually exist. If nothing in the index fits, stop and ask instead of building something custom. This applies everywhere: no exceptions for simple cases, one-off tweaks, or quick fixes — the moment "just this once" is allowed, the sandbox stops meaning anything.

This file is meant to be revisited over time, not written once and forgotten — as gaps get discovered later (a legacy vs. new version of a component, a design-system quirk the index didn't capture), that's normal maintenance for whoever owns the sandbox, not something this setup pass needs to fully solve up front.

---

## Phase 4 — Recreate one core screen

**Goal**: prove the sandbox is actually useful by rebuilding one real, high-impact screen — not a full clone of the app, just enough to iterate on.

If a production app path and screen name were given: read the `[screen name]` page in the production app at `[production app path]`. Rebuild that screen in the sandbox using the design system's real components. Copy the layout, the columns, and the states. Do **not** copy anything that fetches data, checks permissions, or handles login — use fake data instead. This isn't just a shortcut; it's what keeps the sandbox safe for a non-engineer to poke at freely.

If no production app was given, ask the user to describe the screen instead of skipping this phase — the point is to end up with one real, working screen either way, not to make Phase 4 optional.

If a Figma reference or screenshots were supplied, iterate against those for visual accuracy; otherwise the production screen itself is the reference. Build progressively — get the layout solid before adding interaction states on top of it — and stop once it's good enough for the team to actually iterate on, not once it's a pixel-perfect full clone. That's a judgment call for whoever's running this, not something you can self-verify from code alone.

---

## Not covered by this skill (yet)

This skill deliberately stops after Phase 4 (the article's Steps 1–4). It does **not** build:

- An embedded AI chat panel, an inspect/click-to-reference tool, a variant switcher, or a share/tunnel feature (the article's Step 5 — optional UX helpers on top of the sandbox).
- A "Custom UI" escape-hatch toggle for when the design system genuinely can't support what's being explored (the article's Step 6).
- Meta-skills like `sandbox-check` or `index-audit` for verifying or maintaining a sandbox after it's built (the article's Step 7) — **except** fidelity-checking, which is now covered by the companion skill [[design-sandbox-verify]]: once Phase 4 is done, run it to check the recreated screen against the real thing (not just a screenshot) and close any gaps found.

That's a deliberate scope boundary, not an oversight — treat any of the above as a separate follow-up, not something to reach for mid-run here.
