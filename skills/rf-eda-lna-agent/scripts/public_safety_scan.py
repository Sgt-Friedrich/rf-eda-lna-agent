#!/usr/bin/env python3
"""Scan a public RF/EDA skill repo for common leakage hazards."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TEXT_EXTS = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
HEAVY_EXTS = {
    ".pdf",
    ".gds",
    ".gdsii",
    ".dsn",
    ".dds",
    ".oa",
    ".raw",
}
PATTERNS = {
    # The negative look-behind avoids false positives on URL schemes such as https://.
    "windows_absolute_path": re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]|Users[\\/]", re.IGNORECASE),
    "private_project_hint": re.compile(r"lion-lna|lna_ai_report|desktop[\\/]lna", re.IGNORECASE),
    "fixed_candidate_id": re.compile(r"\bD\d{3,}\b"),
    "fixed_metric_threshold": re.compile(r"\b(NF|S21|S11|S22)\s*[<>]=?\s*-?\d", re.IGNORECASE),
    "credential_word": re.compile(r"\b(token|password|secret|api[_-]?key|private[_-]?key)\b", re.IGNORECASE),
}
ALLOWLIST_PHRASES = {
    "credential_word": ["tokens", "credentials", "search for tokens", "user tokens"],
    "negative_policy": ["does not include", "not include", "no ", "do not upload", "不包含", "不上传", "不发布"],
}


def should_skip(path: Path, root: Path) -> bool:
    rel_parts_tuple = path.relative_to(root).parts
    rel_parts = set(rel_parts_tuple)
    if any(part.startswith(".tmp_") for part in rel_parts_tuple):
        return True
    return bool(rel_parts & {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"})


def scan_file(path: Path, root: Path) -> list[dict]:
    findings: list[dict] = []
    rel = path.relative_to(root).as_posix()
    suffix = path.suffix.lower()
    if suffix in HEAVY_EXTS or re.search(r"\.s\d+p$", suffix):
        findings.append({"path": rel, "kind": "heavy_artifact_extension", "line": 0, "text": suffix})
        return findings
    if suffix not in TEXT_EXTS:
        return findings
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return findings
    for idx, line in enumerate(lines, 1):
        if "re.compile(" in line:
            continue
        for kind, pattern in PATTERNS.items():
            if not pattern.search(line):
                continue
            lowered = line.lower()
            if kind == "credential_word":
                if any(phrase in lowered for phrase in ALLOWLIST_PHRASES["credential_word"]):
                    continue
                if any(phrase in lowered for phrase in ALLOWLIST_PHRASES["negative_policy"]):
                    continue
            findings.append({"path": rel, "kind": kind, "line": idx, "text": line[:180]})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    findings: list[dict] = []
    for path in root.rglob("*"):
        if path.is_file() and not should_skip(path, root):
            findings.extend(scan_file(path, root))
    result = {
        "verdict": "pass" if not findings else "fail",
        "finding_count": len(findings),
        "findings": findings,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
