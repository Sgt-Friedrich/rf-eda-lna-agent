#!/usr/bin/env python3
"""Evaluate whether a candidate can be promoted at the configured evidence gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


EVIDENCE_ORDER = {
    "E0": 0,
    "E1": 1,
    "E2": 2,
    "E3": 3,
    "E4": 4,
    "E5": 5,
    "E6": 6,
    "E7": 7,
    "E8": 8,
    "E9": 9,
    "E10": 10,
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-json", required=True, type=Path)
    parser.add_argument("--required-evidence", required=True)
    parser.add_argument("--require-hard-pass", action="store_true")
    parser.add_argument("--forbid-red-flags", action="store_true")
    args = parser.parse_args()

    candidate = load(args.candidate_json)
    evidence = str(candidate.get("evidence_level", "E0"))
    hard = candidate.get("hard_checks", {})
    red_flags = candidate.get("red_flags", [])
    reasons: list[str] = []

    if EVIDENCE_ORDER.get(evidence, -1) < EVIDENCE_ORDER.get(args.required_evidence, 999):
        reasons.append(f"evidence {evidence} below required {args.required_evidence}")
    if args.require_hard_pass:
        failed = [name for name, value in hard.items() if value is not True]
        if failed:
            reasons.append("hard checks failed or missing: " + ", ".join(sorted(failed)))
    if args.forbid_red_flags and red_flags:
        reasons.append("red flags present: " + ", ".join(map(str, red_flags)))

    verdict = "promote" if not reasons else "provisional"
    result = {
        "candidate": candidate.get("id", ""),
        "evidence_level": evidence,
        "required_evidence": args.required_evidence,
        "verdict": verdict,
        "reasons": reasons,
    }
    print(json.dumps(result, indent=2))
    return 0 if verdict == "promote" else 1


if __name__ == "__main__":
    raise SystemExit(main())
