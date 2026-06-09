---
name: design-explore-canvas
description: Generate 4 meaningfully distinct design directions from a single base design (screenshot, Figma URL, code file, or written description), each accompanied by bullet-point rationale explaining the *why* behind its design decisions. Output is an interactive HTML viewer with a toggle bar to switch between base and four options and a side panel showing the rationale. Every generation is also appended to a per-project visual canvas at `<project_root>/explore-design-canvas/canvas.html` — like visual version control for design ideas scoped to one project — so the user can scroll through past options and fork new generations by referencing a stable ID such as "V2-Option3". Use this skill whenever the user wants to see multiple visual directions for a UI, compare design treatments side by side, brainstorm what a screen could look like, fork off a previous exploration, or asks things like "give me 4 options for this", "show me a few directions", "what could this look like", "revise V2-Option3 with a softer feel", or "iterate on that minimalist one". Do not use the Stitch MCP — the user has a separate stitch-brainstorm skill for that.
---

# Design Explore Canvas

Generate 4 distinct design directions from one input, present them in an interactive viewer with rationale bullets, and accumulate every generation on a per-project canvas the user can fork from later.

## Why this skill exists

Most "explore options" flows produce four near-identical pixel tweaks of the same idea. That isn't useful for ideation. The value here is **four meaningfully different design directions** (e.g., editorial vs. minimalist vs. dense vs. playful), each with a short written rationale that explains *why* it made the choices it did. The user reads the rationale, decides which direction resonates, then iterates by referencing a stable option ID.

The per-project canvas makes design exploration feel like **version control for ideas, scoped to one project** — every option generated for *this* project stays viewable with lineage; other projects don't pollute the view. The user can scroll back, pick any past option, and fork from it.

The skill lives at `~/.claude/skills/design-explore-canvas/`. Assets and scripts are referenced from there. The canvas it writes lives **inside the project**, not in `~` — see Step 5.

## Step 1 — Determine the input

If the user is referencing an existing option ID (e.g., "revise V2-Option3", "iterate on V1-Option4 with more whitespace"), this is a **revision** — skip to Step 6.

Otherwise, identify which input type the user is providing. Ask only if it isn't obvious from context:

1. **Image / screenshot** — they pasted or linked an image. Save it locally if needed and remember the path.
2. **Figma URL or node** — a `figma.com/design/...` URL. Use the Figma MCP (`get_design_context`, `get_screenshot`) to read it. Load the `/figma-use` skill first if you're going to call `use_figma`.
3. **Code file** — a component file in the repo. Read it.
4. **Text description / PRD** — written description of the screen.

## Step 2 — Understand the design's intent

Before picking directions, get clear on:
- **What the screen is for** (onboarding, dashboard, checkout, marketing landing, settings, etc.)
- **The user's primary goal** on that screen
- **Brand or tone signals** if visible (corporate, consumer, playful, technical, premium)
- **Hard constraints** the user named ("keep the nav", "must work in dark mode")

If something critical is missing and would meaningfully change which directions you pick, ask one focused question. Otherwise infer and move on — don't over-interview. The user came here to see options, not answer a survey.

## Step 3 — Plan 4 distinct directions

Pick four directions that are **meaningfully different from each other and from the base**. The goal is to give the user *real choices*, not variations of one idea.

Direction families to mix and match (don't pick four from the same family):

- **Structural**: minimalist, dense / utility-forward, sidebar-led, split-screen, single-column scroll, card-grid
- **Editorial**: typography-led, magazine layout, serif-led, long-form
- **Expressive**: brutalist, playful / illustrated, neumorphic, glass / iOS-like, y2k, retro
- **Tonal**: soft / organic, monochrome, vibrant, dark-mode-native, pastel, high-contrast

Sanity check: if two of your four feel like cousins, replace one. Different = different.

Give each direction a short evocative name (e.g. "Editorial Calm", "Data Dense", "Soft Playful", "Brutalist Grid"). The user will see this name on the toggle button.

## Step 4 — Write the rationale, then the HTML

For each option, **write 4–7 rationale bullets before writing any HTML**. This forces the design decisions to be deliberate. Each bullet should explain *why* — what user goal or brand signal motivated this typography, layout, color, or density choice. Bullets should read like a designer thinking aloud, not a checklist of what's visible.

Bad bullet: *"Uses a large serif headline."*
Good bullet: *"Leans on a serif headline to read as editorial rather than transactional — the brand wants to feel considered, not promotional."*

Bad bullet: *"Sidebar on the left."*
Good bullet: *"Pulls the nav into a left rail so the main content can become the hero — the user comes here to read, not to navigate."*

Then write the HTML for each option. Each option is a self-contained block of HTML+CSS that goes inside the viewer's main stage. Quality bar:

- Real-looking copy (no Lorem ipsum). Use plausible product names, prices, headlines, body copy that fits the brief.
- Real-looking icons: Unicode symbols, simple inline SVG, or `https://api.iconify.design/<set>/<name>.svg` URLs.
- Decent typography hierarchy, spacing, color contrast. Layouts should hold up at 1280px.
- **Scope your CSS.** Each option's HTML is injected into the viewer alongside others — wrap it in a unique class like `.v-{slug}` and scope every selector under it, or use inline styles. Don't write bare element selectors that bleed across options. CSS rules must be inside a `<style>` tag — bare CSS pre-pended to the HTML will render as visible text.
- **No JavaScript inside options.** These are static visual mocks. The viewer handles toggling between them.

### Stay inside the base design's grammar by default

This is a hard default, not a suggestion. When the input comes from a real project (code file, live URL of a built page), **use 100% of the base's tokens, components, and icons by default**. Introduce new visual primitives only when a direction genuinely demands it, and even then reference the base — same color family, same border-radius scale, same icon library. Options should look like *plausible siblings* of the baseline, not like designs from four different products.

Before writing any HTML:
1. **Read the design tokens.** Look at `globals.css`, `tailwind.config.*`, `app/globals.css`, or any tokens file. Pull out exact colors, typography scale, border/radius values. Use those exact values inline — don't approximate "teal" when the project ships `--color-accent: rgb(21,114,122)`.
2. **Inventory the base's primitives.** What icons does it use (lucide, heroicons, custom)? What's the card pattern (border width, radius, padding)? What's the heading scale? Re-use these — re-inline lucide SVGs at the same size; match the card chrome exactly.
3. **Vary structure, not style.** The directions should differ in *hierarchy, ordering, density, progressive disclosure* — not in color palette, font family, or icon library. "Editorial vs. brutalist" is the wrong framing for a real project; "summary-led vs. spec-led vs. two-column scan vs. highlights-as-chips" is the right framing.
4. **Exception.** If the user explicitly asks for "off-brand explorations" or "what if we redesigned the whole system", then expressive directions (brutalist, editorial, playful) are fine. Otherwise: same grammar.

This is true even when you have to inline SVGs by hand because the canvas can't run React/lucide. Inline the *same* SVG path data the project uses; don't substitute emojis or different icons.

## Step 5 — Append to the canvas

Everything goes through one script: `scripts/canvas.py add`. It takes a JSON payload describing the generation, appends it to a **per-project** data file at `<project_root>/explore-design-canvas/data.json`, and regenerates `<project_root>/explore-design-canvas/canvas.html`.

The canvas dir is resolved automatically:
- `<project_root>` is the nearest ancestor of the current working directory that contains a `.git` folder (falling back to cwd if none).
- This means each project gets its own canvas; other projects' explorations never appear here.
- Override with the `CLAUDE_DESIGN_CANVAS_DIR` env var if needed.
- The folder is **not** auto-gitignored — mention this to the user once and let them decide whether to track it.

The canvas has two views in one HTML file:

- **Grid view** (`canvas.html` with no hash): every generation for this project, stacked newest-first. Each row shows a header (e.g. `V2` · forked-from chip · timestamp), four card thumbnails, and a right-side **context panel** labeled "PROMPT USED" that quotes the user's verbatim prompt (`source_summary` for fresh gens, `revision_hint` for forks). The header also shows the project's absolute path.
- **Detail view** (`canvas.html#VN-OptionM`): a full-page viewer for one generation. Sticky two-row toolbar (back button · gen ID · prompt text · forked-from chip on row 1; tab-style toggle bar on row 2 with buttons labeled `Base`, `Option 1`, `Option 2`, `Option 3`, `Option 4`). Below: the design in a scrollable stage on the left, rationale bullets in a fixed-width side panel on the right. The toolbar and side panel never reflow as you switch toggles, so heights don't jump.

Construct the JSON payload like this:

```json
{
  "source_summary": "explore 4 design directions for the pricing page",
  "parent_id": null,
  "revision_hint": null,
  "base": {
    "kind": "image",
    "content": "/absolute/path/to/screenshot.png"
  },
  "variants": [
    {
      "direction_name": "Unified Digest",
      "rationale": ["Bullet 1...", "Bullet 2..."],
      "html": "<style>.v-unified {...}</style><div class='v-unified'>...</div>",
      "iframe_src": "http://localhost:3000/embed/option/V1-Option1"
    },
    { "direction_name": "AI-First", "rationale": [...], "html": "...", "iframe_src": "..." },
    { "direction_name": "Two-column Scan", "rationale": [...], "html": "...", "iframe_src": "..." },
    { "direction_name": "Highlights as Chips", "rationale": [...], "html": "...", "iframe_src": "..." }
  ]
}
```

Notes on the schema:
- The array key is still `variants` (internal contract for the script), even though the UI surfaces them as **Options** and IDs read `V1-Option1` etc. Don't rename the JSON key.
- `iframe_src` is optional. Include it only when you've also set up an embed route that renders the option (see "When `base.kind` is `\"url\"`" below). When present, the canvas renders the option via iframe instead of injecting the raw HTML.

For `base.kind`:
- `"url"` — `content` is an `http(s)://` URL (typically the local dev server like `http://localhost:3000`); the canvas embeds it as an `<iframe>` in the Base tab. **Prefer this when the input is code from the running project** — it shows the real Tailwind/React-rendered design instead of a stub. Caveats: requires the server to be running when the canvas is viewed; not a frozen artifact (hot reloads will update the iframe).
- `"image"` — `content` is a file path; the canvas will copy it next to the HTML and `<img>` it. Use when the input was already a screenshot, or when you need a portable frozen snapshot.
- `"html"` — `content` is an HTML snippet (for written-description cases). Avoid when a live URL is available — hand-written HTML stubs drift from the real design.
- `"figma"` — `content` is the URL; the canvas shows the URL plus an `<img>` if you also pass `image_path`.
- `"text"` — `content` is the prose description; the canvas shows it as a styled text block.

**Decision rule for choosing `base.kind`** when the input was a code file or a "design this section" prompt:
1. Is there a live dev server URL that shows the section? → use `"url"`.
2. Else: can you screenshot the design (Playwright MCP, etc.)? → use `"image"`.
3. Else, fall back to `"html"` and tell the user the base is a hand-written stub, not the real render.

### When `base.kind` is `"url"`: also render Options as URLs (apples-to-apples)

If the Base is a live URL, the Base tab shows the section *inside its full page chrome* (header, sidebar, surroundings). If the Options are static HTML, they show *only the section* on an empty canvas — and switching between Base and Option becomes visually whiplash, not a controlled comparison. Always avoid that.

Add an `iframe_src` field to each variant in the payload. When set, the canvas renders that option in an iframe instead of injecting raw HTML, so it inherits the same surroundings as Base:

```json
{
  "direction_name": "Unified Digest",
  "rationale": [...],
  "html": "<div class='v-unified'>...</div>",
  "iframe_src": "http://localhost:3000/embed/option/V1-Option1"
}
```

The `html` field is still required — it's the source of truth that the embed route reads from. The `iframe_src` is just the render hint.

**Recipe to wire this up in a Next.js / React project** (adapt for other frameworks):

1. **Add a clean embed route for the Base** that renders the surrounding context without any toggles or chrome that doesn't belong in the comparison:
   ```tsx
   // app/embed/page.tsx
   export default function Embed() {
     return (
       <div className="bg-page p-6">
         <div className="max-w-[980px] mx-auto">
           <div className="flex gap-6 items-start">
             <div className="flex-1 min-w-0 flex flex-col gap-3">
               <ListingHeader /> <HotMarket /> <AboutThisHome />
             </div>
             <ListingSidebar />
           </div>
         </div>
       </div>
     );
   }
   ```
   Set `base.kind: "url"`, `base.content: "http://localhost:3000/embed"`.

2. **Add a dynamic option route** that reads the option HTML from `data.json` server-side and injects it in place of the section being explored:
   ```tsx
   // app/embed/option/[id]/page.tsx
   import { promises as fs } from "fs"; import path from "path";
   import { notFound } from "next/navigation";

   export default async function OptionEmbed({ params }: { params: Promise<{ id: string }> }) {
     const { id } = await params;
     const data = JSON.parse(await fs.readFile(
       path.join(process.cwd(), "explore-design-canvas", "data.json"), "utf-8"
     ));
     const html = data.generations.flatMap((g: any) => g.variants).find((v: any) => v.id === id)?.html;
     if (!html) notFound();
     return (
       <div className="bg-page p-6">
         <div className="max-w-[980px] mx-auto">
           <div className="flex gap-6 items-start">
             <div className="flex-1 min-w-0 flex flex-col gap-3">
               <ListingHeader /> <HotMarket />
               <div dangerouslySetInnerHTML={{ __html: html }} />
             </div>
             <ListingSidebar />
           </div>
         </div>
       </div>
     );
   }
   ```
   Then set each option's `iframe_src` to `http://localhost:3000/embed/option/<option_id>`.

3. **Don't include a toggle nav on the embed route** — the canvas already has one. Two stacked toggles look broken.

**When to skip Option-as-URL:** if the user wants frozen / shareable artifacts that survive the dev server being off, or the project isn't a runnable web app. In those cases, accept the asymmetry and use `image` for Base too.

A few words on the user-visible strings — they surface in the grid context panel and the detail toolbar, so make them carry weight:

- `source_summary` is the **user's verbatim prompt** for this generation — the thing they actually typed (e.g. `/design-explore-canvas`, "give me 4 directions for the about-this-home section", or whatever they said). Do NOT paraphrase or write a designer-style description. The panel labels it "PROMPT USED" and quotes it.
- `revision_hint` (only for forks) is the user's literal revision instruction, in their own words. Quote them rather than paraphrasing — same "PROMPT USED" panel.

Write the JSON to a temp file (e.g., `/tmp/design-gen.json`), then run:

```bash
python3 ~/.claude/skills/design-explore-canvas/scripts/canvas.py add /tmp/design-gen.json
```

The script prints a `canvas_url` of the form `file:///<project_root>/explore-design-canvas/canvas.html#VN-Option1` — that's a deep link that opens the canvas straight into the full-page detail view for the new generation, focused on Option 1. Open it for the user (the `file://` prefix is required for `open` to preserve the URL fragment):

```bash
open '<canvas_url>'
```

Then tell the user, briefly:
- The canvas is open in the full-page detail view of the new generation
- Use the tab bar (or keys `1`–`5`) to switch between Base and the four options; the design stage scrolls independently so toggling doesn't reflow the page, and the rationale panel on the right updates per option
- The `← Canvas` button in the toolbar returns to the grid of every exploration *for this project*
- They can fork any option by referencing its ID in a follow-up prompt (e.g., "revise `VN-Option2` with a softer feel")

## Step 6 — Handling revisions

When the user references an existing option ID (`VN-OptionM`) and asks for a revision:

1. Look up the option:
   ```bash
   python3 ~/.claude/skills/design-explore-canvas/scripts/canvas.py get <option_id>
   ```
   This prints JSON with the option's `direction_name`, `rationale`, `html`, and original `source_summary`. (The CLI's `get` subcommand still takes a single ID like `V2-Option3`.)

2. Treat that option as the new **base**. Re-run Steps 3–5 with two adjustments:
   - All four new directions should honor the user's revision hint (e.g. "softer", "denser", "darker") while still being meaningfully distinct *from each other*. Don't make four softer takes; make four softer takes that go softer in different ways.
   - In the payload, set `parent_id` to the referenced option ID, set `revision_hint` to the user's instruction in their words, and set `base.kind` to `"html"` with `base.content` set to the parent option's HTML so the viewer can show what was forked.

The canvas will display the new generation with a "Forked from `VN-OptionM`" label, preserving lineage.

## What this skill is not

- **Not a code-output exercise.** The viewer HTML is a comparison tool, not shippable production code. Don't try to use the project's component library or design tokens (unless the input *was* code from the repo and the user explicitly wants on-brand variants).
- **Not for pixel-level iteration on one design.** This skill is for picking *which direction to pursue*. Once the user picks a direction, iterating on a single design happens in code.
- **Does not use the Stitch MCP.** The user has `stitch-brainstorm` for that flow.
