#!/usr/bin/env python3
"""Copy a bundled harness template into a project workspace."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


TEMPLATE_MAP = {
    "schematic": "schematic_generation_template.py",
    "layout": "layout_growth_template.py",
    "em": "em_extraction_template.py",
    "cosim": "cosim_embedding_template.py",
    "optimizer": "optimizer_invocation_template.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, choices=sorted(TEMPLATE_MAP))
    parser.add_argument("--name", required=True, help="Output script file base name, without extension.")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    src = skill_root / "templates" / "harnesses" / TEMPLATE_MAP[args.template]
    if not src.exists():
        raise SystemExit(f"missing bundled template: {src}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    dst = args.out_dir / f"{args.name}.py"
    if dst.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite existing file without --force: {dst}")
    shutil.copyfile(src, dst)
    manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "template": args.template,
        "source": src.name,
        "output": dst.name,
        "status": "materialized",
        "next_action": "fill project-specific EDA hook and keep user targets in config",
    }
    (args.out_dir / f"{args.name}.template_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": "ok", "output": str(dst)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
