#!/usr/bin/env python3
"""Template: incremental RF layout growth harness."""

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


def validate_block_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    for key in ("layout_cell", "block_name", "instances", "routes", "review"):
        if key not in plan:
            errors.append(f"missing {key}")
    if len(plan.get("blocks", [])) > 1:
        errors.append("layout growth template expects one block per run")
    for index, route in enumerate(plan.get("routes", [])):
        if route.get("style") == "all_net_autoroute":
            errors.append(f"routes[{index}] uses all_net_autoroute; use RF-intent route geometry")
        if route.get("rf") and route.get("corner_style") == "right_angle":
            errors.append(f"routes[{index}] uses right_angle on RF route")
    return errors


def run_eda_layout_growth(plan: dict, out: Path) -> dict:
    """Project-specific layout implementation hook."""
    raise NotImplementedError("fill in project-specific EDA layout growth action")


def write_summary(out: Path, evidence: dict) -> None:
    lines = [
        "# Layout Growth Evidence",
        "",
        f"- candidate: `{evidence['candidate']}`",
        f"- block: `{evidence.get('block_name', '')}`",
        f"- verdict: `{evidence['verdict']}`",
        f"- route_count: `{evidence.get('route_count', 0)}`",
        "",
        "Required next checks: screenshot review, pin-net diff, conductive geometry coverage, and local cosim when metric-sensitive.",
    ]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--block-plan", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plan = load_json(args.block_plan)
    errors = validate_block_plan(plan)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    evidence = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "candidate": args.candidate,
        "family": "layout_growth",
        "layout_cell": plan.get("layout_cell", {}),
        "block_name": plan.get("block_name", ""),
        "route_count": len(plan.get("routes", [])),
        "screenshot_requests": plan.get("review", {}).get("screenshots", []),
        "validation_errors": errors,
    }
    write_json(out / "layout_growth_plan.json", {**plan, "validation_errors": errors})
    if errors:
        evidence["verdict"] = "reject_invalid_plan"
        write_json(out / "evidence.json", evidence)
        write_summary(out, evidence)
        print(json.dumps(evidence, indent=2))
        return 2
    if args.dry_run:
        evidence["verdict"] = "dry_run_pass"
        evidence["geometry_coverage_required"] = True
        evidence["visual_review_required"] = True
    else:
        evidence = run_eda_layout_growth(plan, out)
    write_json(out / "evidence.json", evidence)
    write_summary(out, evidence)
    print(json.dumps(evidence, indent=2))
    return 0 if evidence.get("verdict", "").endswith("pass") else 2


if __name__ == "__main__":
    raise SystemExit(main())
