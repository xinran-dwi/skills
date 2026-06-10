#!/usr/bin/env python3
"""
Canvas CLI for the design-explore-canvas skill.

Subcommands:
  add <payload.json>       Append a generation to the canvas and render canvas HTML.
  render                   Re-render canvas.html from data.json.
  get <option_id>          Print the option entry as JSON (used during revision flow).
  list                     Print a short summary of all generations.

Variants can include an optional `iframe_src` field. When set, the canvas
renders the option in an iframe pointing at that URL instead of injecting the
raw `html`. Useful when the base is a live URL and you want options shown
inside the same surrounding page chrome (see SKILL.md, Step 5, "Option-as-URL").
The `html` field is still required — embed routes typically read it from
data.json server-side and inject it where the section being explored sits.

Data lives per-project at <project_root>/explore-design-canvas/:
  data.json                source of truth (all generations for this project)
  canvas.html              the persistent canvas; one file, two views:
                             - grid view (no hash): all generations as rows of cards
                             - detail view (#VN-OptionM): full-page viewer for one gen
  assets/                  copied input images, keyed by generation id

<project_root> is the nearest .git ancestor of the current working directory
(fallback to cwd). Set CLAUDE_DESIGN_CANVAS_DIR to override.

Templates live at ~/.claude/skills/design-explore-canvas/assets/.

For Next.js projects the `add` command prints a canvas_url like http://localhost:3000/canvas#VN-Option1
and scaffolds app/canvas/route.ts if it doesn't exist. For other projects it falls back to
file:///<project_root>/explore-design-canvas/canvas.html#VN-Option1.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
from html import escape
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = SKILL_DIR / "assets"

CANVAS_ROUTE_TEMPLATE = '''\
import { promises as fs } from "fs";
import path from "path";
import { NextResponse } from "next/server";

export async function GET() {
  const html = await fs.readFile(
    path.join(process.cwd(), "explore-design-canvas", "canvas.html"),
    "utf-8"
  );
  return new NextResponse(html, {
    headers: { "Content-Type": "text/html" },
  });
}
'''


def _project_root() -> Path:
    cwd = Path.cwd().resolve()
    for p in [cwd, *cwd.parents]:
        if (p / ".git").exists():
            return p
    return cwd


def _project_canvas_dir() -> Path:
    env = os.environ.get("CLAUDE_DESIGN_CANVAS_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return _project_root() / "explore-design-canvas"


CANVAS_DIR = _project_canvas_dir()
DATA_PATH = CANVAS_DIR / "data.json"
CANVAS_HTML = CANVAS_DIR / "canvas.html"
ASSETS_DIR = CANVAS_DIR / "assets"


# ---------- Next.js detection ----------

def _is_nextjs_project() -> bool:
    pkg = _project_root() / "package.json"
    if not pkg.exists():
        return False
    try:
        data = json.loads(pkg.read_text())
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        return "next" in deps
    except Exception:
        return False


def _ensure_canvas_route() -> bool:
    """Scaffold app/canvas/route.ts if it doesn't exist. Returns True if created."""
    route_path = _project_root() / "app" / "canvas" / "route.ts"
    if route_path.exists():
        return False
    route_path.parent.mkdir(parents=True, exist_ok=True)
    route_path.write_text(CANVAS_ROUTE_TEMPLATE)
    return True


# ---------- data layer ----------

def load_data() -> dict:
    if DATA_PATH.exists():
        return json.loads(DATA_PATH.read_text())
    return {"generations": []}


def save_data(data: dict) -> None:
    CANVAS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(data, indent=2))


def next_gen_id(data: dict) -> str:
    n = len(data["generations"]) + 1
    return f"V{n}"


# ---------- rendering ----------

def render_canvas(data: dict) -> str:
    tmpl = (TEMPLATE_DIR / "canvas.html.tmpl").read_text()

    if not data["generations"]:
        body = '<div class="empty">No generations yet. Run the skill to add the first one.</div>'
    else:
        rows = []
        for gen in reversed(data["generations"]):  # newest first
            ts = gen.get("created_at", "")
            try:
                ts_pretty = dt.datetime.fromisoformat(ts).strftime("%b %d, %Y · %H:%M")
            except Exception:
                ts_pretty = ts
            parent = gen.get("parent_id")
            parent_html = (
                f'<span class="gen-parent" data-parent-jump="{escape(parent)}">forked from {escape(parent)}</span>'
                if parent else ""
            )
            hint = gen.get("revision_hint")
            summary = gen.get("source_summary", "")
            head = (
                f'<div class="gen-head">'
                f'<span class="gen-id">{escape(gen["id"])}</span>'
                f'{parent_html}'
                f'<span class="gen-ts">{escape(ts_pretty)}</span>'
                f'</div>'
            )
            cards = []
            for v in gen["variants"]:
                if v.get("iframe_src"):
                    thumb = f'<div class="thumb"><iframe src="{escape(v["iframe_src"])}"></iframe></div>'
                else:
                    srcdoc = v["html"].replace('"', "&quot;")
                    thumb = f'<div class="thumb"><iframe srcdoc="{srcdoc}" sandbox=""></iframe></div>'
                cards.append(
                    f'<div class="card" data-variant-id="{escape(v["id"])}">'
                    f'{thumb}'
                    f'<div class="card-meta">'
                    f'<div class="card-name">{escape(v["direction_name"])}</div>'
                    f'<div class="card-id">{escape(v["id"])}</div>'
                    f'</div>'
                    f'</div>'
                )

            # right-side context panel: the prompt the user typed (or their revision instruction)
            prompt_text = hint or summary
            if prompt_text:
                side_inner = (
                    f'<div class="gen-side-label">PROMPT USED</div>'
                    f'<p class="gen-side-text is-prompt">"{escape(prompt_text)}"</p>'
                )
            else:
                side_inner = (
                    f'<div class="gen-side-label">PROMPT USED</div>'
                    f'<p class="gen-side-text" style="color:#9b9b94">No prompt recorded.</p>'
                )

            rows.append(
                f'<div class="gen">'
                f'<div class="gen-main">{head}<div class="cards">{"".join(cards)}</div></div>'
                f'<aside class="gen-side">{side_inner}</aside>'
                f'</div>'
            )
        body = f'<div class="generations">{"".join(rows)}</div>'

    out = tmpl
    out = out.replace("__BODY__", body)
    out = out.replace("__DATA_JSON__", json.dumps(data))
    out = out.replace("__PROJECT_PATH__", escape(str(_project_root())))
    return out


def write_canvas(data: dict) -> Path:
    CANVAS_DIR.mkdir(parents=True, exist_ok=True)
    CANVAS_HTML.write_text(render_canvas(data))
    return CANVAS_HTML


# ---------- commands ----------

def cmd_add(args) -> int:
    payload_path = Path(args.payload)
    payload = json.loads(payload_path.read_text())
    variants = payload.get("variants", [])
    if len(variants) != 4:
        print(f"ERROR: expected exactly 4 variants, got {len(variants)}", file=sys.stderr)
        return 2

    data = load_data()
    gen_id = next_gen_id(data)

    # handle base image: copy into canvas assets so the detail view can show it.
    # canvas.html lives at the canvas dir root, so rendered_src is relative to that.
    base = dict(payload.get("base", {"kind": "text", "content": ""}))
    if base.get("kind") in ("image", "figma") and base.get("content"):
        src = Path(base["content"]).expanduser()
        if src.exists() and base["kind"] == "image":
            ASSETS_DIR.mkdir(parents=True, exist_ok=True)
            dest = ASSETS_DIR / f"{gen_id}-base{src.suffix}"
            shutil.copy(src, dest)
            base["rendered_src"] = f"assets/{dest.name}"
        elif base["kind"] == "figma" and payload.get("base", {}).get("image_path"):
            img_src = Path(payload["base"]["image_path"]).expanduser()
            if img_src.exists():
                ASSETS_DIR.mkdir(parents=True, exist_ok=True)
                dest = ASSETS_DIR / f"{gen_id}-figma{img_src.suffix}"
                shutil.copy(img_src, dest)
                base["rendered_src"] = f"assets/{dest.name}"

    gen = {
        "id": gen_id,
        "parent_id": payload.get("parent_id"),
        "revision_hint": payload.get("revision_hint"),
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "source_summary": payload.get("source_summary", ""),
        "base": base,
        "variants": [
            {
                "id": f"{gen_id}-Option{i+1}",
                "direction_name": v["direction_name"],
                "rationale": v.get("rationale", []),
                "html": v["html"],
                **({"iframe_src": v["iframe_src"]} if v.get("iframe_src") else {}),
            }
            for i, v in enumerate(variants)
        ],
    }
    data["generations"].append(gen)
    save_data(data)

    canvas_path = write_canvas(data)
    first_variant = gen["variants"][0]["id"]

    if _is_nextjs_project():
        created = _ensure_canvas_route()
        devserver = os.environ.get("CLAUDE_CANVAS_DEVSERVER", "http://localhost:3000")
        canvas_url = f"{devserver}/canvas#{first_variant}"
        extra = {"nextjs_route_created": created} if created else {}
    else:
        canvas_url = f"file://{canvas_path}#{first_variant}"
        extra = {}

    print(json.dumps({
        "generation_id": gen_id,
        "canvas": str(canvas_path),
        "canvas_url": canvas_url,
        "variant_ids": [v["id"] for v in gen["variants"]],
        **extra,
    }, indent=2))
    return 0


def cmd_render(args) -> int:
    data = load_data()
    # clean up stale viewer_path entries from older versions of this skill
    for gen in data["generations"]:
        gen.pop("viewer_path", None)
        # rewrite legacy '../assets/...' paths to 'assets/...'
        base = gen.get("base", {})
        rs = base.get("rendered_src")
        if isinstance(rs, str) and rs.startswith("../"):
            base["rendered_src"] = rs[3:]
    save_data(data)
    canvas_path = write_canvas(data)
    if _is_nextjs_project():
        _ensure_canvas_route()
        devserver = os.environ.get("CLAUDE_CANVAS_DEVSERVER", "http://localhost:3000")
        canvas_url = f"{devserver}/canvas"
    else:
        canvas_url = f"file://{canvas_path}"
    print(json.dumps({"canvas": str(canvas_path), "canvas_url": canvas_url, "generations": len(data["generations"])}, indent=2))
    return 0


def cmd_get(args) -> int:
    data = load_data()
    vid = args.variant_id
    for gen in data["generations"]:
        for v in gen["variants"]:
            if v["id"] == vid:
                out = {
                    "generation_id": gen["id"],
                    "parent_id": gen.get("parent_id"),
                    "source_summary": gen.get("source_summary"),
                    "variant": v,
                }
                print(json.dumps(out, indent=2))
                return 0
    print(f"ERROR: variant {vid} not found", file=sys.stderr)
    return 1


def cmd_list(args) -> int:
    data = load_data()
    if not data["generations"]:
        print("(canvas is empty)")
        return 0
    for gen in data["generations"]:
        parent = f" ← {gen['parent_id']}" if gen.get("parent_id") else ""
        print(f"{gen['id']}{parent}  {gen.get('source_summary', '')}")
        for v in gen["variants"]:
            print(f"  {v['id']:>18}  {v['direction_name']}")
    return 0


def main():
    p = argparse.ArgumentParser(description="Design canvas CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="Append a generation from a JSON payload")
    a.add_argument("payload", help="Path to JSON payload")
    a.set_defaults(func=cmd_add)

    r = sub.add_parser("render", help="Re-render canvas.html from data.json")
    r.set_defaults(func=cmd_render)

    g = sub.add_parser("get", help="Print a variant entry as JSON")
    g.add_argument("variant_id")
    g.set_defaults(func=cmd_get)

    l = sub.add_parser("list", help="List all generations and variants")
    l.set_defaults(func=cmd_list)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
