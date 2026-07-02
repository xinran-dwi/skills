---
name: images-to-video
description: >-
  Build a self-playing, looping ANIMATED HTML trailer from a set of diagrams or
  SVG scenes, in the minimalist monochrome-hairline-monospace style, where each
  element draws, fades, or pops in individually (per-element motion). The output
  is one standalone .html file that plays in a browser and is meant to be
  screen-recorded into a video/GIF. Use WHENEVER the user wants an animated
  trailer, teaser, reel, explainer animation, or an "animated version" of
  diagrams — e.g. "turn these diagrams into an animated trailer", "animate my
  diagrams", "make an animated html", "images to animated html", "a trailer that
  draws the lines in", "a looping motion graphic from my diagrams". The real
  per-element draw-on effect needs vector SVG scenes; flat PNGs can only fade as
  whole pictures. This outputs the animated HTML to record — it does not itself
  render a finished MP4/GIF (that needs a browser to capture).
---

# Images to Video (animated HTML trailer)

Assemble a sequence of scenes into one self-playing, looping HTML page in the
minimalist monochrome-hairline-monospace style. Each scene's elements animate in
individually — lines draw themselves on, dots pop, boxes and labels fade up — then
the scene fades to the next. A hairline progress bar tracks the loop.

The deliverable is a standalone `.html` file. It plays in any browser; the user
screen-records one loop to get a video/GIF. (It is not itself a video — CSS/JS
animation must run in a browser to be captured.)

## When to use

Trigger for: "animated trailer/teaser/reel", "animate my diagrams", "make an
animated html", "a trailer that draws the lines in", "motion graphic", "animated
version of these diagrams". The signal is **motion authored per element**, output
as HTML.

## Source: SVG scenes (needed for the draw-on look)

Per-element draw-on animation requires **vector SVG** scenes — a flat PNG has no
separate parts to animate. This pairs directly with the `newsletter-diagram`
skill, whose static monochrome SVG diagrams are the ideal scene source. (If only
flat PNGs exist, the script can still fade between them as whole pictures via
`--images`, but there's no per-element draw-on.)

## Workflow

1. **Get or make the scenes as SVG.** Use the user's diagram SVGs, or generate
   them with `newsletter-diagram` first. Aim for 3–6 scenes.

2. **Choose animation depth:**
   - Quick: pass the SVGs with `--auto` — adds a staggered fade-in to every
     element (each appears in sequence; no line-draw).
   - Full effect: hand-tag elements in each scene SVG with `draw` / `fade` / `pop`
     classes and `--d` / `--len` styles (see `references/animation-guide.md`),
     then build without `--auto`. This produces the signature draw-on look.

3. **Build the HTML:**
   ```bash
   # quick, from plain diagram SVGs
   python3 scripts/build_trailer.py --svgs s1.svg s2.svg s3.svg --auto \
     --seconds 2.2 --out /mnt/user-data/outputs/trailer.html

   # full control (line-draw, per-scene viewBox/timing, mixed scene types)
   python3 scripts/build_trailer.py --manifest scenes.json \
     --out /mnt/user-data/outputs/trailer.html
   ```

4. **Deliver + explain recording.** `present_files` the `.html`. Tell the user to
   open it full-screen (Chrome, F11) and screen-record one loop (macOS
   Cmd+Shift+5 / Windows Win+G), then optionally convert to GIF at ezgif.com.
   You can also preview the animation inline first with the visualizer widget.

## Script options (scripts/build_trailer.py)

| Flag | Meaning |
|------|---------|
| `--svgs a.svg b.svg …` | Quick mode: SVG scenes in order |
| `--auto` | Staggered fade-in on every element of each `--svgs` scene |
| `--manifest file.json` | Full control (see below) |
| `--images a.png b.png …` | Fallback: fade between flat images (no draw-on) |
| `--zoom` | Slow ken-burns zoom on `--images` |
| `--seconds` | Per-scene hold (default 2.2) |
| `--stage-width` | Stage max width px (default 960) |
| `--bg` | Stage background (default `#ffffff`) |
| `--no-loop` | Play once instead of looping |
| `--out` | Output `.html` (required) |

### Manifest (per-scene control)

```json
{
  "stage_width": 960, "bg": "#ffffff", "loop": true,
  "scenes": [
    {"svg": "s1.svg", "dur": 2200, "auto": true},
    {"svg": "s2.svg", "dur": 2200, "viewBox": "245 105 710 400"},
    {"svg": "s3.svg", "dur": 2200}
  ]
}
```

`viewBox` (optional) tightens/zooms a scene centered on its content; omit to keep
the SVG's own.

## Animation vocabulary (hand-tagged scenes)

On individual SVG elements:
- `class="draw" style="--len:<len>;--d:<delay>s"` — line/path draws itself on
- `class="fade" style="--d:<delay>s"` — element fades up and rises in
- `class="pop"  style="--d:<delay>s"` — element scales/pops in

Order the `--d` delays to build each scene in reading order (structure → dots →
labels), keeping the last delay + ~0.8s under the scene's hold. Full details,
examples, and how to tag a newsletter-diagram SVG are in
`references/animation-guide.md`.

## Honest limits

- Per-element draw-on requires **vector SVG** scenes; flat images can only fade.
- This skill outputs **HTML**, not a video file. Screen-record it (or run it
  through a headless-browser capturer on your own machine) to get an MP4/GIF.

## Pairs well with

`newsletter-diagram` makes the monochrome SVG diagrams → this skill turns them
into the looping animated HTML trailer.
