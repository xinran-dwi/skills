#!/usr/bin/env python3
"""Rasterize an SVG (file or stdin) to a high-resolution PNG in the
newsletter-diagram style. Defaults to 2x scale on a white background.

Examples:
  python3 render_png.py --svg-file d.svg --out /mnt/user-data/outputs/d.png
  cat d.svg | python3 render_png.py --out out.png --scale 2 --bg "#ffffff"
"""
import argparse
import re
import subprocess
import sys


def ensure_cairosvg():
    try:
        import cairosvg  # noqa: F401
        return
    except ImportError:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "cairosvg",
             "--break-system-packages", "-q"],
            check=True,
        )


def read_dims(svg: str):
    """Pull width/height (px) from the root <svg> tag; fall back to viewBox."""
    w = re.search(r'<svg[^>]*\bwidth="([\d.]+)', svg)
    h = re.search(r'<svg[^>]*\bheight="([\d.]+)', svg)
    if w and h:
        return float(w.group(1)), float(h.group(1))
    vb = re.search(r'viewBox="[\d.\s]*?([\d.]+)\s+([\d.]+)"', svg)
    if vb:
        return float(vb.group(1)), float(vb.group(2))
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg-file", help="Path to SVG; omit to read from stdin")
    ap.add_argument("--out", required=True, help="Output PNG path")
    ap.add_argument("--scale", type=float, default=2.0,
                    help="Resolution multiplier (default 2)")
    ap.add_argument("--bg", default="#ffffff",
                    help="Background color (default white)")
    args = ap.parse_args()

    svg = open(args.svg_file).read() if args.svg_file else sys.stdin.read()

    ensure_cairosvg()
    import cairosvg

    w, h = read_dims(svg)
    kwargs = dict(bytestring=svg.encode("utf-8"), write_to=args.out,
                  background_color=args.bg)
    if w and h:
        kwargs["output_width"] = round(w * args.scale)
        kwargs["output_height"] = round(h * args.scale)

    cairosvg.svg2png(**kwargs)
    print(f"wrote {args.out}" + (f" ({round(w*args.scale)}x{round(h*args.scale)})"
                                 if w and h else ""))


if __name__ == "__main__":
    main()
