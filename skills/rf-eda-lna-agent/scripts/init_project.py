#!/usr/bin/env python3
"""Bootstrap a generic RF/EDA agent project from user-supplied intent."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def q(value: str | None) -> str:
    if value is None or value == "":
        return "TBD"
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def parse_target(raw: str) -> dict[str, str]:
    parts = [p.strip() for p in raw.split(",")]
    if len(parts) < 7:
        raise argparse.ArgumentTypeError(
            "target must be metric,analysis,operator,value,unit,aggregation,evidence_required"
        )
    return {
        "metric": parts[0],
        "analysis": parts[1],
        "operator": parts[2],
        "value": parts[3],
        "unit": parts[4],
        "aggregation": parts[5],
        "evidence_required": parts[6],
    }


def write(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} exists; pass --force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def render_project(args: argparse.Namespace) -> str:
    return f"""project:
  name: {q(args.project_name)}
  privacy: {q(args.privacy)}
  workspace_root: {q(args.workspace_root)}
  candidate_prefix: {q(args.candidate_prefix)}
  candidate_regex: {q(args.candidate_regex)}

eda:
  tool_family: {q(args.eda_tool)}
  tool_version: {q(args.eda_version)}
  launch_command: {q(args.launch_command)}
  sim_command: {q(args.sim_command)}
  python_command: {q(args.python_command)}

pdk:
  profile_name: {q(args.pdk_profile)}
  signoff_decks_required: {str(args.signoff_decks_required).lower()}
  drc_deck: {q(args.drc_deck)}
  lvs_deck: {q(args.lvs_deck)}
  layer_map: {q(args.layer_map)}
  device_map: {q(args.device_map)}

workflow:
  allow_gui: {str(args.allow_gui).lower()}
  allow_remote_git: {str(args.allow_remote_git).lower()}
  github_repository: {q(args.github_repository)}
  max_parallel_jobs: {q(args.max_parallel_jobs)}
"""


def render_metric_list(name: str, targets: list[dict[str, str]]) -> list[str]:
    lines = [f"{name}:"]
    if not targets:
        lines.append("  []")
        return lines
    for target in targets:
        lines += [
            f"  - metric: {q(target['metric'])}",
            f"    analysis: {q(target['analysis'])}",
            f"    operator: {q(target['operator'])}",
            f"    value: {q(target['value'])}",
            f"    unit: {q(target['unit'])}",
            f"    aggregation: {q(target['aggregation'])}",
            f"    evidence_required: {q(target.get('evidence_required', 'TBD'))}",
        ]
    return lines


def render_metrics(args: argparse.Namespace) -> str:
    analyses = [
        "analyses:",
        f"  - name: {q(args.analysis_name)}",
        f"    type: {q(args.analysis_type)}",
        "    range:",
        f"      start: {q(args.range_start)}",
        f"      stop: {q(args.range_stop)}",
        f"      unit: {q(args.range_unit)}",
    ]
    hard = render_metric_list("hard_targets", args.hard_target)
    stretch = render_metric_list("stretch_targets", args.stretch_target)
    report_only = ["report_only:"]
    if not args.report_only:
        report_only.append("  []")
    else:
        for name in args.report_only:
            report_only += [
                f"  - metric: {q(name)}",
                f"    analysis: {q(args.analysis_name)}",
                "    unit: TBD",
                "    aggregation: TBD",
            ]
    return "\n".join(analyses + [""] + hard + [""] + stretch + [""] + report_only) + "\n"


def render_artifact_policy(args: argparse.Namespace) -> str:
    return f"""budget:
  max_repository_size: {q(args.max_repository_size)}
  max_repository_size_unit: {q(args.max_repository_size_unit)}
  max_single_run_temp_size: {q(args.max_single_run_temp_size)}
  max_single_run_temp_size_unit: {q(args.max_single_run_temp_size_unit)}

retain:
  status_docs: true
  metric_json: true
  final_netlists: true
  selected_screenshots: true
  promoted_touchstone: true
  raw_solver_workdirs: false
  remote_snapshots_after_inventory: false

cleanup:
  require_manifest_before_delete: true
  delete_only_inside_workspace: true
  preserve_promoted_artifacts: true
"""


def render_goal(args: argparse.Namespace) -> str:
    return f"""# Goal

## Design Contract

- project: {args.project_name or 'TBD'}
- circuit/application: {args.circuit or 'TBD'}
- analyses: see `config/metrics.yaml`
- hard targets: see `config/metrics.yaml`
- stretch targets: see `config/metrics.yaml`
- deliverables: {args.deliverables or 'TBD'}

## Rules

- User hard targets cannot be changed without user approval.
- No result is promoted unless it reaches the required evidence level.
- No signoff-clean claim without required official reports.
- Heavy artifacts are governed by `config/artifact_policy.yaml`.
- Every candidate must update `docs/exploration_tree.md`.

## Current State

- latest candidate: none
- evidence level: E0
- blocker: none
- next action: build baseline harness
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a generic RF/EDA agent project scaffold.")
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--circuit")
    parser.add_argument("--deliverables")
    parser.add_argument("--privacy", default="private")
    parser.add_argument("--workspace-root")
    parser.add_argument("--candidate-prefix", default="C")
    parser.add_argument("--candidate-regex", default=r"(?P<id>C\d{3})")
    parser.add_argument("--eda-tool")
    parser.add_argument("--eda-version")
    parser.add_argument("--launch-command")
    parser.add_argument("--sim-command")
    parser.add_argument("--python-command")
    parser.add_argument("--pdk-profile")
    parser.add_argument("--signoff-decks-required", action="store_true")
    parser.add_argument("--drc-deck")
    parser.add_argument("--lvs-deck")
    parser.add_argument("--layer-map")
    parser.add_argument("--device-map")
    parser.add_argument("--allow-gui", action="store_true")
    parser.add_argument("--allow-remote-git", action="store_true")
    parser.add_argument("--github-repository")
    parser.add_argument("--max-parallel-jobs")
    parser.add_argument("--analysis-name", default="TBD")
    parser.add_argument("--analysis-type", default="custom")
    parser.add_argument("--range-start")
    parser.add_argument("--range-stop")
    parser.add_argument("--range-unit")
    parser.add_argument("--hard-target", action="append", type=parse_target, default=[])
    parser.add_argument("--stretch-target", action="append", type=parse_target, default=[])
    parser.add_argument("--report-only", action="append", default=[])
    parser.add_argument("--max-repository-size")
    parser.add_argument("--max-repository-size-unit")
    parser.add_argument("--max-single-run-temp-size")
    parser.add_argument("--max-single-run-temp-size-unit")
    parser.add_argument("--allow-tbd", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not args.allow_tbd and not args.hard_target:
        raise SystemExit("At least one --hard-target is required unless --allow-tbd is set")

    root = args.root.resolve()
    files = {
        root / "config" / "project.yaml": render_project(args),
        root / "config" / "metrics.yaml": render_metrics(args),
        root / "config" / "artifact_policy.yaml": render_artifact_policy(args),
        root / "goal.md": render_goal(args),
        root / "docs" / "exploration_tree.md": "# Exploration Tree\n\n## Active\n\nNo candidates yet.\n",
        root / "docs" / "decision_log.md": "# Decision Log\n\nNo decisions recorded yet.\n",
        root / "docs" / "failure_catalog.md": "# Failure Catalog\n\nNo project-specific failures recorded yet.\n",
        root / "manifests" / "artifact_manifest.json": json.dumps(
            {"schema": "rf-eda-artifact-manifest-v1", "artifacts": []}, indent=2
        )
        + "\n",
    }
    for path, content in files.items():
        write(path, content, args.force)
    for dirname in ("scripts", "results"):
        (root / dirname).mkdir(parents=True, exist_ok=True)
    print(json.dumps({"status": "pass_init_project", "root": str(root), "files": len(files)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
