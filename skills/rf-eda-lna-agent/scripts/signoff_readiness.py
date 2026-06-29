#!/usr/bin/env python3
"""Check signoff-readiness collateral without claiming signoff-clean."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def check_path(label: str, value: str | None, required: bool) -> dict:
    if not required:
        return {"name": label, "required": False, "status": "not_required", "path": value}
    if not value:
        return {"name": label, "required": True, "status": "missing_path", "path": value}
    path = Path(value)
    return {
        "name": label,
        "required": True,
        "status": "present" if path.exists() else "missing_file",
        "path": value,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess signoff readiness from user-provided collateral paths.")
    parser.add_argument("--require-drc", action="store_true")
    parser.add_argument("--require-lvs", action="store_true")
    parser.add_argument("--drc-deck")
    parser.add_argument("--lvs-deck")
    parser.add_argument("--layer-map")
    parser.add_argument("--device-map")
    parser.add_argument("--drc-report")
    parser.add_argument("--lvs-report")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    checks = [
        check_path("drc_deck", args.drc_deck, args.require_drc),
        check_path("lvs_deck", args.lvs_deck, args.require_lvs),
        check_path("layer_map", args.layer_map, args.require_drc or args.require_lvs),
        check_path("device_map", args.device_map, args.require_lvs),
        check_path("drc_report", args.drc_report, args.require_drc),
        check_path("lvs_report", args.lvs_report, args.require_lvs),
    ]
    blockers = [c for c in checks if c["status"].startswith("missing")]
    payload = {
        "verdict": "ready" if not blockers else "blocked_external",
        "note": "This is readiness only; signoff-clean requires official clean reports.",
        "checks": checks,
        "blockers": blockers,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
