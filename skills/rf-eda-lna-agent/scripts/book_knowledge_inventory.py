#!/usr/bin/env python3
"""Inventory RF/microwave textbooks without copying copyrighted content.

The script records metadata, extraction status, and chapter/table-of-contents
signals. It is intentionally conservative: failed extraction is reported as a
blocker instead of becoming inferred knowledge.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path


CHAPTER_PATTERNS = [
    re.compile(r"^\s*(chapter|CHAPTER)\s+\d+\s+(.+)$"),
    re.compile(r"^\s*\d+\s+[A-Z][A-Za-z0-9,;:'() /\-]{8,}$"),
    re.compile(r"^\s*\d+\.\d+\s+[A-Z][A-Za-z0-9,;:'() /\-]{8,}$"),
]

KEYWORDS = [
    "noise",
    "stability",
    "matching",
    "transmission",
    "scattering",
    "smith",
    "nonlinear",
    "harmonic",
    "amplifier",
    "lumped",
    "capacitor",
    "inductor",
    "resistor",
    "via",
    "microstrip",
    "ads",
]


def run_command(args: list[str], timeout_s: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, timeout=timeout_s, check=False)


def parse_pdfinfo(text: str) -> dict:
    result: dict[str, str | int] = {}
    for line in text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower().replace(" ", "_")
        value = value.strip()
        if key == "pages":
            try:
                result[key] = int(value)
            except ValueError:
                result[key] = value
        elif key in {"title", "author", "page_size"}:
            result[key] = value
    return result


def extract_toc(pdf: Path, max_pages: int) -> tuple[str, list[str], list[str], str]:
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "toc.txt"
        proc = run_command(["pdftotext", "-layout", "-f", "1", "-l", str(max_pages), str(pdf), str(out)])
        if proc.returncode != 0 or not out.exists():
            reason = (proc.stderr or proc.stdout or "pdftotext failed").strip()
            return "needs_repair_or_ocr", [], [], reason[:1000]
        text = out.read_text(encoding="utf-8", errors="ignore")

    headings: list[str] = []
    keyword_hits: list[str] = []
    for raw in text.splitlines():
        line = " ".join(raw.split())
        if not line:
            continue
        if any(pattern.match(line) for pattern in CHAPTER_PATTERNS):
            if line not in headings:
                headings.append(line[:180])
        lowered = line.lower()
        if any(word in lowered for word in KEYWORDS) and len(keyword_hits) < 80:
            keyword_hits.append(line[:180])
        if len(headings) >= 80:
            break

    if not headings and not keyword_hits:
        return "needs_repair_or_ocr", [], [], "No table-of-contents or keyword text extracted from sampled pages."
    return "extracted", headings[:80], keyword_hits[:80], ""


def inventory_pdf(pdf: Path, max_pages: int) -> dict:
    info_proc = run_command(["pdfinfo", str(pdf)])
    info = parse_pdfinfo(info_proc.stdout) if info_proc.returncode == 0 else {}
    status = "metadata_ok" if info_proc.returncode == 0 else "metadata_failed"
    info_error = "" if info_proc.returncode == 0 else (info_proc.stderr or info_proc.stdout).strip()[:1000]

    toc_status, headings, keyword_hits, toc_error = extract_toc(pdf, max_pages=max_pages)
    if toc_status != "extracted":
        status = "needs_repair_or_ocr"
    else:
        status = "extracted"

    return {
        "file_name": pdf.name,
        "size_bytes": pdf.stat().st_size,
        "metadata": info,
        "status": status,
        "metadata_error": info_error,
        "toc_error": toc_error,
        "chapter_or_toc_signals": headings,
        "keyword_signals": keyword_hits,
        "copyright_boundary": "metadata and short chapter signals only; do not copy textbook body text",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--books-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--max-pages", type=int, default=35)
    args = parser.parse_args()

    books_dir = args.books_dir
    pdfs = sorted(books_dir.glob("*.pdf"))
    records = [inventory_pdf(pdf, max_pages=args.max_pages) for pdf in pdfs]

    args.out.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "books_dir_name": books_dir.name,
        "book_count": len(records),
        "status_counts": {
            status: sum(1 for rec in records if rec["status"] == status)
            for status in sorted({rec["status"] for rec in records})
        },
        "records": records,
    }
    (args.out / "book_knowledge_inventory.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(json.dumps({"verdict": "ok", "book_count": len(records), "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
