#!/usr/bin/env python3
"""Create a generic RF/EDA harness skeleton with evidence outputs."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


FAMILIES = {
    "simulation": "Build or patch a netlist, run configured analyses, and extract metrics.",
    "optimizer": "Run bounded variables, reject degenerate rows, and verify the best result independently.",
    "em_cosim": "Extract or embed EM artifacts with control experiments and Touchstone audits.",
    "layout_growth": "Add one layout block, capture screenshots, and run connectivity/cosim checks.",
    "signoff": "Check final collateral, official reports, and delivery readiness without claiming clean.",
    "diagnostic": "Isolate a failure mode with a small control experiment.",
}


SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""Generic {family} harness.

Purpose:
    {purpose}

Fill in the tool-specific sections for the user's EDA environment. Keep this
script parameterized; do not hard-code local paths, private PDK names, or metric
thresholds.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path or not path.exists():
        return {{}}
    return json.loads(path.read_text(encoding="utf-8"))


def write_evidence(out: Path, payload: dict) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "evidence.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = ["# Harness Evidence", ""]
    for key, value in payload.items():
        if isinstance(value, (dict, list)):
            continue
        lines.append(f"- {{key}}: `{{value}}`")
    (out / "summary.md").write_text("\\n".join(lines) + "\\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--metrics-config", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    metrics_config = load_json(args.metrics_config) if args.metrics_config else {{}}

    # TODO: implement the EDA/tool-specific action for this harness family.
    # Required discipline:
    # - keep all configured hard gates visible;
    # - write raw logs/manifests before summarizing;
    # - do not promote lower-level evidence as final evidence;
    # - preserve enough paths for reproduction.
    verdict = "dry_run" if args.dry_run else "not_implemented"
    evidence = {{
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "family": "{family}",
        "candidate": args.candidate,
        "project": str(args.project),
        "verdict": verdict,
        "metrics_config_keys": sorted(metrics_config.keys()),
        "next_action": "replace TODO section with project-specific runner",
    }}
    write_evidence(args.out, evidence)
    print(json.dumps(evidence, indent=2))
    return 0 if args.dry_run else 2


if __name__ == "__main__":
    raise SystemExit(main())
'''


README_TEMPLATE = """# {name}

Family: `{family}`

Purpose: {purpose}

## Required Customization

- Configure the EDA runtime from project config.
- Load user-supplied metrics instead of hard-coding targets.
- Write raw logs, metric JSON, and a Markdown summary.
- Update the exploration tree after each run.
- Keep heavy solver artifacts out of Git unless the artifact policy allows them.

## Promotion Boundary

This harness scaffold is not evidence until the TODO sections are implemented
and the output is verified by an independent gate.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", required=True, choices=sorted(FAMILIES))
    parser.add_argument("--name", required=True, help="Harness base name, for example c001_optimizer.")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    script = out / f"{args.name}.py"
    readme = out / f"{args.name}.md"
    manifest = out / f"{args.name}.manifest.json"
    purpose = FAMILIES[args.family]

    script.write_text(SCRIPT_TEMPLATE.format(family=args.family, purpose=purpose), encoding="utf-8")
    readme.write_text(README_TEMPLATE.format(name=args.name, family=args.family, purpose=purpose), encoding="utf-8")
    manifest.write_text(
        json.dumps(
            {
                "created": datetime.now(timezone.utc).isoformat(),
                "family": args.family,
                "name": args.name,
                "files": [script.name, readme.name],
                "status": "scaffold",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(json.dumps({"verdict": "ok", "script": str(script), "manifest": str(manifest)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
