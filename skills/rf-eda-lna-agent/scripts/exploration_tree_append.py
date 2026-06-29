#!/usr/bin/env python3
"""Append a candidate record to exploration-tree Markdown and JSONL registry."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Append candidate evidence to an exploration tree.")
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--parent")
    parser.add_argument("--branch", required=True)
    parser.add_argument("--hypothesis", required=True)
    parser.add_argument("--evidence-level", required=True)
    parser.add_argument("--decision", required=True, choices=["promote", "retire", "blocked", "continue", "provisional"])
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--do-not-repeat", action="append", default=[])
    parser.add_argument("--next-action", default="")
    args = parser.parse_args()

    record = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "id": args.candidate,
        "parent": args.parent,
        "branch": args.branch,
        "hypothesis": args.hypothesis,
        "evidence_level": args.evidence_level,
        "decision": args.decision,
        "artifacts": args.artifact,
        "do_not_repeat": args.do_not_repeat,
        "next_action": args.next_action,
    }
    args.tree.parent.mkdir(parents=True, exist_ok=True)
    if not args.tree.exists():
        args.tree.write_text("# Exploration Tree\n\n", encoding="utf-8", newline="\n")
    lines = [
        "",
        f"## {args.candidate} - {args.branch}",
        "",
        f"- timestamp: `{record['timestamp']}`",
        f"- parent: `{args.parent or 'none'}`",
        f"- evidence level: `{args.evidence_level}`",
        f"- decision: `{args.decision}`",
        f"- hypothesis: {args.hypothesis}",
    ]
    for artifact in args.artifact:
        lines.append(f"- artifact: `{artifact}`")
    for rule in args.do_not_repeat:
        lines.append(f"- do not repeat: {rule}")
    if args.next_action:
        lines.append(f"- next action: {args.next_action}")
    with args.tree.open("a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    if args.registry:
        args.registry.parent.mkdir(parents=True, exist_ok=True)
        with args.registry.open("a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"status": "appended", "candidate": args.candidate, "tree": str(args.tree)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
