Creator: Xinran Ma

More resources like this on: designwithai.co

# design-sandbox-verify

## What it is

`design-sandbox-verify` checks a rebuilt UI screen against the **real thing it's supposed to resemble**, finds concrete gaps, and closes them. Instead of comparing against a screenshot — which can be months stale while the real component has moved on — it fetches the real component source read-only, renders it live in a throwaway harness fed your sandbox's own fake data, and compares the two side by side. It's the companion to [`design-sandbox-setup`](../design-sandbox-setup/): that skill builds the first pass of a screen, this one proves how close it actually got.

## When to use it

- You rebuilt a screen and it "looks about right," but you have no idea how right.
- You built from a screenshot or from memory, and you suspect the real component has changed since.
- Someone looked at your sandbox next to the real app and said "these look different" — but nobody can say exactly how.
- You want to confirm a rebuild is genuinely using design system components, not lookalikes that happen to render similarly.
- You want an itemized, checkable list of what's off, instead of a vague sense that something is.

## How to use it

### Install (one time)

```bash
git clone https://github.com/xinran-dwi/skills.git
mv skills/design-sandbox-verify ~/.claude/skills/
```

Restart Claude Code.

### Step by step

1. **Have a screen to check** — run it in your sandbox on its own dev server first. This skill checks an existing rebuild; it doesn't create one. If you don't have a sandbox yet, run [`design-sandbox-setup`](../design-sandbox-setup/) first.

2. **Run it** — `/design-sandbox-verify`, then something like *"check this against the real screen."* Tell it where the real source lives (a public repo, an internal repo, a local checkout) and which screen, unless that's already obvious from the sandbox's own `COMPONENTS.md` and comments — if it can't tell, it asks rather than guessing.

3. **It builds a ground-truth harness** — fetching the real component files one by one (never a full clone of a huge repo), placing them at the paths their own imports expect, and mocking only what genuinely needs a running instance: a permissions hook, an i18n call, an API client. **It never edits the fetched files.** Anything that must change to make them render changes in the mock layer, so ground truth stays ground truth.

4. **It feeds both sides the same data** — your sandbox's existing fake data, reshaped into whatever shape the real files expect. This matters more than it sounds: if the two sides show different content, every difference you spot is ambiguous. Identical data is what makes a difference mean something.

5. **It compares three ways** — a render pass (screenshot both, then flip between them in place, because a difference invisible when your eye travels between two images jumps out when one swaps under a fixed cursor); a source pass that reads the **styling layer**, not just the markup, since copying a component's structure while dropping its CSS is the easiest way to pass a props check and still look wrong; and a measurement pass that reads real computed geometry via `getBoundingClientRect()` and `getComputedStyle()`.

6. **You get `FIDELITY_REPORT.md`** — gaps sorted into four kinds: **missing** (a real element the rebuild lacks), **invented** (something that was never in the real screen), **wrong mapping** (a real component used in the wrong spot), and **styling dropped** (right component, right props, visual layer didn't come across). Measured numbers go in the report next to each other — "card width 1392px vs 1392px" is checkable by the next person; "looks the same now" isn't.

7. **It fixes the small stuff and asks about the big stuff** — a wrong component mapping or a dropped CSS rule gets fixed directly. A whole missing modal or a feature area the rebuild never had is a scope decision, so it stops and asks. Re-verification is by measurement, not by eye: a clean typecheck proves the code compiles, not that the screen looks right.

8. **Look at it yourself** — it offers a before/after/real toggle page on its own port so you can flip between the three and judge the result rather than taking the report's word for it.

Anything still different at the end is named in the report as a deliberate call with its cause identified, not quietly left to look like a match. A report that says "here's what's still off and why" is worth more than one claiming perfection.

## Requirements

- [Claude Code](https://claude.ai/code)
- A rebuilt screen running on a local dev server — usually a [`design-sandbox-setup`](../design-sandbox-setup/) output
- Read access to the real component source (public repo, internal repo, or local checkout). You never need to *run* the real app.
