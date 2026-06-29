#!/usr/bin/env python3
"""Evaluate user-configured metric targets against measured metric JSON."""
from __future__ import annotations

import argparse
import json
import operator
from pathlib import Path
from typing import Any


OPS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "=": operator.eq,
}


def load_metrics(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "metrics" in payload and isinstance(payload["metrics"], list):
        return {str(item["name"]): item.get("value") for item in payload["metrics"]}
    if "metrics" in payload and isinstance(payload["metrics"], dict):
        return payload["metrics"]
    return payload


def load_targets(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("hard_targets", []))


def evaluate(metrics: dict[str, Any], targets: list[dict[str, Any]]) -> dict[str, Any]:
    checks = []
    all_pass = True
    for target in targets:
        name = str(target["metric"])
        op = str(target["operator"])
        expected = target.get("value")
        measured = metrics.get(name)
        if op not in OPS:
            verdict = "fail_unknown_operator"
            passed = False
        elif measured is None:
            verdict = "fail_missing_metric"
            passed = False
        else:
            try:
                passed = bool(OPS[op](float(measured), float(expected)))
                verdict = "pass" if passed else "fail"
            except (TypeError, ValueError):
                passed = measured == expected if op in {"=", "=="} else False
                verdict = "pass" if passed else "fail_non_numeric"
        all_pass = all_pass and passed
        checks.append(
            {
                "metric": name,
                "measured": measured,
                "operator": op,
                "target": expected,
                "unit": target.get("unit"),
                "verdict": verdict,
            }
        )
    return {"verdict": "pass" if all_pass else "fail", "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate metric JSON against target JSON.")
    parser.add_argument("--metrics-json", type=Path, required=True)
    parser.add_argument("--targets-json", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    result = evaluate(load_metrics(args.metrics_json), load_targets(args.targets_json))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["verdict"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
