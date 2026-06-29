#!/usr/bin/env python3
"""Template: native/simulator optimizer invocation harness."""

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


def validate_optimizer_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    for key in ("runner", "variables", "hard_targets", "verification"):
        if key not in plan:
            errors.append(f"missing {key}")
    for index, var in enumerate(plan.get("variables", [])):
        for key in ("name", "min", "max"):
            if key not in var:
                errors.append(f"variables[{index}] missing {key}")
        if var.get("min") is not None and var.get("max") is not None and var["min"] >= var["max"]:
            errors.append(f"variables[{index}] min must be less than max")
        if not (var.get("physical_meaning") or var.get("model_meaning")):
            errors.append(f"variables[{index}] needs physical_meaning or model_meaning")
    hard_targets = plan.get("hard_targets", [])
    if not hard_targets:
        errors.append("hard_targets cannot be empty")
    for index, target in enumerate(hard_targets):
        for key in ("metric", "operator", "value"):
            if key not in target:
                errors.append(f"hard_targets[{index}] missing {key}")
    if not plan.get("verification", {}).get("independent_rerun"):
        errors.append("verification.independent_rerun must be true")
    return errors


def run_optimizer(plan: dict, out: Path) -> dict:
    """Project-specific optimizer hook."""
    raise NotImplementedError("fill in project-specific optimizer command")


def write_summary(out: Path, evidence: dict) -> None:
    lines = [
        "# Optimizer Invocation Evidence",
        "",
        f"- candidate: `{evidence['candidate']}`",
        f"- verdict: `{evidence['verdict']}`",
        f"- variable_count: `{evidence.get('variable_count', 0)}`",
        f"- hard_target_count: `{evidence.get('hard_target_count', 0)}`",
        "",
        "Raw optimizer rows are provisional until quantized and independently verified.",
    ]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--optimizer-plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = load_json(args.optimizer_plan)
    errors = validate_optimizer_plan(plan)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    evidence = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidate": args.candidate,
        "family": "optimizer_invocation",
        "runner": plan.get("runner", {}),
        "variable_count": len(plan.get("variables", [])),
        "hard_target_count": len(plan.get("hard_targets", [])),
        "validation_errors": errors,
    }
    write_json(out / "optimizer_run_plan.json", {**plan, "validation_errors": errors})
    if errors:
        evidence["verdict"] = "reject_invalid_plan"
        write_json(out / "evidence.json", evidence)
        write_summary(out, evidence)
        print(json.dumps(evidence, indent=2))
        return 2
    if args.dry_run:
        evidence["verdict"] = "dry_run_pass"
        evidence["promotion_blocked_until"] = [
            "optimizer completes",
            "outputs are quantized",
            "independent verification passes",
            "exploration tree is updated",
        ]
    else:
        evidence = run_optimizer(plan, out)
    write_json(out / "evidence.json", evidence)
    write_summary(out, evidence)
    print(json.dumps(evidence, indent=2))
    return 0 if evidence.get("verdict", "").endswith("pass") else 2


if __name__ == "__main__":
    raise SystemExit(main())
