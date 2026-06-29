#!/usr/bin/env python3
"""Template: EM/circuit cosimulation embedding harness."""

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


def validate_embedding_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    for key in ("circuit_harness", "artifacts", "port_map", "mode"):
        if key not in plan:
            errors.append(f"missing {key}")
    if plan.get("mode") not in {"replace", "audit", "hybrid"}:
        errors.append("mode must be replace, audit, or hybrid")
    for index, artifact in enumerate(plan.get("artifacts", [])):
        for key in ("name", "path", "ports", "coverage"):
            if key not in artifact:
                errors.append(f"artifacts[{index}] missing {key}")
        if artifact.get("requires_dc") and not artifact.get("coverage", {}).get("has_dc"):
            errors.append(f"artifacts[{index}] requires DC but coverage.has_dc is false")
        if artifact.get("coverage", {}).get("band_limited") and plan.get("evidence_level") in {"signoff", "final"}:
            errors.append(f"artifacts[{index}] is band-limited for final/signoff evidence")
    if plan.get("mode") == "replace" and not plan.get("control_experiment", {}).get("passed"):
        errors.append("replace mode requires a passed control_experiment")
    return errors


def run_cosim(plan: dict, out: Path) -> dict:
    """Project-specific cosim hook."""
    raise NotImplementedError("fill in project-specific cosim embedding action")


def write_summary(out: Path, evidence: dict) -> None:
    lines = [
        "# Cosim Embedding Evidence",
        "",
        f"- candidate: `{evidence['candidate']}`",
        f"- mode: `{evidence.get('mode', '')}`",
        f"- verdict: `{evidence['verdict']}`",
        f"- artifact_count: `{evidence.get('artifact_count', 0)}`",
        "",
        "Promotion requires the embedded circuit to pass the configured metric gate, not only this embedding-plan audit.",
    ]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--embedding-plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = load_json(args.embedding_plan)
    errors = validate_embedding_plan(plan)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    evidence = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidate": args.candidate,
        "family": "cosim_embedding",
        "mode": plan.get("mode", ""),
        "artifact_count": len(plan.get("artifacts", [])),
        "validation_errors": errors,
    }
    write_json(out / "embedding_run_plan.json", {**plan, "validation_errors": errors})
    if errors:
        evidence["verdict"] = "reject_invalid_plan"
        write_json(out / "evidence.json", evidence)
        write_summary(out, evidence)
        print(json.dumps(evidence, indent=2))
        return 2
    if args.dry_run:
        evidence["verdict"] = "dry_run_pass"
        evidence["metric_gate_required"] = True
    else:
        evidence = run_cosim(plan, out)
    write_json(out / "evidence.json", evidence)
    write_summary(out, evidence)
    print(json.dumps(evidence, indent=2))
    return 0 if evidence.get("verdict", "").endswith("pass") else 2


if __name__ == "__main__":
    raise SystemExit(main())
