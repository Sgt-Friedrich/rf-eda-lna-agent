#!/usr/bin/env python3
"""Classify scripts and documents into reusable RF/EDA harness families."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


FAMILY_PATTERNS: dict[str, list[str]] = {
    "optimizer_or_sweep": [
        r"optimi[sz]e",
        r"\bopt\b",
        r"sweep",
        r"trim",
        r"margin",
        r"recenter",
        r"recover",
        r"polish",
        r"tune",
    ],
    "em_cosim": [
        r"\bem\b",
        r"momentum",
        r"\bmom\b",
        r"cosim",
        r"embed",
        r"snp",
        r"touchstone",
        r"s[0-9]+p",
        r"partition",
    ],
    "layout_gui": [
        r"layout",
        r"\bgui\b",
        r"screen",
        r"capture",
        r"route",
        r"artwork",
        r"floorplan",
        r"pad",
        r"p?cell",
    ],
    "audit_diagnostic": [
        r"audit",
        r"probe",
        r"diagnostic",
        r"preflight",
        r"guard",
        r"check",
        r"compare",
        r"fixture",
        r"coverage",
    ],
    "large_signal": [
        r"\bhb\b",
        r"p1db",
        r"iip3",
        r"ip1db",
        r"compression",
        r"large.?signal",
    ],
    "signoff": [
        r"drc",
        r"lvs",
        r"gds",
        r"signoff",
        r"deck",
        r"clean",
    ],
    "process_artifact": [
        r"process",
        r"cleanup",
        r"size",
        r"artifact",
        r"status",
        r"manifest",
        r"inventory",
        r"history",
    ],
}


def iter_files(root: Path, include_exts: set[str], exclude_dirs: set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in exclude_dirs for part in path.relative_to(root).parts[:-1]):
            continue
        if path.suffix.lower() in include_exts:
            yield path


def classify(path: Path, sample: str = "") -> tuple[str, list[str]]:
    haystack = f"{path.name}\n{path.as_posix()}\n{sample[:2000]}".lower()
    scores: Counter[str] = Counter()
    hits: list[str] = []
    for family, patterns in FAMILY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, haystack, re.IGNORECASE):
                scores[family] += 1
                hits.append(f"{family}:{pattern}")
    if not scores:
        return "other", []
    family, _score = scores.most_common(1)[0]
    return family, hits


def read_sample(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def write_markdown(out: Path, data: dict) -> None:
    lines = ["# Script Family Inventory", ""]
    lines.append(f"Root: `{data['root']}`")
    lines.append("")
    lines.append("## Counts")
    lines.append("")
    lines.append("| family | count |")
    lines.append("|---|---:|")
    for family, count in sorted(data["counts"].items()):
        lines.append(f"| {family} | {count} |")
    lines.append("")
    lines.append("## Examples")
    lines.append("")
    for family, examples in sorted(data["examples"].items()):
        lines.append(f"### {family}")
        lines.append("")
        for item in examples:
            lines.append(f"- `{item}`")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--ext",
        action="append",
        default=None,
        help="File extension to include, repeatable. Defaults to common script/doc extensions.",
    )
    parser.add_argument(
        "--exclude-dir",
        action="append",
        default=[".git", "__pycache__", "build", "node_modules"],
        help="Directory name to skip, repeatable.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    include_exts = {e.lower() if e.startswith(".") else f".{e.lower()}" for e in (args.ext or ["py", "ps1", "m", "ael", "md", "yaml", "yml", "json"])}
    exclude_dirs = set(args.exclude_dir or [])

    records = []
    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    for path in iter_files(root, include_exts, exclude_dirs):
        rel = path.relative_to(root).as_posix()
        family, hits = classify(path, read_sample(path))
        counts[family] += 1
        if len(examples[family]) < 10:
            examples[family].append(rel)
        records.append({"path": rel, "family": family, "hits": hits})

    result = {
        "root": str(root),
        "file_count": len(records),
        "counts": dict(sorted(counts.items())),
        "examples": {k: v for k, v in sorted(examples.items())},
        "records": records,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "script_family_inventory.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown(args.out / "script_family_inventory.md", result)
    print(json.dumps({"verdict": "ok", "file_count": len(records), "counts": result["counts"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
