#!/usr/bin/env python3
"""Generic RF/EDA project inventory helper.

This script is open-source oriented: it does not assume a specific user path,
repository, PDK, library, or historical project. It scans configurable folders
for candidate IDs, scripts, reports, and result artifacts, then emits a compact
JSON and Markdown inventory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any


def sha1_file(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text_prefix(path: Path, limit: int = 200_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def first_heading(path: Path) -> str | None:
    for line in read_text_prefix(path, 20_000).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def classify_script(path: Path) -> str:
    name = path.name.lower()
    if any(k in name for k in ("opt", "sweep", "trim", "recenter", "recover")):
        return "optimizer-or-sweep"
    if any(k in name for k in ("em", "momentum", "snp", "touchstone", "cosim", "embed")):
        return "em-cosim-harness"
    if any(k in name for k in ("layout", "gui", "screen", "route", "net")):
        return "layout-harness"
    if any(k in name for k in ("hb", "p1db", "iip3", "large")):
        return "large-signal"
    if any(k in name for k in ("audit", "probe", "preflight", "guard", "inventory")):
        return "audit-diagnostic"
    return "other"


def extract_ids(text: str, regex: re.Pattern[str]) -> set[str]:
    ids: set[str] = set()
    for match in regex.finditer(text):
        if "id" in match.groupdict():
            ids.add(match.group("id"))
        elif match.groups():
            ids.add(match.group(1))
        else:
            ids.add(match.group(0))
    return ids


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def add_item(index: dict[str, dict[str, Any]], candidate_id: str) -> dict[str, Any]:
    return index.setdefault(
        candidate_id,
        {
            "id": candidate_id,
            "docs": [],
            "scripts": [],
            "results": [],
            "artifact_counts": {},
        },
    )


def scan(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    candidate_re = re.compile(args.candidate_regex, re.I)
    index: dict[str, dict[str, Any]] = {}

    for folder in args.doc_dirs:
        doc_root = root / folder
        if not doc_root.exists():
            continue
        for path in doc_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in args.doc_ext:
                continue
            ids = extract_ids(path.name, candidate_re) or extract_ids(read_text_prefix(path), candidate_re)
            for cid in sorted(ids):
                add_item(index, cid)["docs"].append(
                    {
                        "path": rel(path, root),
                        "bytes": path.stat().st_size,
                        "sha1": sha1_file(path),
                        "heading": first_heading(path),
                    }
                )

    for folder in args.script_dirs:
        script_root = root / folder
        if not script_root.exists():
            continue
        for path in script_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in args.script_ext:
                continue
            ids = extract_ids(path.name, candidate_re)
            for cid in sorted(ids):
                add_item(index, cid)["scripts"].append(
                    {
                        "path": rel(path, root),
                        "bytes": path.stat().st_size,
                        "sha1": sha1_file(path),
                        "class": classify_script(path),
                    }
                )

    for folder in args.result_dirs:
        result_root = root / folder
        if not result_root.exists():
            continue
        for path in result_root.rglob("*"):
            if not path.is_file():
                continue
            ids = extract_ids(str(path.relative_to(result_root)), candidate_re)
            for cid in sorted(ids):
                item = add_item(index, cid)
                suffix = path.suffix.lower() or "<none>"
                item["artifact_counts"][suffix] = item["artifact_counts"].get(suffix, 0) + 1
                if len(item["results"]) < args.max_result_paths:
                    item["results"].append({"path": rel(path, root), "bytes": path.stat().st_size})

    candidates = [index[k] for k in sorted(index, key=lambda s: (len(s), s))]
    return {
        "schema": "rf-eda-inventory-v1",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "root": str(root),
        "candidate_regex": args.candidate_regex,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def write_markdown(data: dict[str, Any], path: Path) -> None:
    lines = [
        "# RF/EDA Project Inventory",
        "",
        f"- generated: `{data['generated_at']}`",
        f"- root: `{data['root']}`",
        f"- candidate regex: `{data['candidate_regex']}`",
        f"- candidate count: `{data['candidate_count']}`",
        "",
        "| candidate | docs | scripts | result samples | artifact types |",
        "|---|---:|---:|---:|---|",
    ]
    for item in data["candidates"]:
        artifacts = ", ".join(f"{k}:{v}" for k, v in sorted(item["artifact_counts"].items()))
        lines.append(
            f"| {item['id']} | {len(item['docs'])} | {len(item['scripts'])} | {len(item['results'])} | {artifacts} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory a generic RF/EDA exploration project.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root.")
    parser.add_argument("--out", type=Path, required=True, help="Output directory.")
    parser.add_argument(
        "--candidate-regex",
        default=r"(?<![A-Za-z0-9])(?P<id>[A-Za-z]{1,4}\d{1,5})(?![A-Za-z0-9])",
        help="Regex for candidate IDs. Use a named group 'id' when possible.",
    )
    parser.add_argument("--doc-dirs", nargs="*", default=["docs"], help="Documentation directories.")
    parser.add_argument("--script-dirs", nargs="*", default=["scripts"], help="Script directories.")
    parser.add_argument("--result-dirs", nargs="*", default=["results"], help="Result directories.")
    parser.add_argument("--doc-ext", nargs="*", default=[".md", ".txt"], help="Documentation extensions.")
    parser.add_argument("--script-ext", nargs="*", default=[".py", ".ps1", ".sh"], help="Script extensions.")
    parser.add_argument("--max-result-paths", type=int, default=20, help="Maximum result path samples per candidate.")
    args = parser.parse_args()

    root = args.root.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    data = scan(root, args)
    (out / "project_inventory.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(data, out / "project_inventory.md")
    print(json.dumps({"status": "pass_inventory", "out": str(out), "candidates": data["candidate_count"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
