from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "rf-eda-lna-agent" / "scripts"


def run_script(name: str, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if check and proc.returncode != 0:
        raise AssertionError(f"{name} failed\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc


class ScriptTests(unittest.TestCase):
    def test_init_project_append_and_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            project = Path(td) / "project"
            run_script("init_project.py", "--root", project, "--project-name", "synthetic", "--allow-tbd")
            self.assertTrue((project / "goal.md").exists())
            self.assertTrue((project / "config" / "metrics.yaml").exists())

            run_script(
                "exploration_tree_append.py",
                "--tree",
                project / "docs" / "exploration_tree.md",
                "--registry",
                project / "manifests" / "candidate_registry.jsonl",
                "--candidate",
                "C001",
                "--branch",
                "baseline",
                "--hypothesis",
                "synthetic baseline",
                "--evidence-level",
                "E1",
                "--decision",
                "continue",
            )
            out = Path(td) / "inventory"
            run_script("inventory_project.py", "--root", project, "--out", out, "--candidate-regex", r"(?P<id>C\d{3})")
            data = json.loads((out / "project_inventory.json").read_text(encoding="utf-8"))
            self.assertEqual(data["candidate_count"], 1)

    def test_metrics_gate_pass_and_fail(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            metrics = root / "metrics.json"
            targets = root / "targets.json"
            metrics.write_text(json.dumps({"gain": 3.0}), encoding="utf-8")
            targets.write_text(json.dumps({"hard_targets": [{"metric": "gain", "operator": ">=", "value": 2.0}]}), encoding="utf-8")
            passed = run_script("metrics_gate.py", "--metrics-json", metrics, "--targets-json", targets)
            self.assertIn('"verdict": "pass"', passed.stdout)
            targets.write_text(json.dumps({"hard_targets": [{"metric": "gain", "operator": ">=", "value": 4.0}]}), encoding="utf-8")
            failed = run_script("metrics_gate.py", "--metrics-json", metrics, "--targets-json", targets, check=False)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn('"verdict": "fail"', failed.stdout)

    def test_touchstone_audit_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            s2p = Path(td) / ("block." + "s2p")
            s2p.write_text(
                "# Hz S RI R 50\n"
                "0 0 0 1 0 1 0 0 0\n"
                "1 0 0 1 0 1 0 0 0\n",
                encoding="utf-8",
            )
            ok = run_script("touchstone_audit.py", s2p, "--expect-ports", "2", "--require-dc")
            self.assertIn('"verdict": "audit_pass"', ok.stdout)
            band = run_script("touchstone_audit.py", s2p, "--expect-ports", "2", "--max-freq", "2")
            self.assertIn('"verdict": "band_limited"', band.stdout)
            port = run_script("touchstone_audit.py", s2p, "--expect-ports", "3", check=False)
            self.assertNotEqual(port.returncode, 0)
            self.assertIn("reject_port_count", port.stdout)

    def test_status_artifact_and_signoff_helpers(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            status = root / "docs" / "status.md"
            run_script(
                "status_append.py",
                "--status-file",
                status,
                "--candidate",
                "C001",
                "--evidence-level",
                "E2",
                "--verdict",
                "provisional",
                "--summary",
                "synthetic status",
            )
            self.assertIn("synthetic status", status.read_text(encoding="utf-8"))

            budget = run_script("artifact_guard.py", "--root", root, "--max-bytes", "1", check=False)
            self.assertNotEqual(budget.returncode, 0)
            self.assertIn("fail_budget", budget.stdout)

            signoff = run_script("signoff_readiness.py", "--require-drc", "--require-lvs", check=False)
            self.assertNotEqual(signoff.returncode, 0)
            self.assertIn("blocked_external", signoff.stdout)


if __name__ == "__main__":
    unittest.main()
