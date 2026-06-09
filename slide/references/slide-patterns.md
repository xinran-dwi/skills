# Slide Patterns

A library of composable layouts. These are starting points, not a fixed template. Mix surfaces, vary which side holds the headline, drop patterns you don't need. The goal is a deck that feels art-directed, where each slide earns its layout from its content.

## How patterns work

Every slide is a `<section class="slide surf-X">` where `surf-X` is one of four semantic surfaces:

| Surface | Role | Verdant looks like |
|---|---|---|
| `surf-paper` | light, neutral, for dense content | off-white bg, near-black ink |
| `surf-ink` | near-black, for focus/contrast | black bg, white ink |
| `surf-brand` | deep brand color, for openers/closers | forest green bg, lime headline |
| `surf-accent` | vivid, for energy/section breaks | chartreuse bg, dark ink |

The color-style toggle (`C`) remaps all four surfaces at once, so a deck that alternates surfaces stays coherent in every palette. **Rotate surfaces for rhythm** — don't put five paper slides in a row. A common cadence: brand opener, accent section break, paper/ink content, accent break, brand closer.

Wrap the first one or two elements of each slide's `.body` in `class="rise"` so the subtle fade-up plays on entry. Don't put `rise` on every element — one gesture per slide reads as intentional, a cascade of twenty reads as noise.

The header band is optional on full-bleed opener/closer slides (title, section, Q&A) and expected on content slides.

---

## 1. Title / opener

Full-bleed brand surface, oversized serif, meta row pinned to the bottom with a hairline above it.

```html
<section class="slide surf-brand is-active">
  <div class="body">
    <h1 class="display rise">Project Status</h1>
  </div>
  <hr class="rule">
  <div class="foot rise" style="margin-top:20px">
    <div><div class="label">Project Aero</div><div class="sub">Next-Gen Smart Home Appliances</div></div>
    <div><div class="label">Alison Lee</div><div class="sub">Head of Product Design</div></div>
    <div class="mt-a" style="margin-left:auto"><div class="sub">[Company Logo]</div></div>
  </div>
</section>
```

## 2. Agenda (headline left, divided list right)

```html
<section class="slide surf-accent">
  <div class="head"><span class="kicker">Project Name</span><span class="pageno">01</span></div>
  <div class="body row center-v">
    <h1 class="h1 grow rise">Agenda</h1>
    <div class="list-divided grow rise">
      <div>Project Overview &amp; Objectives</div>
      <div>Milestones &amp; Status</div>
      <div>Timeline</div>
      <div>Budget</div>
      <div>Issues &amp; Risks</div>
      <div>Next Steps</div>
    </div>
  </div>
</section>
```

## 3. Overview + team grid (two columns)

```html
<section class="slide surf-ink">
  <div class="head"><span class="kicker">Project Name</span><span class="pageno">02</span></div>
  <div class="body grid-2">
    <div class="col gap-m">
      <h2 class="h2 rise">Project overview</h2>
      <p class="text rise" style="max-width:34ch">Project Aero aims to revolutionize the smart home industry with a new line of intelligent, energy-efficient appliances.</p>
      <p class="text dim" style="max-width:34ch">Designed to integrate seamlessly with existing ecosystems, improving efficiency and elevating the experience.</p>
    </div>
    <div class="col gap-m">
      <span class="eyebrow">January 2025 – March 2027</span>
      <div class="grid-2 gap-m">
        <div><div class="text" style="font-weight:600">Alison Lee</div><div class="text dim">Head of Product Design</div></div>
        <div><div class="text" style="font-weight:600">Emma Chen</div><div class="text dim">Project Lead</div></div>
        <div><div class="text" style="font-weight:600">Liam Patel</div><div class="text dim">Lead Designer</div></div>
        <div><div class="text" style="font-weight:600">Sarah Lopez</div><div class="text dim">Mechanical Engineer</div></div>
      </div>
    </div>
  </div>
</section>
```

## 4. Big-number stat cards

Cards use `card-fill` (theme fill color) with serif numerals, so they read as the accent regardless of host surface. Put the descriptive text above the cards.

```html
<section class="slide surf-paper">
  <div class="head"><span class="kicker">Project Name</span><span class="pageno">03</span></div>
  <div class="body gap-l">
    <h1 class="h1 rise">Objectives and Goals</h1>
    <div class="grid-3 rise">
      <div class="col gap-s">
        <div class="text" style="font-weight:600">Improve Energy Efficiency</div>
        <p class="text dim">Advanced energy-saving modes that optimize performance based on usage.</p>
        <div class="card-fill stat col" style="padding:24px; margin-top:8px">
          <div class="stat-label">Reduced Energy Use</div>
          <div class="serif-num">20%</div>
        </div>
      </div>
      <div class="col gap-s">
        <div class="text" style="font-weight:600">Increase Market Penetration</div>
        <p class="text dim">Partner with at least three major retail chains across regions.</p>
        <div class="card-fill stat col" style="padding:24px; margin-top:8px">
          <div class="stat-label">Market Share</div>
          <div class="serif-num">15%</div>
        </div>
      </div>
      <div class="col gap-s">
        <div class="text" style="font-weight:600">Promote Sustainability</div>
        <p class="text dim">Obtain Energy Star certification for the entire product line.</p>
        <div class="card-fill stat col" style="padding:24px; margin-top:8px">
          <div class="stat-label">Recycled Material</div>
          <div class="serif-num">30%+</div>
        </div>
      </div>
    </div>
  </div>
</section>
```

Single hero metric variant: one `serif-num` at ~160px on an `surf-ink` or `surf-accent` slide with a short caption. Use for a single powerful number.

## 5. Milestone / image grid

```html
<section class="slide surf-accent">
  <div class="head"><span class="kicker">Project Name</span><span class="pageno">04</span></div>
  <div class="body row gap-l">
    <h1 class="h1 rise" style="flex:0 0 26%">Milestones Achieved</h1>
    <div class="grid-3 grow rise">
      <div class="col gap-s"><div class="ph"></div><div class="eyebrow">UI Designs Finalized</div><p class="text">Consensus among stakeholders on final iterations.</p></div>
      <div class="col gap-s"><div class="ph"></div><div class="eyebrow">Energy Feature Shipped</div><p class="text">Extensive testing validated the energy-saving features.</p></div>
      <div class="col gap-s"><div class="ph"></div><div class="eyebrow">Retail Partners Secured</div><p class="text">Logistics and distribution finalized for rollout.</p></div>
    </div>
  </div>
</section>
```

Replace `<div class="ph"></div>` with `<img>` when the user provides real images. Keep aspect ratio with `style="aspect-ratio:3/4;object-fit:cover;width:100%"`.

## 6. Timeline (pills + node dots)

```html
<section class="slide surf-paper">
  <div class="head"><span class="kicker">Project Name</span><span class="pageno">06</span></div>
  <div class="body gap-m">
    <h1 class="h1 rise">Timeline</h1>
    <div class="timeline grow rise">
      <div class="grid-4"><span class="pill">Q1 2026</span><span class="pill">Q2 2026</span><span class="pill">Q3 2026</span><span class="pill">Q4 2026</span></div>
      <div class="track"><span class="node" style="left:0%"></span><span class="node" style="left:33.3%"></span><span class="node" style="left:66.6%"></span><span class="node" style="left:100%;margin-left:-10px"></span></div>
      <div class="grid-4">
        <ul class="text dim" style="list-style:none"><li>Complete UI concepts</li><li>Finalize energy algorithms</li><li>Secure two retail chains</li></ul>
        <ul class="text dim" style="list-style:none"><li>Initial efficiency tests</li><li>Customer service system</li><li>Begin Energy Star cert</li></ul>
        <ul class="text dim" style="list-style:none"><li>Refined prototype tests</li><li>Feedback tracking</li><li>Voice control dev</li></ul>
        <ul class="text dim" style="list-style:none"><li>Launch campaign</li><li>Expand partnerships</li><li>Finalize suppliers</li></ul>
      </div>
    </div>
  </div>
</section>
```

## 7. Next steps (columns with left rule)

```html
<section class="slide surf-accent">
  <div class="head"><span class="kicker">Project Name</span><span class="pageno">09</span></div>
  <div class="body gap-l">
    <h1 class="h1 rise">Next Steps</h1>
    <div class="grid-4 rise">
      <div class="bordered col gap-s"><div class="h2" style="font-size:24px">Consult Stakeholders</div><p class="text">Gather feedback from department heads and SMEs on prototype results.</p></div>
      <div class="bordered col gap-s"><div class="h2" style="font-size:24px">Production Planning</div><p class="text">Assess readiness, identify bottlenecks, optimize processes.</p></div>
      <div class="bordered col gap-s"><div class="h2" style="font-size:24px">Service Training</div><p class="text">Prepare the customer service team for launch.</p></div>
      <div class="bordered col gap-s"><div class="h2" style="font-size:24px">Refine Marketing</div><p class="text">Reconvene the team to review and refine strategy.</p></div>
    </div>
  </div>
</section>
```

## 8. Q&A / contact

```html
<section class="slide surf-brand">
  <div class="body row center-v gap-l">
    <h1 class="display rise" style="flex:0 0 30%">Q&amp;A</h1>
    <div class="grid-2 grow rise">
      <div><div class="label" style="color:var(--s-head);font-size:22px">Alison Lee</div><div class="text" style="font-weight:600">alison@company.com</div><div class="text dim">Head of Product Design</div></div>
      <div><div class="label" style="color:var(--s-head);font-size:22px">Emma Chen</div><div class="text" style="font-weight:600">emma@company.com</div><div class="text dim">Project Lead</div></div>
    </div>
  </div>
</section>
```

## 9. Section break

A single word or short phrase on an `surf-accent` or `surf-brand` slide. Big serif, optional number, lots of air. Use to chapter a long deck.

```html
<section class="slide surf-brand">
  <div class="body"><div class="col gap-m rise">
    <span class="eyebrow" style="color:var(--s-accent)">Part Two</span>
    <h1 class="display" style="font-size:84px">Strategy</h1>
    <p class="lead" style="max-width:34ch">A one-line framing for the section ahead.</p>
  </div></div>
</section>
```

Keep section breaks **left-aligned**, consistent with the rest of the deck. The body already centers content vertically, so just omit `center-v` (which would also center horizontally and makes the cover read as oddly floating mid-slide). Critically, **do not put a `max-width` on the column that holds the `display` headline** — at that type size a narrow column forces even a short headline to wrap into slivers and reads as broken. Let the headline take its natural width, and constrain only the supporting `lead` line (e.g. `max-width:34ch`) so it wraps comfortably.

---

## Composition guidance

- **Vary the headline side.** Some slides lead with the headline on the left and detail on the right; others stack. Avoid every slide looking identical.
- **One idea per slide.** If a slide has two ideas, split it.
- **Short text.** Headlines are phrases, body is tight. No paragraphs longer than ~3 lines. No bullet walls — prefer divided lists or short statements.
- **Let whitespace breathe.** Resist filling the canvas. Negative space is the look.
- **Numerals are serif.** Stats, percentages, years rendered in the serif read as editorial.
- **Pick a page-number scheme** (e.g. `01`, `02`) and a fixed kicker (the project/deck name) and keep them consistent across content slides.
