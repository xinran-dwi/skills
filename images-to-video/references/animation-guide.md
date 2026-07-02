# Animation guide — authoring scenes for the trailer

The trailer plays a sequence of **scenes**. Each scene is a full-frame SVG whose
elements animate in, one by one, when the scene becomes active. Then it fades to
the next scene and loops. This is the per-element "draw-on" look — different from
crossfading whole flat images.

## The three animation classes

Add these to individual SVG elements. Each reads a `--d` (delay) so elements
stagger; `.draw` also needs a `--len` (dash length ≈ the path/line length).

| Class | Effect | Required style | Use on |
|-------|--------|----------------|--------|
| `draw` | line/path draws itself on | `--len:<length>;--d:<delay>s` | `<line>`, `<path>` |
| `fade` | fades up + rises 8px | `--d:<delay>s` | anything (boxes, text, dots) |
| `pop`  | scales/pops in | `--d:<delay>s` | `<circle>` dots, `<g>` marks |

`--len` for a straight line = its pixel length; for a curved path, use a value
slightly larger than the path length (overshooting is fine — it just starts fully
hidden). Delays are cumulative timing within the scene, e.g. `.0s, .2s, .35s...`.

### Example scene (hand-tagged for the real draw-on look)

```svg
<svg viewBox="245 105 710 400" preserveAspectRatio="xMidYMid meet">
  <line class="draw" style="--len:520;--d:0s"   x1="340" y1="350" x2="860" y2="350" stroke="#1b1b19" stroke-width="1.75"/>
  <path class="draw" style="--len:360;--d:.35s" d="M480 350 C 520 350 532 270 575 270 L 690 270" fill="none" stroke="#1b1b19" stroke-width="1.75"/>
  <circle class="pop" style="--d:.55s" cx="600" cy="270" r="6" fill="none" stroke="#1b1b19" stroke-width="1.75"/>
  <text class="fade" style="--d:.2s" x="360" y="338" font-size="15" fill="#a3a199">main</text>
</svg>
```

## Turning a newsletter-diagram SVG into a scene

The newsletter-diagram skill emits static monochrome SVGs — perfect scene source.
To animate one:

1. Keep the `viewBox` (or tighten it to zoom the diagram — e.g. `245 125 710 400`
   frames the content larger and centered).
2. Delete the white background `<rect>` (the stage is already white; the build
   script also strips it automatically).
3. Tag elements: `fade` on boxes/labels, `pop` on dots, `draw` on the connector
   lines/arrows. Order the `--d` delays so the diagram builds in a sensible
   reading order (structure first, then dots, then labels).

If you just want a quick result, skip the manual tagging and let the build script
add a staggered **fade-in to every element** with `--auto` — it won't line-draw,
but each element still appears in sequence.

## Timing

- Per-scene hold: ~2.2s is punchy; ~3s is calmer. Keep animation delays inside the
  hold so everything finishes before the cut (last `--d` + ~0.8s < hold).
- The bottom progress bar auto-matches the total loop length.

## Colors (fixed, since it's a standalone file)

Match the newsletter-diagram palette: ink `#1b1b19`, secondary `#6c6b64`,
tertiary `#a3a199`, hairline `#c9c7be`, emphasis border `#9a988f`, white stage.
These are baked in (not theme variables) because the output is a self-contained
page on a white stage.

## Recording it to video/GIF

The output is HTML that plays in a browser — it is not itself a video file
(CSS/JS animation needs a browser to run). To get a shareable clip:

1. Open the `.html` full-screen in Chrome (F11).
2. Screen-record one full loop (macOS Cmd+Shift+5, Windows Win+G).
3. Optionally convert the recording to GIF at ezgif.com, or keep it as MP4.

For a pixel-perfect render without screen-recording, run the HTML through a
headless-browser capturer on your own machine (e.g. `timecut` or a small
Puppeteer + ffmpeg script) — that isn't available inside this sandbox.

## Image fallback

If you only have flat PNGs (no vector source), the build script's `--images`
mode crossfades them as whole pictures (optional slow zoom with `--zoom`). There's
no per-element draw-on in this mode — a flat image has no separate parts to
animate. Prefer SVG scenes whenever you have them.
