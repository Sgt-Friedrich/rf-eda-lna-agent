#!/usr/bin/env python3
"""Append a compact candidate status record."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a status record to a Markdown log.")
    parser.add_argument("--status-file", type=Path, required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--evidence-level", required=True)
    parser.add_argument("--verdict", required=True, choices=["pass", "fail", "blocked", "provisional", "continue"])
    parser.add_argument("--summary", required=True)
    parser.add_argument("--metrics-json", type=Path)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--next-action", default="")
    args = parser.parse_args()

    metrics = None
    if args.metrics_json:
        metrics = json.loads(args.metrics_json.read_text(encoding="utf-8"))

    args.status_file.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "",
        f"## {time.strftime('%Y-%m-%d %H:%M:%S')} {args.candidate}",
        "",
        f"- evidence level: `{args.evidence_level}`",
        f"- verdict: `{args.verdict}`",
        f"- summary: {args.summary}",
    ]
    if metrics is not None:
        lines.append(f"- metrics: `{json.dumps(metrics, ensure_ascii=False)}`")
    for artifact in args.artifact:
        lines.append(f"- artifact: `{artifact}`")
    if args.next_action:
        lines.append(f"- next action: {args.next_action}")
    with args.status_file.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    print(json.dumps({"status": "appended", "file": str(args.status_file), "candidate": args.candidate}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

