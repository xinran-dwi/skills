#!/usr/bin/env python3
"""
build_trailer.py — assemble animated SVG scenes (or images) into a single,
self-playing, looping HTML trailer in the minimalist monochrome-hairline style.

The output is one standalone .html file. Open it in a browser and it plays on a
loop; screen-record one cycle to get a video/GIF.

Three ways to use it
--------------------
1) SVG scenes with auto per-element fade-in (quickest; works on plain diagram SVGs):
     python3 build_trailer.py --svgs a.svg b.svg c.svg --auto \
       --out /mnt/user-data/outputs/trailer.html --seconds 2.2

2) Images (whole-picture crossfade; use when you only have PNGs):
     python3 build_trailer.py --images a.png b.png --out trailer.html --seconds 2.5

3) Full control via a JSON manifest (mix scene types, set line-draw, viewBox, timing):
     python3 build_trailer.py --manifest scenes.json --out trailer.html

   scenes.json:
   {
     "stage_width": 960, "bg": "#ffffff", "loop": true,
     "scenes": [
       {"svg": "s1.svg", "dur": 2200, "auto": true},
       {"svg": "s2.svg", "dur": 2200, "viewBox": "245 105 710 400"},
       {"image": "s3.png", "dur": 2500, "zoom": true}
     ]
   }

For the real line-draw / pop effect, pre-tag elements in the scene SVG with the
classes below (see references/animation-guide.md); --auto only adds staggered
fade-in, not line-draw:
  class="draw"  style="--len:<len>;--d:<delay>s"   line/path draws itself on
  class="fade"  style="--d:<delay>s"               element fades + rises in
  class="pop"   style="--d:<delay>s"               element scales/pops in
"""
import argparse
import json
import os
import re
import sys

PRIMITIVES = ("line", "rect", "circle", "ellipse", "path", "polyline", "polygon", "text", "g")


def read(path):
    with open(path) as f:
        return f.read()


def svg_parts(svg_text):
    """Return (viewBox, inner_body) from a full <svg>...</svg> string."""
    vb = re.search(r'<svg[^>]*\bviewBox="([^"]+)"', svg_text)
    viewbox = vb.group(1) if vb else "0 0 1200 675"
    inner = re.sub(r'^.*?<svg[^>]*>', '', svg_text, count=1, flags=re.S)
    inner = re.sub(r'</svg>\s*$', '', inner, flags=re.S)
    # drop a background rect if the diagram painted one (the stage is already white)
    inner = re.sub(r'<rect[^>]*fill="#ffffff"[^>]*/>\s*', '', inner, count=1)
    return viewbox, inner.strip()


def auto_fade(inner, step=0.12):
    """Add a staggered fade-in to each top-level primitive that has no class yet."""
    counter = {"i": 0}

    def add(m):
        tag = m.group(1)
        rest = m.group(2)
        if "class=" in rest:
            return m.group(0)
        d = round(counter["i"] * step, 3)
        counter["i"] += 1
        return f'<{tag} class="fade" style="--d:{d}s"{rest}'

    return re.sub(r'<(' + "|".join(PRIMITIVES) + r')(\s[^>]*?)(?=/?>)', add, inner)


def scene_html_svg(svg_path, dur, viewbox=None, auto=False, step=0.12):
    vb, inner = svg_parts(read(svg_path))
    if viewbox:
        vb = viewbox
    if auto:
        inner = auto_fade(inner, step)
    return (f'  <section class="scene" data-dur="{int(dur)}">\n'
            f'    <svg viewBox="{vb}" preserveAspectRatio="xMidYMid meet">{inner}</svg>\n'
            f'  </section>')


def scene_html_image(img_path, dur, zoom=False):
    cls = "kb" if zoom else ""
    return (f'  <section class="scene" data-dur="{int(dur)}">\n'
            f'    <img class="{cls}" src="{img_path}" alt="">\n'
            f'  </section>')


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>trailer</title>
<style>
  :root{{ --ink:#1b1b19; --sec:#6c6b64; --ter:#a3a199; --hair2:#c9c7be;
          --mono: ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,"DejaVu Sans Mono",monospace; }}
  *{{box-sizing:border-box;}} html,body{{height:100%;margin:0;}}
  body{{background:#ECEAE3;display:flex;align-items:center;justify-content:center;font-family:var(--mono);}}
  .stage{{position:relative;width:min(94vw,{STAGE_W}px);aspect-ratio:16/9;background:{BG};
          border:1px solid var(--hair2);border-radius:12px;overflow:hidden;
          box-shadow:0 18px 60px rgba(27,27,25,.12);}}
  .stage svg text{{font-family:var(--mono);}}
  .progress{{position:absolute;left:0;bottom:0;height:3px;background:var(--ink);width:0;
             animation:prog {TOTAL_MS}ms linear infinite;z-index:6;}}
  @keyframes prog{{from{{width:0}} to{{width:100%}}}}
  .scene{{position:absolute;inset:0;opacity:0;}}
  .scene.active{{opacity:1;transition:opacity .4s ease;}}
  .scene svg{{position:absolute;inset:0;width:100%;height:100%;display:block;}}
  .scene img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:{BG};}}
  .scene.active img.kb{{transform:scale(1.06);transition:transform 6s ease;}}
  .draw{{stroke-dasharray:var(--len,900);stroke-dashoffset:var(--len,900);}}
  .scene.active .draw{{stroke-dashoffset:0;transition:stroke-dashoffset .75s ease var(--d,0s);}}
  .fade{{opacity:0;transform:translateY(8px);}}
  .scene.active .fade{{opacity:1;transform:none;transition:opacity .55s ease var(--d,0s),transform .55s ease var(--d,0s);}}
  .pop{{opacity:0;transform:scale(.1);transform-box:fill-box;transform-origin:center;}}
  .scene.active .pop{{opacity:1;transform:scale(1);transition:opacity .4s ease var(--d,0s),transform .5s cubic-bezier(.2,1.35,.4,1) var(--d,0s);}}
</style>
</head>
<body>
<div class="stage">
  <div class="progress"></div>
{SCENES}
</div>
<script>
  var scenes = Array.from(document.querySelectorAll('.scene'));
  var loopOn = {LOOP};
  var i = 0;
  function tick(){{
    scenes.forEach(function(s,k){{ s.classList.toggle('active', k === i); }});
    var dur = parseInt(scenes[i].dataset.dur, 10) || 2200;
    var next = i + 1;
    if(next >= scenes.length && !loopOn) return;
    i = next % scenes.length;
    setTimeout(tick, dur);
  }}
  tick();
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description="Build a self-playing animated HTML trailer.")
    ap.add_argument("--manifest", help="JSON manifest describing scenes")
    ap.add_argument("--svgs", nargs="*", default=[], help="SVG scene files (quick mode)")
    ap.add_argument("--images", nargs="*", default=[], help="Image files (quick crossfade mode)")
    ap.add_argument("--out", required=True, help="Output .html path")
    ap.add_argument("--seconds", type=float, default=2.2, help="Default per-scene hold (default 2.2)")
    ap.add_argument("--auto", action="store_true", help="Auto staggered fade-in for --svgs")
    ap.add_argument("--zoom", action="store_true", help="Slow zoom on --images (ken burns)")
    ap.add_argument("--stage-width", type=int, default=960, help="Stage max width px (default 960)")
    ap.add_argument("--bg", default="#ffffff", help="Stage background (default white)")
    ap.add_argument("--no-loop", action="store_true", help="Play once instead of looping")
    args = ap.parse_args()

    scenes_cfg = []
    stage_w, bg, loop = args.stage_width, args.bg, not args.no_loop

    if args.manifest:
        m = json.load(open(args.manifest))
        stage_w = m.get("stage_width", stage_w)
        bg = m.get("bg", bg)
        loop = m.get("loop", loop)
        scenes_cfg = m["scenes"]
    else:
        for p in args.svgs:
            scenes_cfg.append({"svg": p, "dur": args.seconds * 1000, "auto": args.auto})
        for p in args.images:
            scenes_cfg.append({"image": p, "dur": args.seconds * 1000, "zoom": args.zoom})

    if not scenes_cfg:
        raise SystemExit("No scenes. Use --svgs, --images, or --manifest.")

    blocks, total = [], 0
    for sc in scenes_cfg:
        dur = sc.get("dur", args.seconds * 1000)
        total += dur
        if "svg" in sc:
            if not os.path.exists(sc["svg"]):
                raise SystemExit(f"Missing svg: {sc['svg']}")
            blocks.append(scene_html_svg(sc["svg"], dur, sc.get("viewBox"),
                                         sc.get("auto", False), sc.get("step", 0.12)))
        elif "image" in sc:
            if not os.path.exists(sc["image"]):
                raise SystemExit(f"Missing image: {sc['image']}")
            blocks.append(scene_html_image(sc["image"], dur, sc.get("zoom", False)))
        else:
            raise SystemExit(f"Scene needs 'svg' or 'image': {sc}")

    html = TEMPLATE.format(STAGE_W=stage_w, BG=bg, TOTAL_MS=int(total),
                           SCENES="\n".join(blocks), LOOP="true" if loop else "false")
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        f.write(html)
    print(f"wrote {args.out}  ({len(scenes_cfg)} scenes, ~{total/1000:.1f}s loop)")


if __name__ == "__main__":
    main()
