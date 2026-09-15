#!/usr/bin/env python3
"""
Measure a design export — colors and element rects — in design pixels, and
compare a rendered build against it.

Why this exists: a design export is usually a screenshot of an artboard, and
screenshots from design tools carry a display ICC profile, so their raw pixel
values are NOT sRGB. Reading them straight gives colors 5-10 levels off, which
is enough to build an entire palette wrong while believing it was measured.
Every command here converts to sRGB first.

Second reason: the artboard sits on a canvas at an arbitrary zoom. `locate`
finds it and returns the mapping, so every number printed is in design px and
compares directly to CSS.

Usage
  measure-ref.py locate  <image> [--design 390x844]
  measure-ref.py colors  <image> --view mobile [--points name:x,y ...]
  measure-ref.py medians <image> --view mobile --region x,y,w,h [...]
  measure-ref.py edges   <image> --view mobile --at x,y
  measure-ref.py crop    <image> --view mobile --rect x,y,w,h --out FILE
  measure-ref.py compare <reference> <screenshot> --view mobile [--tolerance 5]

`compare` is the color check an eyeball pass cannot do: it samples both images
at the same design coordinates and prints per-channel deltas, exiting non-zero
past the tolerance so it can gate a commit. Build screenshots (Playwright, etc.)
are already sRGB and already 1:1 with the design — `compare` treats the
screenshot side as flat automatically.

Views and sample points come from a samples.json next to the references:

  {
    "mobile":  { "design": [390, 844],  "points": { "page-top": [195, 20] } },
    "desktop": { "design": [1440, 931], "points": { "panel-top": [1430, 140] } }
  }

(a top-level "views" wrapper works too). Keep every point inside a flat region,
off text strokes and photography — a point that lands on a glyph measures
antialiasing, not a token.

Needs Python 3 + Pillow. No dependency is added to the project being checked.
"""

import argparse
import io
import json
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageCms

SAMPLES_CANDIDATES = ("design-refs/samples.json", "samples.json")


# ---------------------------------------------------------------- color space


def load_srgb(path):
    """Open an image and convert it out of its embedded display profile into sRGB."""
    im = Image.open(path)
    icc = im.info.get("icc_profile")
    im = im.convert("RGB")
    if icc:
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        dst = ImageCms.createProfile("sRGB")
        im = ImageCms.profileToProfile(im, src, dst, outputMode="RGB")
    return im


def hexof(c):
    return "#%02x%02x%02x" % tuple(c[:3])


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def delta(a, b):
    return tuple(int(x) - int(y) for x, y in zip(a, b))


# ---------------------------------------------------------------- samples file


def samples_path(explicit=None):
    if explicit:
        return Path(explicit)
    for c in SAMPLES_CANDIDATES:
        if Path(c).exists():
            return Path(c)
    return Path(SAMPLES_CANDIDATES[0])


def load_views(explicit=None):
    """Read samples.json into {view: {"design": [w, h], "points": {...}}}."""
    p = samples_path(explicit)
    if not p.exists():
        return {}
    data = json.loads(p.read_text())
    data = data.get("views", data)
    return {
        k: v
        for k, v in data.items()
        if not k.startswith("_") and isinstance(v, dict) and "design" in v
    }


def view_size(args):
    """Design size for this invocation: --design wins, else samples.json."""
    if getattr(args, "design", None):
        w, h = args.design.lower().split("x")
        return (float(w), float(h))
    views = load_views(getattr(args, "samples", None))
    view = getattr(args, "view", None)
    if view and view in views:
        return tuple(views[view]["design"])
    sys.exit(
        f"no design size: pass --design WxH, or add view '{view}' to "
        f"{samples_path(getattr(args, 'samples', None))}"
    )


def view_points(args):
    views = load_views(getattr(args, "samples", None))
    return dict(views.get(getattr(args, "view", None), {}).get("points", {}))


# ---------------------------------------------------------------- frame finding


def locate(im, design_w, design_h):
    """
    Find the artboard inside a design-tool canvas screenshot.

    The canvas is typically mid-grey and the artboard is not, so mask on
    "saturated or clearly darker/lighter than the surround" — in practice a
    blue-dominant dark mask covers the common dark-UI case. Returns
    (x0, y0, scale) mapping design px -> image px. Falls back to a flat 1:1
    mapping when nothing is found, i.e. the image is already just the artboard
    (a rendered build screenshot).
    """
    px = im.load()
    w, h = im.size

    def navy(c):
        return (c[2] - c[0]) > 25 and lum(c) < 110

    colf = [sum(1 for y in range(0, h, 2) if navy(px[x, y])) / (h / 2) for x in range(w)]
    rowf = [sum(1 for x in range(0, w, 2) if navy(px[x, y])) / (w / 2) for y in range(h)]
    xs = [x for x, f in enumerate(colf) if f > 0.3]
    ys = [y for y, f in enumerate(rowf) if f > 0.3]
    if not xs or not ys:
        return 0, 0, w / design_w

    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    if (x1 - x0 + 1) > w * 0.95 and (y1 - y0 + 1) > h * 0.95:
        return 0, 0, w / design_w
    return x0, y0, (x1 - x0 + 1) / design_w


class Frame:
    """An image plus the mapping from design px to its pixels."""

    def __init__(self, im, size, flat=False):
        self.im = im
        self.px = im.load()
        self.w, self.h = im.size
        self.design_w, self.design_h = size
        if flat:
            self.x0, self.y0, self.scale = 0, 0, self.w / self.design_w
        else:
            self.x0, self.y0, self.scale = locate(im, self.design_w, self.design_h)

    def at(self, dx, dy):
        x = round(self.x0 + dx * self.scale)
        y = round(self.y0 + dy * self.scale)
        x = max(0, min(self.w - 1, x))
        y = max(0, min(self.h - 1, y))
        return self.px[x, y]

    def describe(self):
        return (
            f"origin ({self.x0}, {self.y0})  scale {self.scale:.4f}  "
            f"-> design {self.w / self.scale:.0f} x {self.h / self.scale:.0f}"
        )


# ---------------------------------------------------------------- measurement


def edges(frame, dx, dy, tol=26):
    """
    Find the rect of the element under (dx, dy) by walking out along both axes
    until the color stops matching the element's fill.

    Scanning a center line rather than counting matching pixels per row is
    deliberate: density banding clips antialiased rounded corners and
    under-measures every card.
    """
    fill = frame.at(dx, dy)

    def same(c):
        return sum(abs(int(a) - int(b)) for a, b in zip(c, fill)) < tol

    left = dx
    while left > 0 and same(frame.at(left - 1, dy)):
        left -= 0.5
    right = dx
    while right < frame.design_w and same(frame.at(right + 1, dy)):
        right += 0.5
    top = dy
    while top > 0 and same(frame.at(dx, top - 1)):
        top -= 0.5
    bottom = dy
    while bottom < frame.design_h and same(frame.at(dx, bottom + 1)):
        bottom += 0.5

    return {
        "fill": hexof(fill),
        "x": round(left, 1),
        "y": round(top, 1),
        "w": round(right - left, 1),
        "h": round(bottom - top, 1),
    }


def median_color(frame, x, y, w, h, step=2):
    """Median color over a design-px region — the honest way to read a surface.

    A flat surface in an export varies by several levels between adjacent
    pixels, so one sampled pixel is not a color.
    """
    px = [
        frame.at(sx, sy)
        for sx in range(int(x), int(x + w), step)
        for sy in range(int(y), int(y + h), step)
    ]
    return tuple(round(statistics.median(c[i] for c in px)) for i in range(3))


# ---------------------------------------------------------------- commands


def cmd_locate(args):
    im = load_srgb(args.image)
    views = load_views(getattr(args, "samples", None))
    if args.design:
        sizes = {"(--design)": view_size(args)}
    elif views:
        sizes = {k: tuple(v["design"]) for k, v in views.items()}
    else:
        sys.exit("no samples.json found: pass --design WxH")
    for name, size in sizes.items():
        print(f"as {name:10s}: {Frame(im, size).describe()}")


def cmd_colors(args):
    f = Frame(load_srgb(args.image), view_size(args), flat=args.flat)
    print(f"# {Path(args.image).name} — {f.describe()}")
    points = view_points(args)
    for p in args.points or []:
        name, coord = p.split(":")
        x, y = coord.split(",")
        points[name] = [float(x), float(y)]
    if not points:
        sys.exit("no points: add them to samples.json or pass --points name:x,y")
    for name, (x, y) in points.items():
        print(f"  {name:22s} ({x:>6}, {y:>6})  {hexof(f.at(x, y))}")


def cmd_medians(args):
    f = Frame(load_srgb(args.image), view_size(args), flat=args.flat)
    print(f"# {Path(args.image).name} — {f.describe()}")
    for r in args.region:
        x, y, w, h = (float(v) for v in r.split(","))
        print(f"  {r:24s} {hexof(median_color(f, x, y, w, h))}")


def cmd_edges(args):
    f = Frame(load_srgb(args.image), view_size(args), flat=args.flat)
    x, y = (float(v) for v in args.at.split(","))
    r = edges(f, x, y)
    print(f"# {Path(args.image).name} — {f.describe()}")
    print(f"  at ({x}, {y}) fill {r['fill']}: x={r['x']} y={r['y']} w={r['w']} h={r['h']}")


def cmd_crop(args):
    """Cut a design-px rectangle out of an export at source resolution."""
    im = load_srgb(args.image)
    f = Frame(im, view_size(args))
    x, y, w, h = (float(v) for v in args.rect.split(","))
    box = (
        round(f.x0 + x * f.scale),
        round(f.y0 + y * f.scale),
        round(f.x0 + (x + w) * f.scale),
        round(f.y0 + (y + h) * f.scale),
    )
    out = im.crop(box)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.save(args.out, quality=92)
    print(f"  {args.out}  {out.size[0]}x{out.size[1]}px  (design {w:g}x{h:g})")


def cmd_compare(args):
    size = view_size(args)
    ref = Frame(load_srgb(args.reference), size)
    shot = Frame(load_srgb(args.screenshot), size, flat=True)
    points = view_points(args)
    if not points:
        sys.exit(
            f"no sample points for view '{args.view}' in "
            f"{samples_path(getattr(args, 'samples', None))}"
        )

    print(f"# reference  {Path(args.reference).name}  {ref.describe()}")
    print(f"# build      {Path(args.screenshot).name}  {shot.describe()}")
    print(f"\n{'point':22s} {'design':>14s}  {'design file':9s} {'build':9s} {'delta':>16s}")
    worst = 0
    for name, (x, y) in points.items():
        a, b = ref.at(x, y), shot.at(x, y)
        d = delta(a, b)
        worst = max(worst, max(abs(v) for v in d))
        flag = "  <-- off" if max(abs(v) for v in d) > args.tolerance else ""
        print(
            f"{name:22s} ({x:>5},{y:>5})  {hexof(a)}  {hexof(b)}  "
            f"{str(d):>16s}{flag}"
        )
    print(f"\nworst channel delta: {worst} (tolerance {args.tolerance})")
    return 1 if worst > args.tolerance else 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, view_required=True):
        p.add_argument("--view", required=view_required)
        p.add_argument("--design", help="WxH in design px, instead of samples.json")
        p.add_argument("--samples", help="path to samples.json")
        p.add_argument("--flat", action="store_true", help="image IS the artboard")
        return p

    p = sub.add_parser("locate")
    p.add_argument("image")
    p.add_argument("--design")
    p.add_argument("--samples")
    p.set_defaults(fn=cmd_locate)

    p = common(sub.add_parser("colors"))
    p.add_argument("image")
    p.add_argument("--points", nargs="*")
    p.set_defaults(fn=cmd_colors)

    p = common(sub.add_parser("medians"))
    p.add_argument("image")
    p.add_argument("--region", nargs="+", required=True, help="x,y,w,h in design px")
    p.set_defaults(fn=cmd_medians)

    p = common(sub.add_parser("edges"))
    p.add_argument("image")
    p.add_argument("--at", required=True)
    p.set_defaults(fn=cmd_edges)

    p = common(sub.add_parser("crop"))
    p.add_argument("image")
    p.add_argument("--rect", required=True, help="x,y,w,h in design px")
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_crop)

    p = common(sub.add_parser("compare"))
    p.add_argument("reference")
    p.add_argument("screenshot")
    p.add_argument("--tolerance", type=int, default=5)
    p.set_defaults(fn=cmd_compare)

    args = ap.parse_args()
    sys.exit(args.fn(args) or 0)


if __name__ == "__main__":
    main()
