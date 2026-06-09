---
name: design-exploration
description: Create N distinct design explorations of a UI section, grounded in a PRD and user research, displayed with a toggle switcher and full surrounding page context.
---

You are helping the user run a structured design exploration sprint for a UI section.

## Step 1 — Understand the brief

Before designing anything, ask the user to confirm or provide:
1. **Which section** to redesign (e.g. "About This Home", "Checkout Summary")
2. **How many explorations** (default: 3)
3. **Brief files** — look for these in the project (common locations: `_brief/`, `docs/`, `brief/`):
   - A PRD or product context file (product goals, business goals, design constraints)
   - A user research file (usability findings, pain points, what's working)
   - A screenshot or image of the current design as the baseline
4. **The current component file** to use as the implementation baseline

Read all brief files and the current component before planning.

## Step 2 — Plan 3 distinct explorations

Each exploration must:
- Address a **different cluster** of user research findings — not 3 variations of the same idea
- Respect all design constraints from the PRD (height limits, team boundaries, etc.)
- **Preserve what's working** (note this explicitly from user research)
- Be implementable in React + Tailwind using existing color tokens and components

Name each exploration with a short descriptor (e.g. "Cost-Forward", "Scan-First", "Unified Digest") that communicates its core concept.

Present the plan to the user before writing any code.

## Step 3 — Implement

Create a separate component file for each exploration:
- `components/[SectionName]V1.tsx`
- `components/[SectionName]V2.tsx`
- `components/[SectionName]V3.tsx`

Keep the agent footer / chrome / unchanged regions identical to the baseline — only redesign the section in scope.

All "Show more" / expand interactions remain static (no state) — this is a visual design exploration.

## Step 4 — Build the toggle display

Create `components/ExplorationToggle.tsx` as a `"use client"` component that:
- Shows a **toggle bar at the top** with one tab per exploration plus the baseline
- Each tab has a short label ("Exploration 1") and sublabel ("Cost-Forward")
- Active tab is visually distinct (dark background)
- Switching tabs swaps only the section under exploration — the surrounding page context (header, sidebar, adjacent sections) stays mounted and visible at all times

Wrap the toggled section in the **full surrounding page context** — include the components above and below the section (listing header, hot market banner, sidebar, etc.) exactly as they appear in the real page layout. This lets the user evaluate each exploration in its actual page environment, not in isolation.

Update `app/page.tsx` to render `<ExplorationToggle />` with the appropriate max-width for the layout.

## Step 5 — Verify

Run a TypeScript check (`npx tsc --noEmit`) before declaring done. Flag any errors to the user.
