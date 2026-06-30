#!/usr/bin/env python3
"""Append sanitized RF textbook lessons to a Markdown knowledge base.

Lessons are authored summaries, not copied textbook content. The script accepts
short user-written fields and a source hint so teams can turn reading notes into
repeatable agent checks.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", required=True, type=Path)
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--source", required=True, help="Book or chapter-level source label")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--agent-use", required=True, help="How an RF/EDA agent should use the lesson")
    parser.add_argument("--sanity-gates", default="", help="Comma-separated gate/check names")
    parser.add_argument("--harness-links", default="", help="Comma-separated harness families")
    parser.add_argument("--notes", default="", help="Original summary only; do not paste textbook text")
    args = parser.parse_args()

    record = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": args.source,
        "topic": args.topic,
        "agent_use": args.agent_use,
        "sanity_gates": split_csv(args.sanity_gates),
        "harness_links": split_csv(args.harness_links),
        "notes": args.notes,
        "copyright_boundary": "original summary; no copied textbook body text",
    }

    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.registry.parent.mkdir(parents=True, exist_ok=True)

    if not args.markdown.exists():
        args.markdown.write_text("# RF Textbook Lessons\n\n", encoding="utf-8")

    section = [
        f"## {record['topic']}",
        "",
        f"- Source: {record['source']}",
        f"- Agent use: {record['agent_use']}",
        f"- Sanity gates: {', '.join(record['sanity_gates']) or 'none'}",
        f"- Harness links: {', '.join(record['harness_links']) or 'none'}",
    ]
    if args.notes:
        section.extend(["- Notes: " + args.notes])
    section.extend(["", ""])
    with args.markdown.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(section))

    with args.registry.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(json.dumps({"verdict": "ok", "topic": args.topic}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
