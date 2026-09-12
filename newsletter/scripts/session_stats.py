#!/usr/bin/env python3
"""Per-task token and time stats from a Claude Code session transcript.

Newsletter pieces about AI work live or die on real numbers. This reads the
transcript Claude Code already writes and splits it at each user prompt, so you
get a per-task breakdown instead of one session-wide total.

Usage:
    session_stats.py                          # most recent session, cwd's project
    session_stats.py --project ~/code/thing   # a specific project directory
    session_stats.py --transcript path.jsonl  # an exact transcript
    session_stats.py --list                   # show sessions, newest first
    session_stats.py --json                   # machine-readable

Notes on the numbers, which are easy to misreport:

  fresh in  - uncached input. Usually near zero; not worth putting in an article.
  cache wr  - tokens newly written to cache this turn.
  cache rd  - the whole conversation re-sent on every tool round-trip. This is
              the big one, and it scales with STEPS TAKEN, not with how much the
              user typed. That relationship is the interesting story.
  output    - what the model actually wrote.
  minutes   - elapsed inside the task, first prompt to last event. NOT wall-clock
              across a day with gaps between tasks. Say so when you publish it.
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

PROJECTS = Path.home() / ".claude" / "projects"


def project_dir(path: Path) -> Path:
    """Claude Code slugifies the project path: / and . and _ all become -."""
    slug = str(path.resolve()).replace("/", "-").replace(".", "-").replace("_", "-")
    return PROJECTS / slug


def transcripts(proj: Path):
    if not proj.is_dir():
        return []
    return sorted(proj.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)


def load(path: Path):
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # partial final line while a session is live
    return rows


def text_of(msg) -> str:
    content = msg.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


def user_prompts(rows):
    """Only turns the human actually typed.

    The transcript labels these: a typed prompt carries `promptSource`, while
    injected content (a skill body loading, an interruption notice, a tool
    result) carries `isMeta` or `sourceToolUseID` instead. Without this filter a
    single loaded skill shows up as its own multi-thousand-token "task", which
    is exactly the kind of number you don't want to publish.
    """
    out = []
    seen_ids = set()
    for r in rows:
        if r.get("type") != "user" or r.get("isMeta"):
            continue
        if not r.get("promptSource") or r.get("sourceToolUseID"):
            continue
        pid = r.get("promptId")
        if pid and pid in seen_ids:
            continue  # same prompt re-logged with reminders attached
        body = text_of(r.get("message", {})).strip()
        ts = r.get("timestamp", "")
        if not body or not ts:
            continue
        if pid:
            seen_ids.add(pid)
        out.append((ts, body))
    return out


def analyse(rows):
    marks = user_prompts(rows)
    if not marks:
        return []

    bounds = [ts for ts, _ in marks]

    def bucket(ts):
        idx = -1
        for i, b in enumerate(bounds):
            if ts >= b:
                idx = i
        return idx

    agg = defaultdict(
        lambda: {
            "turns": 0, "tools": 0, "fresh": 0, "cache_w": 0,
            "cache_r": 0, "output": 0, "last_ts": "", "tool_names": Counter(),
        }
    )
    seen = set()

    for r in rows:
        ts = r.get("timestamp", "")
        if not ts:
            continue
        i = bucket(ts)
        if i < 0:
            continue
        a = agg[i]
        if r.get("type") != "assistant":
            continue
        # Anchor the end of a task to its last assistant turn. Background events
        # (artifact watches, hook output) can land hours later in the idle gap
        # before the next prompt, and counting those turns a 7-minute task into
        # a 5-hour one.
        if ts > a["last_ts"]:
            a["last_ts"] = ts

        msg = r.get("message", {})
        for block in msg.get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                a["tools"] += 1
                a["tool_names"][block.get("name", "?")] += 1

        # One assistant message can appear on several lines (streaming); count
        # its usage once or every number comes out inflated.
        mid = msg.get("id")
        if mid and mid in seen:
            continue
        if mid:
            seen.add(mid)

        u = msg.get("usage") or {}
        a["turns"] += 1
        a["fresh"] += u.get("input_tokens", 0)
        a["cache_w"] += u.get("cache_creation_input_tokens", 0)
        a["cache_r"] += u.get("cache_read_input_tokens", 0)
        a["output"] += u.get("output_tokens", 0)

    fmt = "%Y-%m-%dT%H:%M:%S"
    tasks = []
    for i, (ts, prompt) in enumerate(marks):
        a = agg.get(i)
        if not a or a["turns"] == 0:
            continue
        try:
            mins = (
                datetime.strptime(a["last_ts"][:19], fmt)
                - datetime.strptime(ts[:19], fmt)
            ).total_seconds() / 60
        except ValueError:
            mins = 0.0
        tasks.append({
            "n": len(tasks) + 1,
            "started": ts[:19].replace("T", " "),
            "prompt": " ".join(prompt.split())[:70],
            "minutes": round(mins, 1),
            "turns": a["turns"],
            "tools": a["tools"],
            "fresh_in": a["fresh"],
            "cache_write": a["cache_w"],
            "cache_read": a["cache_r"],
            "output": a["output"],
            "top_tools": dict(a["tool_names"].most_common(5)),
        })
    return tasks


def render(tasks, source):
    if not tasks:
        print("No completed tasks found in that transcript.", file=sys.stderr)
        return
    print(f"\n{source.name}\n")
    head = f"{'#':>2}  {'task':<46}{'min':>6}{'turns':>7}{'tools':>7}{'output':>10}{'cache rd':>12}"
    print(head)
    print("-" * len(head))
    tot = Counter()
    for t in tasks:
        print(
            f"{t['n']:>2}  {t['prompt'][:44]:<46}{t['minutes']:>6}"
            f"{t['turns']:>7}{t['tools']:>7}{t['output']:>10,}{t['cache_read']:>12,}"
        )
        for k in ("minutes", "turns", "tools", "output", "cache_read",
                  "cache_write", "fresh_in"):
            tot[k] += t[k]
    print("-" * len(head))
    print(
        f"{'':>2}  {'TOTAL':<46}{round(tot['minutes'], 1):>6}"
        f"{tot['turns']:>7}{tot['tools']:>7}{tot['output']:>10,}{tot['cache_read']:>12,}"
    )
    if tot["output"]:
        print(f"\n  cache read : output  =  {tot['cache_read'] / tot['output']:.0f} : 1")
    print(f"  cache writes {tot['cache_write']:,} | fresh input {tot['fresh_in']:,}")
    print(
        "\n  Minutes are time inside each task, not elapsed across the day."
        "\n  Cache reads scale with steps taken, not with prompt length.\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", type=Path, default=Path.cwd())
    ap.add_argument("--transcript", type=Path)
    ap.add_argument("--list", action="store_true", help="list sessions, newest first")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()

    if args.transcript:
        path = args.transcript
        if not path.is_file():
            sys.exit(f"No such transcript: {path}")
    else:
        proj = project_dir(args.project)
        found = transcripts(proj)
        if not found:
            sys.exit(
                f"No transcripts for {args.project}\n"
                f"Looked in: {proj}\n"
                f"Pass --transcript to point at one directly."
            )
        if args.list:
            for p in found:
                when = datetime.fromtimestamp(p.stat().st_mtime)
                print(f"{when:%Y-%m-%d %H:%M}  {p.stat().st_size/1e6:6.1f} MB  {p.name}")
            return
        path = found[0]

    tasks = analyse(load(path))
    if args.json:
        print(json.dumps({"transcript": str(path), "tasks": tasks}, indent=2))
    else:
        render(tasks, path)


if __name__ == "__main__":
    main()
