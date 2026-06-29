#!/usr/bin/env python3
"""Report repository artifact size and optionally write a manifest."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect artifact sizes without deleting anything.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--max-bytes", type=int)
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    files = []
    total = 0
    for path in iter_files(root):
        size = path.stat().st_size
        total += size
        files.append({"path": path.relative_to(root).as_posix(), "bytes": size})
    files.sort(key=lambda item: item["bytes"], reverse=True)
    verdict = "pass" if args.max_bytes is None or total <= args.max_bytes else "fail_budget"
    payload = {
        "root": str(root),
        "total_bytes": total,
        "max_bytes": args.max_bytes,
        "verdict": verdict,
        "largest": files[: args.top],
    }
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
