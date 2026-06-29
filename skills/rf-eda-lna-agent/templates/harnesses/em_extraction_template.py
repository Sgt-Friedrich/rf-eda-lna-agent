#!/usr/bin/env python3
"""Template: EM extraction harness."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def validate_em_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    for key in ("layout_cell", "em_block", "ports", "frequency", "substrate"):
        if key not in plan:
            errors.append(f"missing {key}")
    for index, port in enumerate(plan.get("ports", [])):
        for key in ("name", "node", "reference_plane"):
            if key not in port:
                errors.append(f"ports[{index}] missing {key}")
        if port.get("carries_dc") and not plan.get("dc_handling", {}).get("documented"):
            errors.append(f"ports[{index}] carries DC but dc_handling.documented is not true")
    freq = plan.get("frequency", {})
    if "stop" not in freq:
        errors.append("frequency.stop is required")
    return errors


def run_em_solver(plan: dict, out: Path) -> dict:
    """Project-specific EM solver hook."""
    raise NotImplementedError("fill in project-specific EM solver command")


def write_summary(out: Path, evidence: dict) -> None:
    lines = [
        "# EM Extraction Evidence",
        "",
        f"- candidate: `{evidence['candidate']}`",
        f"- block: `{evidence.get('em_block', '')}`",
        f"- verdict: `{evidence['verdict']}`",
        f"- port_count: `{evidence.get('port_count', 0)}`",
        "",
        "An EM artifact is not safe to embed until Touchstone coverage, DC behavior, port order, and reference planes are audited.",
    ]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--em-plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = load_json(args.em_plan)
    errors = validate_em_plan(plan)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    evidence = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidate": args.candidate,
        "family": "em_extraction",
        "em_block": plan.get("em_block", ""),
        "port_count": len(plan.get("ports", [])),
        "frequency": plan.get("frequency", {}),
        "validation_errors": errors,
    }
    write_json(out / "em_run_plan.json", {**plan, "validation_errors": errors})
    if errors:
        evidence["verdict"] = "reject_invalid_plan"
        write_json(out / "evidence.json", evidence)
        write_summary(out, evidence)
        print(json.dumps(evidence, indent=2))
        return 2
    if args.dry_run:
        evidence["verdict"] = "dry_run_pass"
        evidence["expected_touchstone"] = f"{plan.get('em_block', 'block')}.sNp"
    else:
        evidence = run_em_solver(plan, out)
    write_json(out / "evidence.json", evidence)
    write_summary(out, evidence)
    print(json.dumps(evidence, indent=2))
    return 0 if evidence.get("verdict", "").endswith("pass") else 2


if __name__ == "__main__":
    raise SystemExit(main())
