#!/usr/bin/env python3
"""Template: EDA schematic generation harness.

Copy this file into a project and fill in `run_eda_database_builder`.
The template is intentionally generic: it does not know a PDK, tool path,
library name, device name, frequency range, or metric threshold.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


REQUIRED_DESIGN_KEYS = {"cell", "instances", "connections"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def validate_design_spec(spec: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_DESIGN_KEYS - set(spec))
    if missing:
        errors.append("missing design keys: " + ", ".join(missing))
    if not isinstance(spec.get("instances", []), list):
        errors.append("instances must be a list")
    if not isinstance(spec.get("connections", []), list):
        errors.append("connections must be a list")
    for index, inst in enumerate(spec.get("instances", [])):
        for key in ("name", "symbol", "parameters"):
            if key not in inst:
                errors.append(f"instances[{index}] missing {key}")
    for index, conn in enumerate(spec.get("connections", [])):
        if "from" not in conn or "to" not in conn:
            errors.append(f"connections[{index}] must include from and to endpoints")
        if conn.get("method") == "terminal_label":
            errors.append(f"connections[{index}] uses terminal_label; use explicit wire/metal connectivity")
    return errors


def build_plan(spec: dict, eda_config: dict, candidate: str) -> dict:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidate": candidate,
        "cell": spec.get("cell", {}),
        "instance_count": len(spec.get("instances", [])),
        "connection_count": len(spec.get("connections", [])),
        "eda_runtime_configured": bool(eda_config.get("eda_runtime") or eda_config.get("python")),
        "drawing_rules": [
            "explicit pin-to-pin wires",
            "hidden wire labels only after real wires exist",
            "ground name comes from project config",
            "bias and decoupling are visible",
            "no forbidden ideal final elements",
        ],
    }


def run_eda_database_builder(plan: dict, spec: dict, eda_config: dict, out: Path) -> dict:
    """Project-specific EDA implementation hook.

    Replace this with calls into the user's configured EDA runtime. The hook
    should create/update the schematic cell, export a netlist or manifest, and
    run connectivity audits. Keep all tool paths in project config.
    """
    raise NotImplementedError("fill in project-specific EDA schematic builder")


def write_summary(out: Path, evidence: dict) -> None:
    lines = [
        "# Schematic Generation Evidence",
        "",
        f"- candidate: `{evidence['candidate']}`",
        f"- verdict: `{evidence['verdict']}`",
        f"- cell: `{evidence.get('cell', {}).get('name', '')}`",
        f"- instance_count: `{evidence.get('instance_count', 0)}`",
        f"- connection_count: `{evidence.get('connection_count', 0)}`",
        "",
        "This evidence is schematic-generation evidence only. It is not layout, EM, or signoff evidence.",
    ]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--design-spec", required=True, type=Path)
    parser.add_argument("--eda-config", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec = load_json(args.design_spec)
    eda_config = load_json(args.eda_config)
    errors = validate_design_spec(spec)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    plan = build_plan(spec, eda_config, args.candidate)
    plan["validation_errors"] = errors
    write_json(out / "schematic_build_plan.json", plan)

    if errors:
        evidence = {**plan, "verdict": "reject_invalid_spec"}
        write_json(out / "evidence.json", evidence)
        write_summary(out, evidence)
        print(json.dumps(evidence, indent=2))
        return 2

    if args.dry_run:
        evidence = {**plan, "verdict": "dry_run_pass"}
    else:
        evidence = run_eda_database_builder(plan, spec, eda_config, out)
    write_json(out / "evidence.json", evidence)
    write_summary(out, evidence)
    print(json.dumps(evidence, indent=2))
    return 0 if evidence.get("verdict", "").endswith("pass") else 2


if __name__ == "__main__":
    raise SystemExit(main())
