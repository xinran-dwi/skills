---
name: figma-to-claude-code
description: Turn a Figma design into a working Next.js + Tailwind CSS prototype. Use whenever the user pastes a Figma URL, says "build this from Figma", "implement this design", "turn my Figma into code", "convert Figma to Next.js", "make this design real", or wants to take a design they made in Figma and run it in the browser. Also triggers on /figma-to-claude-code.
---

# Figma to Claude Code

Take a Figma design and turn it into a fully working Next.js + Tailwind CSS prototype — pixel-faithful, with real design tokens, running live in the browser. Follow every step in order. Do not skip steps or bundle them together.

---

## Step 1 — Verify Figma is connected

Call `mcp__figma__whoami` silently.

- If it **succeeds**: continue to Step 2 without mentioning it.
- If it **fails**: stop and tell the user:

> "To use this skill, Figma needs to be connected to Claude Code. Here's how to set it up:
>
> 1. In Claude Code, type `/MCP` and press Enter — this opens the MCP settings screen.
> 2. Add the Figma MCP server from the list.
> 3. Once it's connected, come back and paste your Figma URL here.
>
> Alternatively, you can ask me: **"Set up Figma MCP for me"** and I'll walk you through it step by step."

Do not proceed past this step if the connection failed.

---

## Step 2 — Get the Figma URL

Ask the user:

> "Open your Figma file and right-click the main frame — the outermost rectangle that holds the full screen design. Choose **Copy as → Copy link to selection**.
>
> Paste that link here and I'll start reading the design."

Wait for the user to paste the URL. Do not proceed until you have it.

**Validate the URL:**
- It should contain `figma.com/design/`.
- It should ideally have a `node-id` parameter (this points to a specific frame rather than the whole file).
- If the URL has no `node-id`, tell the user:
  > "This link points to the whole file. For a more focused reading, right-click the specific frame you want built → Copy as → Copy link to selection, then try again. Or paste the same URL if you'd like me to work from the full file."
  Let the user decide. Don't block — if they paste again or confirm to proceed, continue.
- If the URL is not a Figma URL at all, ask them to re-paste and briefly explain where to find the correct link.

---

## Step 3 — Check the project environment

Look for an existing Next.js project in the current directory:
- `package.json` containing `"next"` in dependencies or devDependencies
- `next.config.*` file at the root
- `app/` or `pages/` directory

**If a Next.js project is found:**
Also check for Tailwind CSS (`tailwind.config.*` at root, or `"tailwindcss"` in `package.json`).

- If Tailwind is **missing**, tell the user:
  > "I found a Next.js project here, but it doesn't have Tailwind CSS set up yet. Tailwind is what lets me precisely match the spacing, colors, and typography from your Figma design. Should I add it now? (yes / no)"
  - If **yes**: install `tailwindcss`, `postcss`, `autoprefixer`; run `npx tailwindcss init -p`; update `tailwind.config.ts` content array to include `./app/**/*.{ts,tsx}` and `./components/**/*.{ts,tsx}`; add Tailwind directives to global CSS. Then continue.
  - If **no**: continue and note you'll use CSS variables and classes where Tailwind would otherwise be used.

**If no Next.js project is found:**
Ask:
> "I don't see a Next.js project in this folder. I can create one for you right here, or if you have an existing project open in a different folder, navigate there and run `/figma-to-claude-code` again.
>
> Should I create a new Next.js + Tailwind project here? (yes / no)"

- If **yes**: run `npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir=no --import-alias="@/*"`. Wait for it to complete, then tell the user: "All set — your project is ready. Now let's build the design."
- If **no**: tell the user which folder to navigate to and how to re-run the skill. Stop.

---

## Step 4 — Read the design and plan

This step has two phases: **read**, then **plan**. No code is written until the user approves the plan.

### Phase A — Read

Extract `fileKey` and `nodeId` from the Figma URL:
- URL pattern: `figma.com/design/<fileKey>/<name>?node-id=<nodeId>`
- Convert any `-` in `nodeId` to `:` before passing to MCP tools.

Run these calls in parallel:

1. `mcp__figma__get_design_context` (fileKey, nodeId) — layout structure, auto-layout behavior, constraints, component hierarchy
2. `mcp__figma__get_screenshot` (fileKey, nodeId) — visual reference; keep this for all subsequent steps
3. `mcp__figma__get_variable_defs` (fileKey) — design tokens: color variables, typography styles, spacing values, border radii; note exact Figma-given names
4. `mcp__figma__get_metadata` (fileKey, nodeId) — frame names, page structure, component instances used

After reading, synthesize what you learned. Do not output raw tool responses.

### Phase B — Plan

Present your plan in plain language — no code yet. Use this structure:

> **What I see:**
> [2–3 sentences: type of screen, main visual zones, overall style and feel]
>
> **Design tokens I'll use:**
> [Key color variables, font sizes, spacing values — named exactly as Figma named them so you can verify against your file]
>
> **Files I'll create:**
> [e.g., `app/page.tsx` (main page), `components/NavBar.tsx`, `components/HeroSection.tsx`, `app/globals.css` (token definitions)]
>
> **Build order:**
> 1. [e.g., Global CSS with color/type tokens]
> 2. [e.g., Layout shell]
> 3. [e.g., Components, inside-out or top-down]

Then ask:
> "Does this plan look right? If something seems off — a section I missed, a color that doesn't look right — tell me now and I'll adjust before building. Otherwise just say **'go'** and I'll start."

**Do not write any code until the user confirms.**

---

## Step 5 — Build

Build according to the approved plan. Apply these standards without exception.

### Quality bar
Reference: Linear, Vercel dashboard, Airbnb listing page. Dieter Rams: less, but better. Restraint over decoration. Every element earns its place.

### Design standards
- **Colors:** Maximum 3 hues. Use the token names from the Figma file — do not invent colors.
- **Hierarchy:** Achieved through size, weight, and spacing — not decorative effects.
- **Elevation:** Shadows and layering used only where the Figma design uses them. Lighter things foreground, darker things background. Prefer subtlety.
- **Alignment:** Pick a grid and hold it. Strong alignment everywhere.
- **Interactive color:** One brand/action color, used consistently.

### Technical standards
- **Tokens first.** Map all Figma color variables and typography styles to CSS custom properties in `app/globals.css` (e.g., `--color-primary: #...;`). Wire them into Tailwind via `tailwind.config.ts` `extend.colors` and `extend.fontSize`. This keeps naming in sync between Figma and code.
- **Pixel-faithful layout.** Use the auto-layout values from `get_design_context` for flex direction, gap, and padding. If Figma says `gap: 24`, use `gap-6` (Tailwind 4-unit scale).
- **Component structure.** One file per major section (`components/NavBar.tsx`, `components/HeroSection.tsx`, etc.). Keep `app/page.tsx` as an assembly of imports only.
- **Real copy.** No Lorem ipsum — write contextual placeholder text that fits the design.
- **Interactive states.** Implement hover, focus, and active states on all interactive elements using Tailwind's `hover:`, `focus:`, `active:` variants.
- **Responsive.** Verify layout at 1280px (desktop) and 375px (mobile). Add breakpoints where the Figma design implies different mobile behavior.
- **Assets.** If the design includes embedded images or icons, call `mcp__figma__download_assets` and output to `public/`.

After writing each major component, mentally compare it to the `get_screenshot` from Step 4. Fix drift before moving on.

Report each completed file in one line (e.g., "NavBar done."). Don't ask for feedback between files — just report and continue.

---

## Step 6 — Verify

Do not declare the build complete until you've verified it visually.

### Start the dev server

Detect the package manager:
- `pnpm-lock.yaml` → `pnpm dev`
- `yarn.lock` → `yarn dev`
- `package-lock.json` → `npm run dev`

Start the dev server in the background. Wait until port 3000 is reachable.

If the server fails to start, show the error and tell the user:
> "You can start it manually by typing `! npm run dev` (or `! pnpm dev` / `! yarn dev`) into Claude Code."

### Inspect with Playwright

Use the Playwright MCP tools:

1. `mcp__playwright__browser_navigate` → `http://localhost:3000`
2. `mcp__playwright__browser_take_screenshot` at 1280px — compare against the Figma screenshot from Step 4
3. `mcp__playwright__browser_resize` to 375px → `mcp__playwright__browser_take_screenshot` — check mobile layout
4. `mcp__playwright__browser_snapshot` — verify the accessibility tree; buttons, links, and inputs should all be reachable
5. Walk through the main interactive user flow: `mcp__playwright__browser_click`, `mcp__playwright__browser_fill_form`, `mcp__playwright__browser_press_key` as needed

Look for: missing sections, wrong layout gaps, color mismatches, typography that doesn't match the design, elements with no hover/focus state.

Fix any issues before declaring done. Re-screenshot after structural fixes.

**If Playwright MCP is unavailable:** ask the user to open `http://localhost:3000` in Chrome and describe what to look for section by section.

### TypeScript check

Run `npx tsc --noEmit`. Fix all errors silently if they're minor. If errors would require significant rework, surface them and propose the fix before executing.

### Report

> "Your design is live at **http://localhost:3000**. Here's what was built: [2–3 sentences describing the main sections, key interactions, and any intentional judgment calls you made]."

---

## Step 7 — What's next?

Present both options clearly, then stop and wait for the user's choice.

---

**Option A — Make revisions to this design**

> "To refine a specific part:
>
> 1. In Figma, zoom into the section that needs a change.
> 2. Right-click that specific area → **Copy as → Copy link to selection** — this gives me a narrower, more focused URL that produces much better results than re-sharing the whole page.
> 3. If you want to mark something up visually, draw shapes or annotations directly in Figma, take a screenshot of that area (**⌘⇧4** on Mac), and paste it here (**⌘V**). I can read images directly.
> 4. Paste either (or both) back here and tell me what to change.
>
> Iteration gets faster once you have a solid base — and you're there now."

---

**Option B — Build a new page from this design**

> "To add another page that stays visually consistent, paste this prompt into a new message and fill in the last line:
>
> ---
> Use the components in this codebase to create a new page that needs to be consistent with the current page. Use similar structural elements, chrome, color, layout, alignment, and spacing. The new page is: [describe what it needs to do]
> ---"
