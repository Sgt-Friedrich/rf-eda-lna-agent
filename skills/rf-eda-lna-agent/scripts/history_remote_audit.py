#!/usr/bin/env python3
"""Compare a local project tree with one or more history snapshots by path/hash."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path


DEFAULT_INCLUDE_DIRS = ("docs", "scripts", "config", "manifests", "skills", "examples")
DEFAULT_EXCLUDE_DIRS = {".git", "__pycache__", "build", "node_modules"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def collect(root: Path, include_dirs: tuple[str, ...], exclude_dirs: set[str]) -> dict[str, str]:
    files: dict[str, str] = {}
    for top in include_dirs:
        start = root / top
        if not start.exists():
            continue
        for path in start.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(root).parts
            if any(part in exclude_dirs for part in rel_parts[:-1]):
                continue
            files[Path(*rel_parts).as_posix()] = sha256(path)
    return files


def parse_snapshot(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("snapshot must be NAME=PATH")
    name, raw_path = value.split("=", 1)
    if not name:
        raise argparse.ArgumentTypeError("snapshot name cannot be empty")
    path = Path(raw_path).resolve()
    if not path.exists():
        raise argparse.ArgumentTypeError(f"snapshot path does not exist: {path}")
    return name, path


def archive_git_ref(root: Path, ref: str, temp_root: Path) -> Path:
    safe = ref.replace("/", "_").replace("\\", "_").replace(":", "_")
    out = temp_root / safe
    out.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "-C", str(root), "archive", ref],
        check=False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode(errors="ignore") or f"git archive failed for {ref}")
    tar = subprocess.run(
        ["tar", "-x", "-C", str(out)],
        input=proc.stdout,
        check=False,
        capture_output=True,
    )
    if tar.returncode != 0:
        raise RuntimeError(tar.stderr.decode(errors="ignore") or f"tar extract failed for {ref}")
    return out


def compare(local: dict[str, str], other: dict[str, str]) -> dict[str, list[str]]:
    local_paths = set(local)
    other_paths = set(other)
    common = local_paths & other_paths
    changed = sorted(path for path in common if local[path] != other[path])
    return {
        "local_only": sorted(local_paths - other_paths),
        "snapshot_only": sorted(other_paths - local_paths),
        "changed": changed,
        "same": sorted(path for path in common if local[path] == other[path]),
    }


def write_markdown(out: Path, result: dict) -> None:
    lines = ["# History Remote Audit", ""]
    lines.append(f"Root: `{result['root']}`")
    lines.append("")
    for snap in result["snapshots"]:
        lines.append(f"## {snap['name']}")
        lines.append("")
        lines.append("| category | count |")
        lines.append("|---|---:|")
        for key in ("local_only", "snapshot_only", "changed", "same"):
            lines.append(f"| {key} | {len(snap[key])} |")
        lines.append("")
        for key in ("snapshot_only", "changed", "local_only"):
            if snap[key]:
                lines.append(f"### {key}")
                lines.append("")
                for item in snap[key][:50]:
                    lines.append(f"- `{item}`")
                if len(snap[key]) > 50:
                    lines.append(f"- ... {len(snap[key]) - 50} more")
                lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--snapshot", action="append", type=parse_snapshot, default=[])
    parser.add_argument("--git-ref", action="append", default=[])
    parser.add_argument("--include-dir", action="append", default=None)
    parser.add_argument("--exclude-dir", action="append", default=list(DEFAULT_EXCLUDE_DIRS))
    args = parser.parse_args()

    root = args.root.resolve()
    include_dirs = tuple(args.include_dir or DEFAULT_INCLUDE_DIRS)
    exclude_dirs = set(args.exclude_dir or [])
    local = collect(root, include_dirs, exclude_dirs)
    snapshots = list(args.snapshot)

    with tempfile.TemporaryDirectory() as td:
        temp_root = Path(td)
        for ref in args.git_ref:
            snapshots.append((f"git:{ref}", archive_git_ref(root, ref, temp_root)))

        result = {"root": str(root), "include_dirs": include_dirs, "snapshots": []}
        for name, path in snapshots:
            other = collect(path, include_dirs, exclude_dirs)
            diff = compare(local, other)
            diff.update({"name": name, "path": str(path), "file_count": len(other)})
            result["snapshots"].append(diff)

        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "history_remote_audit.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        write_markdown(args.out / "history_remote_audit.md", result)
        print(json.dumps({"verdict": "ok", "local_file_count": len(local), "snapshots": len(result["snapshots"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
