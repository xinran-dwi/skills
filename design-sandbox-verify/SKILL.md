---
name: design-sandbox-verify
description: Check a hand-built or AI-rebuilt UI screen (especially from design-sandbox-setup) against the REAL thing it resembles, find concrete gaps, and fix them. When the original is running code, fetches its current component source read-only and renders it live in a throwaway harness fed the sandbox's own fake data — not a screenshot, which can be stale. When the original is a design export (a Figma frame, a PNG spec), measures that export instead — color-managed sampling and design-pixel rects, never eyeballed values. Compares rendered screenshots, source (markup AND the styling layer), and measured geometry and color, so a rebuild that copies a component's structure but drops its CSS — or repaints it in colors that merely look close — gets caught. Produces an itemized FIDELITY_REPORT.md (missing real elements, invented elements, wrong-component swaps, dropped styling, wrong values), auto-fixes small unambiguous gaps, asks before bigger scope additions. Use whenever the user says a rebuilt screen "looks different" from the original, asks to check or verify fidelity against the real UI or against a design, wants a sandbox screen made closer to what it's based on, or wants to confirm an AI-recreated screen truly matches its reference rather than just looking plausible — even unsaid, e.g. "these look different, fix it", "make this match the real app", or "the colors are off from the Figma."
---

# Design Sandbox Verify

## Why this exists

A screen rebuilt from a screenshot or from memory drifts from reality in ways that are easy to miss just by eyeballing it once: a screenshot can be months stale while the real component moved on, and "looks about right" hides specific, fixable mistakes — a whole missing element, an invented one that was never real, or a real component used in the wrong spot. This skill exists to replace "looks about right" with a real side-by-side check against the actual current thing, and a concrete list of what to fix.

There's a second, subtler failure this skill has to defend against, because it's the one a careless run produces: checking the rebuild at the level of *which component and which props* and stopping there. That check passes easily — the components genuinely are right — while the real file's styling layer never made it across, and the two screens still look plainly different to anyone who opens them. **A verification pass that never compares the two renders and never measures anything hasn't verified anything.** Phases 2 and 4 exist in their current form specifically to make that failure impossible to reach.

There's a third failure, and it is the one a *diligent* run produces: measuring the dimension that is easy to measure, judging the rest by eye, and reporting the whole thing as verified. Geometry submits to `getBoundingClientRect()`, so geometry gets checked. Color doesn't, so color gets eyeballed — and eyes are near-useless at it: `#0a0e41` and `#050a36` both read as "dark blue" when you flip between two screenshots, while looking plainly different to whoever opens the build next to the original. **Color is a measurement, not an impression.** Phase 2c says so, and the design-export path ships a tool for it.

This skill has two ground-truth paths, because the original is either executable or it isn't. When it's running code, the whole file below applies. When it's a fixed design export — a Figma frame, a PNG spec — Phase 1 and Phase 2 are replaced by [`references/design-export.md`](references/design-export.md); every other phase here still applies unchanged.

This is the natural follow-up to [[design-sandbox-setup]] — that skill builds the first pass of a screen; this one checks it against reality and tightens it. Run it any time a sandbox screen was built from a screenshot, from memory, or a while ago and might have drifted.

## Inputs

- **Sandbox folder** — the screen to check, usually a `design-sandbox-setup` output. Needs its own dev server you can point a browser at.
- **What it's supposed to resemble** — either where the real target's actual component source lives (a public repo, an npm package, a local codebase) and which real screen, or, if the original is a design rather than a product, the export file itself. If this isn't given and isn't obvious from the sandbox's own comments/`COMPONENTS.md`, ask rather than guess at what it was based on.

  A reference you can't immediately find is not a reference that doesn't exist. Pasted images are cached on disk by the harness (Claude Code: `~/.claude/image-cache/<session-id>/`), exports sit in download and handoff folders, and the user can hand you the file. Search, then ask. Declaring the check blocked and estimating values instead is the failure this skill exists to prevent, not a way of coping with it.

The sandbox's own existing fake data (whatever it already uses) gets reused for the ground-truth render too — never invent new fake data for this check. If the two sides show different data, any visual difference you find is ambiguous: is it a real gap, or just different content? Keeping data identical is what makes the comparison mean something.

---

## Phase 1 — Establish ground truth

**Goal**: get the real screen actually rendering somewhere you can look at it, as close to "the real thing, right now" as possible — not a description of it, not a guess at it, not last year's picture of it.

**First, which kind of original is this?** If it's a fixed design export — a Figma frame, a PNG spec, a handoff image — stop here and follow [`references/design-export.md`](references/design-export.md) for Phases 1 and 2, then come back for Phase 3 onward. There the export *is* the spec, so it gets measured rather than treated as a lossy picture of something better, and the mechanics are different enough (color profiles, artboard scale, pixel sampling) to need their own page. The ladder below is for an original that is running code.

Try these in order, because each one down this list trades accuracy for convenience:

**a) Preferred — build a real-source harness.** If the real target's component source is inspectable at all (even read-only, even in a huge monorepo you'd never want to fully clone), this is worth the extra effort because it's the only option that's guaranteed current:

1. Fetch the real, current component files for that screen — individual files via `gh api repos/<org>/<repo>/contents/<path>` (or the raw file URL), not a full `git clone` of a large repo. Save them unmodified.
2. Stand up a minimal throwaway app (a fresh Vite + React app is usually the fastest) in a **separate folder** from the sandbox being checked. Place the fetched files at the same relative paths their own internal imports expect, so their `import`s resolve without editing them.
3. Those real files will depend on a few things that only exist inside a fully running instance of the real product — an internal app-context hook, an i18n hook, routing, maybe more. Write the smallest possible mock for exactly what those specific files call (nothing more), and wire it in via whatever mechanism keeps the real files untouched — a matching relative path for a relative import, or a bundler alias (e.g. Vite's `resolve.alias`) for a package import like `react-i18next`.
4. Feed the mock's data-fetching call the sandbox's own existing fake data, reshaped into whatever data shape the real files expect. If the real screen has interactive actions (a toggle, a delete), wire the mock so they actually mutate that data and the screen visibly reacts — a real comparison needs both sides to actually work, not just render once statically.
5. Run this harness on its own dev-server port, separate from the sandbox's own port.

The one rule that makes this whole technique trustworthy: **never edit the real fetched files.** If something needs to change to make it render, that change belongs in your mock or wrapper layer. The moment you start patching the real files to make them behave, they stop being ground truth and you're back to guessing.

**b) Fallback — a live public demo.** If the real source isn't practically renderable this way (it's not open, or it's too deeply coupled to infrastructure you can't stand up), and the real product has a public demo, use that instead. Never submit a signup or lead-gen form, provide an email, or enter credentials on the user's behalf to reach it — if that's the only way in, stop and ask the user to either do it themselves or share a way in.

**c) Last resort — a real screenshot.** Prefer one sourced from the product's own current docs or marketing over a random third-party post, and explicitly flag it in your output as a screenshot (not a live render) with whatever date info you can find — treat it as possibly stale, because it might be. This is strictly worse than (a) or (b): a stale screenshot is exactly what caused the original mismatch this skill exists to catch.

---

## Phase 2 — Structured discrepancy pass

**Goal**: turn "these look different" into a concrete, itemized list — vague visual impressions don't tell you what to fix.

With ground truth running on its own port and the sandbox on its own, work through both. Don't scan the whole screen at once and call it "close" or "off." Walk it region by region instead: the top-level layout containers first (is there a sidebar, a header, a toolbar the other side doesn't have?), then each distinct interactive control within them (is this filter row the same kind of control on both sides? does this card's footer have the same actions?).

### Do all three passes — they catch different things

**a) The render pass.** Screenshot both sides at the same viewport and compare the images. This is not optional and not satisfied by a glance: flip between the two screenshots in place rather than scanning them side by side, because a difference that's invisible when your eye travels between two images jumps out when one swaps under a fixed cursor.

**b) The source pass — read the styling layer, not just the JSX.** When you open a real component file, its element tree and props are only half of it. The other half is whatever visual layer it carries: a CSS-in-JS block (`css`/`styled`/emotion), a `className`, `style`/`styles` overrides, a companion `.css`/`.scss` file, theme-token spacing. **Diff that layer explicitly, line by line, the same way you diff the markup.** Copying a real component's structure while dropping its styling is the single easiest way to produce a rebuild that passes a props check and still looks obviously wrong — the components are right, the props are right, and every card still renders a divider the real one doesn't have.

Two specifics that hide well and are worth grepping for on both sides:
- Rules targeting the design system's own internal class names (`.ant-card-body`, `.ant-card-actions li:first-child`, etc.). These do heavy layout work — equal heights, cell widths, suppressed borders — and vanish silently when only the JSX gets copied.
- Hardcoded numbers on the sandbox side where the real source reads a theme token. `gap: 16` vs `gap: token.margin` may render identically today and drift the moment the theme changes.

If the sandbox can't use the real file's styling mechanism (no emotion installed, say), port the rules to one it does have and say so in the report — don't silently drop them.

**c) The measurement pass.** Impressions plateau; numbers don't. For the handful of elements that matter most on the screen, read actual computed geometry and styles on both sides — via the browser tools, e.g. `getBoundingClientRect()` and `getComputedStyle()` — and compare the numbers:

- widths and heights of the repeated element (cards, rows, list items), including whether siblings in a row are equal height
- x/y origins of the main containers, to catch offsets
- the specific properties you just fixed or suspect: `borderBottomWidth`, cell widths inside a footer, padding
- **color, always, and numerically.** Read the actual `backgroundColor` / `color` off both sides and compare the values; never settle it by flipping between screenshots. Near-identical dark surfaces are invisible to the eye and obvious to a subtraction. If one side is a design export rather than a DOM, sample it with `scripts/measure-ref.py compare`, which prints per-channel deltas and exits non-zero past a tolerance.

Record the numbers in the report. "Card width 317px vs 317px" is checkable by the next person; "looks the same now" isn't.

### Sort what you find

Write it to `FIDELITY_REPORT.md` at the sandbox's root, sorted into four kinds of gaps:

1. **Missing** — a real element the rebuild doesn't have at all.
2. **Invented** — something in the rebuild that isn't actually part of the real screen (often the fingerprint of a stale screenshot or a guess that didn't pan out). Watch for the tell where an invented element exists to compensate for a dropped one — a hand-added 1px border standing in for a background the real screen has, say. Fix the cause, not the symptom.
3. **Wrong mapping** — a real component was used, but the wrong one for this spot, or hand-rolled markup stands in where a real component should be. Same spirit as the `Wrong move → right move` column in the sandbox's own `COMPONENTS.md` — name the wrong thing and the exact real replacement.
4. **Styling dropped** — the right component with the right props, but the real file's visual layer didn't come across. Name the specific rules that went missing, not just "styling differs."

### Know what's out of scope before you call it a gap

The harness renders only the real files you fetched. Anything outside them — app shell, nav bar, page title, surrounding layout chrome — is absent from ground truth because it wasn't fetched, **not** because the real product lacks it. Don't report that as an "invented" element in the sandbox, and don't delete the sandbox's version to make the two match.

Say so explicitly in the report instead: which side has chrome the other doesn't, and why. If the sandbox has chrome that was itself built from a stale screenshot, flag it as unverified — it's outside this screen's scope, but the user should know it was never checked, and widening the harness to cover it is their call to make.

---

## Phase 3 — Apply fixes

**Goal**: close the gaps from Phase 2 without drifting into rebuilding the whole screen or inventing scope the real thing doesn't ask for.

Split fixes into two kinds:

- **Small and unambiguous** — a wrong component mapping, hand-rolled markup that should be a real component, a missing prop or link that's clearly scoped. Fix these directly. Still follow the sandbox's own `CLAUDE.md` rule while you do: check `COMPONENTS.md` and the real installed component source before writing anything, same as any other edit to this sandbox — this check doesn't get to skip that discipline just because it found the gap.
- **Larger scope additions** — a whole new modal, a whole new sidebar or feature area the rebuild never had at all. Stop and ask before building these. The real thing having more surface area than the rebuild isn't automatically a mandate to match all of it — that's a call for whoever owns the sandbox, the same "ask, don't guess" discipline the rest of this workflow already runs on.

---

## Phase 4 — Re-verify

**Goal**: confirm the fixes actually closed the gaps, not just that you made some edits.

Re-render both sides after fixing and re-check the list from Phase 2 item by item.

A clean typecheck and a few interaction clicks are **not** re-verification. They prove the code compiles and the handlers fire; they say nothing about whether the screen looks like the real one. The check that matters is the one that failed before:

- **Re-screenshot both sides** and flip between them again. Editing the sandbox invalidates the "before" screenshot — take a new one.
- **Re-measure, color included.** Run the same comparison from Phase 2c — geometry *and* color — and put the numbers in the report, sandbox value next to real value. Editing tokens invalidates the previous color run exactly as editing layout invalidates the previous geometry run. If a number still differs, that's an open item, not a rounding detail — chase it until you can name the cause (a scrollbar, a `box-sizing` inherited from a reset, a token the real app overrides).
- **Re-read the styling diff** for the specific rules you ported, confirming they actually took effect in the rendered output rather than being overridden.

Anything still open at this point should be a deliberate call, not an oversight — name it explicitly in `FIDELITY_REPORT.md` (e.g. "real detail view needs backend content this sandbox doesn't have; built a simplified version instead") rather than letting it quietly stay unresolved.

### Reporting honestly

If this run found gaps a previous run of this same skill declared clean, say so plainly in the report — a new section describing what the earlier pass missed and why its method let it through. A fidelity report that quietly overwrites its own past conclusions teaches the next reader to trust it more than it deserves. The report's value is that it records how the screen was checked, not just that someone checked it.

### Offer the comparison to the user

The user usually wants to see this themselves, not just read that it's fixed. Offer a before/after they can open: serve the screenshots (before, after, real) from a small static page on its own port with a toggle that swaps them in place, and give them the URL alongside the live ports. Keep the "before" screenshot — once the fixes land it's the only remaining record of the original state.
