# Style reference — copy-and-adapt SVG snippets

All snippets assume a 900px-wide canvas and the fixed palette from SKILL.md:

```
ink     #1b1b19    secondary #6c6b64    tertiary #a3a199
hair-lt #e2e0d8    hair-md   #c9c7be    active   #9a988f    bg #ffffff
font: 'DejaVu Sans Mono','Liberation Mono',monospace
```

Always start the SVG with a white background rect, and set explicit
`width`/`height` so the renderer can scale:

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="360" viewBox="0 0 900 360">
<rect x="0" y="0" width="900" height="360" fill="#ffffff"/>
<!-- content -->
</svg>
```

## Panel frame (for UI mockups)

A hairline-bordered card with a header row, a divider, and a body. Near-square
corners (`rx="6"`).

```svg
<rect x="30" y="30" width="840" height="300" rx="6" fill="#ffffff" stroke="#c9c7be" stroke-width="1"/>
<text x="58" y="68" font-family="'DejaVu Sans Mono',monospace" font-size="19" fill="#1b1b19">styles.css</text>
<text x="842" y="66" text-anchor="end" font-family="'DejaVu Sans Mono',monospace" font-size="13" fill="#a3a199" letter-spacing="0.5">conflict 1 of 1</text>
<line x1="30" y1="92" x2="870" y2="92" stroke="#e2e0d8" stroke-width="1"/>
```

## Dot timeline with a branch and merge

Solid dots = landed on the main line; hollow dots = branch work in progress.
Solid lines for established paths; a dashed line for an attempt/blocked merge.

```svg
<!-- main line -->
<line x1="96" y1="120" x2="600" y2="120" stroke="#1b1b19" stroke-width="1"/>
<!-- branch up, then merge back down -->
<path d="M170 120 C 210 120 220 56 260 56 L 330 56" fill="none" stroke="#1b1b19" stroke-width="1"/>
<path d="M330 56 C 388 56 398 120 430 120" fill="none" stroke="#1b1b19" stroke-width="1"/>
<!-- branch down + dashed (blocked) attempt -->
<path d="M170 120 C 210 120 220 184 260 184 L 348 184" fill="none" stroke="#1b1b19" stroke-width="1"/>
<path d="M348 184 C 420 182 452 132 498 124" fill="none" stroke="#1b1b19" stroke-width="1" stroke-dasharray="4 4"/>
<!-- solid (landed) dots -->
<circle cx="170" cy="120" r="4" fill="#1b1b19"/>
<circle cx="430" cy="120" r="4" fill="#1b1b19"/>
<!-- hollow (in-progress) dots -->
<circle cx="295" cy="56" r="4" fill="none" stroke="#1b1b19" stroke-width="1"/>
<circle cx="300" cy="184" r="4" fill="none" stroke="#1b1b19" stroke-width="1"/>
<!-- labels: lowercase, letter-spaced -->
<text x="44" y="124" font-family="'DejaVu Sans Mono',monospace" font-size="12" fill="#6c6b64" letter-spacing="0.04em">main</text>
```

## Conflict markers (code block)

Marker lines (`<<<<<<<`, `=======`, `>>>>>>>`) in tertiary; real code in ink.
Line numbers right-aligned in tertiary. Remember to HTML-escape `<` and `>`.
Line-height ~30px at 15px text.

```svg
<text x="88"  y="122" text-anchor="end" font-family="'DejaVu Sans Mono',monospace" font-size="14" fill="#a3a199">11</text>
<text x="104" y="122" font-family="'DejaVu Sans Mono',monospace" font-size="15" fill="#1b1b19">.site-header {</text>
<text x="88"  y="152" text-anchor="end" font-family="'DejaVu Sans Mono',monospace" font-size="14" fill="#a3a199">12</text>
<text x="104" y="152" font-family="'DejaVu Sans Mono',monospace" font-size="15" fill="#a3a199">&lt;&lt;&lt;&lt;&lt;&lt;&lt; redesign-header</text>
<text x="104" y="182" font-family="'DejaVu Sans Mono',monospace" font-size="15" fill="#1b1b19">  padding: 24px 32px;</text>
<text x="104" y="212" font-family="'DejaVu Sans Mono',monospace" font-size="15" fill="#a3a199">=======</text>
<text x="104" y="242" font-family="'DejaVu Sans Mono',monospace" font-size="15" fill="#1b1b19">  background: var(--bg-dark);</text>
<text x="104" y="272" font-family="'DejaVu Sans Mono',monospace" font-size="15" fill="#a3a199">&gt;&gt;&gt;&gt;&gt;&gt;&gt; main</text>
```

## Buttons (one active, one locked)

The active button gets the slightly darker `active` border so the eye lands on
it; a locked/disabled button uses the faint hairline and tertiary text.

```svg
<!-- active -->
<rect x="58" y="244" width="200" height="44" rx="4" fill="none" stroke="#9a988f" stroke-width="1"/>
<text x="158" y="272" text-anchor="middle" font-family="'DejaVu Sans Mono',monospace" font-size="14" fill="#1b1b19">resolve conflicts</text>
<!-- locked -->
<rect x="274" y="244" width="190" height="44" rx="4" fill="none" stroke="#e2e0d8" stroke-width="1"/>
<text x="369" y="272" text-anchor="middle" font-family="'DejaVu Sans Mono',monospace" font-size="14" fill="#a3a199">merge pull request</text>
```

## Tag / pill (hairline, never filled)

```svg
<rect x="58" y="100" width="58" height="26" rx="3" fill="none" stroke="#c9c7be" stroke-width="1"/>
<text x="87" y="118" text-anchor="middle" font-family="'DejaVu Sans Mono',monospace" font-size="12" fill="#6c6b64" letter-spacing="0.5">open</text>
```

## Warning triangle

```svg
<path d="M70 172 L82 194 L58 194 Z" fill="none" stroke="#1b1b19" stroke-width="1" stroke-linejoin="round"/>
<line x1="70" y1="179" x2="70" y2="186" stroke="#1b1b19" stroke-width="1"/>
<circle cx="70" cy="189.5" r="0.8" fill="#1b1b19"/>
```

## Conflict / error mark (✕) with a leader to a label

```svg
<line x1="503" y1="115" x2="515" y2="127" stroke="#1b1b19" stroke-width="1.5"/>
<line x1="515" y1="115" x2="503" y2="127" stroke="#1b1b19" stroke-width="1.5"/>
<line x1="509" y1="132" x2="509" y2="150" stroke="#a3a199" stroke-width="0.5"/>
<text x="509" y="166" text-anchor="middle" font-family="'DejaVu Sans Mono',monospace" font-size="11" fill="#1b1b19" letter-spacing="0.04em">merge conflict</text>
```

## Layout tips

- Monospace advance ≈ 0.6 × font-size px per char. A 29-char line at 15px ≈
  261px wide — size boxes and place right-edge labels from that.
- Right-aligned side labels (`text-anchor="end"`) must align to the *baseline of
  the line they annotate*. After rendering, view the PNG and confirm — a label
  one line off is the most common slip.
- Keep element count low. If it feels busy, remove something rather than
  shrinking everything.
- For pure diagrams, no panel frame is needed — strokes + labels on the white
  canvas read as a clean technical drawing.
