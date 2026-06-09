---
name: design-inspect
description: Open a running Next.js dev build in the browser with an inspect-and-prompt overlay (like Cursor's Design Mode). The user clicks one or more elements on the page, types a change request, and the overlay copies an inline-fingerprint payload (`<tag class="..."> "text" [Component]` blocks plus instructions) to the clipboard. They paste it back into Claude Code and the assistant locates the exact JSX line by component + className/text and makes the edit. Use this whenever the user wants to point at something in their running app and ask for a change — phrases like "inspect mode", "design mode", "let me click the thing I want to change", "I want to point at an element", or invokes the slash command /design-inspect.
---

# Design Inspect

Lets the user point at one or more rendered elements in their Next.js dev build and hand a precise edit prompt back to Claude Code. The overlay captures each element's React component name (via the fiber tree) plus a **DOM fingerprint** — tag, className, visible text — so the assistant can locate the exact JSX line even when source-map line numbers don't resolve (common in Next.js with Turbopack/webpack-bundled dev output).

It works in `next dev`. Production builds strip component metadata, so the fingerprint will still help but component names may be absent.

## Flow

Follow these steps in order. Do not skip steps or batch them.

### 1. Confirm we're in a Next.js project

Check for `next` in the nearest `package.json`. If not found, tell the user "design-inspect needs a Next.js project — I don't see `next` in package.json" and stop.

### 2. Make sure a dev server is running

Check if anything is listening on common Next.js dev ports (3000, 3001, 3002):

```
lsof -nP -iTCP -sTCP:LISTEN | grep -E ':(3000|3001|3002)' || echo "no dev server"
```

- If something is listening, ask the user which port is their app (don't assume).
- If nothing is listening, ask the user: "Should I start `npm run dev` (or `pnpm/yarn dev` — match their lockfile)?" If yes, start it with `run_in_background: true` and wait until the port is reachable. Use `Monitor` on the background task to detect "ready" / "compiled" / port-open in the logs.

### 3. Open the app

```
open http://localhost:<port>
```

### 4. Branch on whether the overlay is already loaded

The user may have installed the optional userscript (see "Optional: zero-friction setup" below), in which case the overlay auto-loads on every `localhost` page. Tell the user:

> Look at the bottom-right corner of the page. Do you see a `◎ Inspect Mode` pill?

**If yes** — the userscript is doing its job. Skip ahead and send only the usage instructions:

> Great — the overlay is already loaded. Click `◎ Inspect Mode`, then hover/click the elements you want to change (blue outline + label appears). Click each element to add it as a chip. Type your instructions in the popup, hit Enter or click "Copy to clipboard", and paste back here.

**If no** — fall back to the paste flow. First copy the overlay to the clipboard:

```
pbcopy < ~/.claude/skills/design-inspect/overlay.js
```

Then send the user this message:

> The overlay script is on your clipboard. In the browser:
> 1. Open DevTools Console (⌥⌘J)
> 2. If Chrome warns about pasting, type `allow pasting` + Enter, then paste the overlay and hit Enter
> 3. A small `◎ Inspect Mode` pill appears bottom-right — click it, then hover over the elements you want to change (a blue outline + label shows the component name)
> 4. Click each element to add it as a chip to the popup. Inspect Mode stays on so you can stack chips without re-clicking
> 5. Type your instructions in the popup. Hit Enter or click "Copy to clipboard"
> 6. Paste back here and I'll make the edits

### 5. Wait for the user's paste

The overlay produces a single prose string where each selected element is expanded **inline** as a fingerprint right next to the user's request text. There is no separate References block — the target and the action sit next to each other.

### Inline fingerprint shape

Each chip becomes one of these inline tokens:

- With source location: `<tag class="..."> "visible text" [ComponentName @ path/file.tsx:NN]`
- Component only:     `<tag class="..."> "visible text" [ComponentName]`
- Tag/text only:      `<tag class="..."> "visible text"`

Example payloads:

Single target — one line:
```
<span class="font-bold text-lg leading-[27px] text-text-primary pr-1"> "658" [ListingHeader] change to green
```

Multiple targets — each fingerprint+instruction block is on its own paragraph, separated by a blank line:
```
<button class="antialiased bg-transparent text-accent..."> "5:00 pm" [HotMarket]  change to red

<button class="antialiased bg-transparent text-accent..."> "6:00 pm" [HotMarket]  change to red

<span class="font-bold text-lg leading-[27px] text-text-primary pr-1"> "658" [ListingHeader]  change to green
```

Each paragraph is a self-contained request: a single fingerprint plus the action text the user wrote around it. Process them as a group — read every referenced file and apply edits across the project in one coherent change.

### How to act on the payload

For each inline fingerprint:

1. **If `[Component @ path:line]` is present** — open that file at that line. Verify the line matches the fingerprint's tag + className before editing (defends against off-by-one source maps).
2. **If only `[ComponentName]` is given** — open the component's source file (`ComponentName` → `components/ComponentName.tsx`, or a quick grep). Locate the exact JSX element by grepping for the className first (Tailwind classes like `font-bold text-heading pr-2` are highly distinctive — usually one line in the file). If className isn't unique, narrow by the visible `"text"`. If still not unique, use both.
3. **If no `[...]` tag is given** — grep the project for the className or text.

Read the line(s) around your match before editing. If the fingerprint doesn't uniquely match exactly one line, ask the user rather than guess.

### Mapping intent to targets

Each paragraph in a multi-chip payload is one target + its instruction. The action text in that paragraph applies to the fingerprint in that paragraph. Two examples:

```
<button ...> "5:00 pm" [HotMarket]  change to red

<button ...> "6:00 pm" [HotMarket]  change to red
```
→ both buttons get red applied (two paragraphs, same instruction).

```
<span ...> "658" [ListingHeader] change to green
```
→ the 658 span gets green.

If the instruction sits before the fingerprint in a paragraph, that still applies to that paragraph's fingerprint:
```
change to blue <span ...> "$275,000" [ListingHeader]
```

When the className is shared by sibling elements (e.g., a list rendered via `.map()`), edits to that JSX line affect all of them. Call that out in your reply so the user knows whether to add conditional logic for a subset.

If a fingerprint has no tag, no className, and no text, the element wasn't capturable (e.g., a text-only DOM node, or a node inside `dangerouslySetInnerHTML`). Ask the user to pick a parent element instead.

## Notes

- The overlay is designed for `next dev`. Production builds strip React component metadata, so chips will lack `[ComponentName]` and you'd need to fall back to grepping the project for the className / text.
- The overlay persists for the page session. The user can keep adding chips and submitting prompts without re-pasting — just rerun the skill if they reload the page.
- Inspect Mode **stays on** after each click, so the user can stack chips by clicking multiple elements in a row. Esc (or clicking the `◎ Inspect Mode` pill again) exits inspect mode. Esc with the popup open closes the popup and discards.
- The popup has a `Clear` button (bottom-left) that wipes chips + prose without closing.
- Source-map line numbers often don't resolve in Next dev — bundled paths like `_next/static/chunks/components_xxx._.js:NN` are intentionally skipped because the line numbers point into the bundle, not source. Component name + fingerprint is the actionable info; trust it.
- If the user's app has a strict CSP that blocks console-injected scripts, the overlay won't load; they'd need to allow `unsafe-eval` / `unsafe-inline` in dev, or we'd have to embed the overlay as a dev-only component (a heavier path — propose that as a fallback only if asked).
- A diagnostic helper is available: `window.__designInspectDebug(document.querySelector("some-selector"))` dumps the fiber chain's debug fields. Useful when fingerprint capture seems wrong.

## Optional: zero-friction setup (skip the paste step)

For repeat users only. The default paste flow is intentional — it requires zero prerequisites and is safe for everyone. If you use this skill often and want to skip console paste each session, install the bundled userscript so the overlay auto-loads on every `localhost` page.

**Install (one-time):**

1. Install [Tampermonkey](https://www.tampermonkey.net/) (Chrome/Edge/Brave/Firefox/Safari) or Violentmonkey.
2. Open `~/.claude/skills/design-inspect/userscript.user.js` in your browser — Tampermonkey will detect the `.user.js` extension and show an Install screen.
3. Click Install.

After install: open any `http://localhost:*` page and the `◎ Inspect Mode` pill appears automatically. When you next run `/design-inspect`, the assistant will see the pill is already present and skip the paste step.

**Trust note.** The userscript matches `http://localhost:*/*` and `http://127.0.0.1:*/*`, so it injects the overlay into every local web service you run (DB admin UIs, internal tools, etc.). If that's a concern, tighten the `@match` lines in the userscript to specific ports (e.g. `http://localhost:3000/*`).

**Updating.** When `overlay.js` changes (rare), re-run the regeneration step below and reinstall the userscript, or it will silently run stale code.

**Regenerating `userscript.user.js` from `overlay.js`** (maintainer-only, after editing `overlay.js`):

```
cd ~/.claude/skills/design-inspect
( head -n 11 userscript.user.js; cat overlay.js ) > userscript.user.js.new && mv userscript.user.js.new userscript.user.js
```

The `11` matches the line count of the `==UserScript==` header block + its trailing blank line. `overlay.js` remains the single source of truth.
