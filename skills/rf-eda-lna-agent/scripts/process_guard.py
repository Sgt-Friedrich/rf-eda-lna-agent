#!/usr/bin/env python3
"""List candidate EDA processes without killing anything by default."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect possible EDA processes.")
    parser.add_argument("--pattern", action="append", default=["ads", "hpeesof", "momentum", "python"])
    args = parser.parse_args()

    if sys.platform.startswith("win"):
        cmd = ["powershell", "-NoProfile", "-Command", "Get-Process | Select-Object Id,ProcessName,CPU,WorkingSet64 | ConvertTo-Json -Depth 3"]
    else:
        cmd = ["ps", "-eo", "pid,comm,rss,pcpu"]
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    output = proc.stdout
    lower_patterns = [p.lower() for p in args.pattern]
    matches = [line for line in output.splitlines() if any(p in line.lower() for p in lower_patterns)]
    payload = {"patterns": args.pattern, "matches": matches}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

