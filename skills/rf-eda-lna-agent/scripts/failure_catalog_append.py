#!/usr/bin/env python3
"""Append a structured failure or blocker lesson to Markdown and JSONL logs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path, help="Markdown failure catalog to append.")
    parser.add_argument("--registry", required=True, type=Path, help="JSONL registry to append.")
    parser.add_argument("--category", required=True)
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--root-cause", required=True)
    parser.add_argument("--response", required=True)
    parser.add_argument("--evidence", default="")
    parser.add_argument("--status", choices=["active", "retired", "blocked", "watch"], default="active")
    parser.add_argument("--candidate", default="")
    args = parser.parse_args()

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "category": args.category,
        "symptom": args.symptom,
        "root_cause": args.root_cause,
        "response": args.response,
        "evidence": args.evidence,
        "status": args.status,
        "candidate": args.candidate,
    }

    args.catalog.parent.mkdir(parents=True, exist_ok=True)
    if not args.catalog.exists():
        args.catalog.write_text("# Failure Catalog\n\n", encoding="utf-8")
    with args.catalog.open("a", encoding="utf-8") as f:
        f.write("\n")
        f.write(f"## {record['timestamp']} - {args.category}\n\n")
        f.write(f"- Symptom: {args.symptom}\n")
        f.write(f"- Root cause: {args.root_cause}\n")
        f.write(f"- Response: {args.response}\n")
        if args.evidence:
            f.write(f"- Evidence: {args.evidence}\n")
        if args.candidate:
            f.write(f"- Candidate: {args.candidate}\n")
        f.write(f"- Status: {args.status}\n")

    args.registry.parent.mkdir(parents=True, exist_ok=True)
    with args.registry.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(json.dumps({"verdict": "ok", "category": args.category, "status": args.status}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
