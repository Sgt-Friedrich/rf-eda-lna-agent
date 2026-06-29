#!/usr/bin/env python3
"""Audit Touchstone files for generic RF/EDA workflows."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path


SNP_RE = re.compile(r"\.s(?P<n>\d+)p$", re.I)


def infer_ports(path: Path) -> int | None:
    match = SNP_RE.search(path.name)
    return int(match.group("n")) if match else None


def parse_touchstone(path: Path) -> dict:
    freqs: list[float] = []
    option = None
    data_rows = 0
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.split("!", 1)[0].strip()
        if not line:
            continue
        if line.startswith("#"):
            option = line
            continue
        parts = line.split()
        try:
            freq = float(parts[0])
        except (ValueError, IndexError):
            continue
        freqs.append(freq)
        data_rows += 1
    return {
        "option": option,
        "data_rows": data_rows,
        "freq_min": min(freqs) if freqs else None,
        "freq_max": max(freqs) if freqs else None,
        "has_dc_row": bool(freqs and math.isclose(min(freqs), 0.0, abs_tol=1e-30)),
    }


def verdict(payload: dict, args: argparse.Namespace) -> str:
    if payload["ports"] is None:
        return "reject_unknown_port_count"
    if args.expect_ports is not None and payload["ports"] != args.expect_ports:
        return "reject_port_count"
    if payload["data_rows"] == 0:
        return "reject_no_data"
    if args.require_dc and not payload["has_dc_row"]:
        return "dc_missing"
    if args.min_freq is not None and (payload["freq_min"] is None or payload["freq_min"] > args.min_freq):
        return "band_limited"
    if args.max_freq is not None and (payload["freq_max"] is None or payload["freq_max"] < args.max_freq):
        return "band_limited"
    return "audit_pass"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a Touchstone file for embedding readiness.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--expect-ports", type=int)
    parser.add_argument("--min-freq", type=float, help="Required minimum frequency in the file's stated units.")
    parser.add_argument("--max-freq", type=float, help="Required maximum frequency in the file's stated units.")
    parser.add_argument("--require-dc", action="store_true")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    payload = parse_touchstone(args.path)
    payload.update(
        {
            "path": str(args.path),
            "ports": infer_ports(args.path),
            "expected_ports": args.expect_ports,
            "required_min_freq": args.min_freq,
            "required_max_freq": args.max_freq,
            "require_dc": args.require_dc,
        }
    )
    payload["verdict"] = verdict(payload, args)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if payload["verdict"] in {"audit_pass", "dc_missing", "band_limited"} else 1


if __name__ == "__main__":
    raise SystemExit(main())

