from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "rf-eda-lna-agent" / "scripts"
TEMPLATES = ROOT / "skills" / "rf-eda-lna-agent" / "templates"


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

    def test_script_family_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "legacy"
            (root / "scripts").mkdir(parents=True)
            (root / "docs").mkdir()
            (root / "scripts" / "candidate_optimizer_sweep.py").write_text("run optimizer sweep", encoding="utf-8")
            (root / "scripts" / "layout_gui_screenshot.py").write_text("capture layout screenshot", encoding="utf-8")
            (root / "docs" / "em_cosim_notes.md").write_text("Momentum SnP embedding notes", encoding="utf-8")
            out = Path(td) / "families"
            proc = run_script("script_family_inventory.py", "--root", root, "--out", out)
            self.assertIn('"verdict": "ok"', proc.stdout)
            data = json.loads((out / "script_family_inventory.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(data["counts"].get("optimizer_or_sweep", 0), 1)
            self.assertGreaterEqual(data["counts"].get("layout_gui", 0), 1)
            self.assertGreaterEqual(data["counts"].get("em_cosim", 0), 1)

    def test_history_remote_audit_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            local = Path(td) / "local"
            snap = Path(td) / "snapshot"
            (local / "docs").mkdir(parents=True)
            (snap / "docs").mkdir(parents=True)
            (local / "scripts").mkdir()
            (snap / "scripts").mkdir()
            (local / "docs" / "same.md").write_text("same", encoding="utf-8")
            (snap / "docs" / "same.md").write_text("same", encoding="utf-8")
            (local / "docs" / "changed.md").write_text("new", encoding="utf-8")
            (snap / "docs" / "changed.md").write_text("old", encoding="utf-8")
            (snap / "scripts" / "remote_only.py").write_text("print('remote')", encoding="utf-8")
            out = Path(td) / "audit"
            run_script("history_remote_audit.py", "--root", local, "--snapshot", f"old={snap}", "--out", out)
            data = json.loads((out / "history_remote_audit.json").read_text(encoding="utf-8"))
            diff = data["snapshots"][0]
            self.assertIn("docs/changed.md", diff["changed"])
            self.assertIn("scripts/remote_only.py", diff["snapshot_only"])

    def test_failure_catalog_append(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            catalog = root / "docs" / "failure_catalog.md"
            registry = root / "manifests" / "failure_catalog.jsonl"
            proc = run_script(
                "failure_catalog_append.py",
                "--catalog",
                catalog,
                "--registry",
                registry,
                "--category",
                "optimizer",
                "--symptom",
                "hard gate omitted",
                "--root-cause",
                "objective was incomplete",
                "--response",
                "reject and rerun",
                "--status",
                "retired",
            )
            self.assertIn('"verdict": "ok"', proc.stdout)
            self.assertIn("hard gate omitted", catalog.read_text(encoding="utf-8"))
            lines = registry.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(json.loads(lines[0])["status"], "retired")

    def test_harness_scaffold_and_evidence_gate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "harnesses"
            proc = run_script("harness_scaffold.py", "--family", "optimizer", "--name", "c001_optimizer", "--out", out)
            self.assertIn('"verdict": "ok"', proc.stdout)
            scaffold = out / "c001_optimizer.py"
            self.assertTrue(scaffold.exists())
            dry = subprocess.run(
                [
                    sys.executable,
                    str(scaffold),
                    "--project",
                    str(root),
                    "--candidate",
                    "C001",
                    "--out",
                    str(root / "evidence"),
                    "--dry-run",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertTrue((root / "evidence" / "evidence.json").exists())

            candidate = root / "candidate.json"
            candidate.write_text(
                json.dumps(
                    {
                        "id": "C001",
                        "evidence_level": "E5",
                        "hard_checks": {"gain": True, "match": True},
                        "red_flags": [],
                    }
                ),
                encoding="utf-8",
            )
            gate = run_script(
                "evidence_gate.py",
                "--candidate-json",
                candidate,
                "--required-evidence",
                "E4",
                "--require-hard-pass",
                "--forbid-red-flags",
            )
            self.assertIn('"verdict": "promote"', gate.stdout)
            candidate.write_text(
                json.dumps(
                    {
                        "id": "C001",
                        "evidence_level": "E2",
                        "hard_checks": {"gain": True, "match": False},
                        "red_flags": ["port_reference_uncertain"],
                    }
                ),
                encoding="utf-8",
            )
            blocked = run_script(
                "evidence_gate.py",
                "--candidate-json",
                candidate,
                "--required-evidence",
                "E4",
                "--require-hard-pass",
                "--forbid-red-flags",
                check=False,
            )
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn('"verdict": "provisional"', blocked.stdout)

    def test_materialize_and_template_dry_runs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            materialized = root / "scripts"
            proc = run_script(
                "materialize_template.py",
                "--template",
                "schematic",
                "--name",
                "c001_schematic_builder",
                "--out-dir",
                materialized,
            )
            self.assertIn('"verdict": "ok"', proc.stdout)
            self.assertTrue((materialized / "c001_schematic_builder.py").exists())
            self.assertTrue((materialized / "c001_schematic_builder.template_manifest.json").exists())

            examples = TEMPLATES / "examples"
            harnesses = TEMPLATES / "harnesses"
            cases = [
                (
                    "schematic_generation_template.py",
                    [
                        "--candidate",
                        "C001",
                        "--design-spec",
                        examples / "schematic_design_spec.example.json",
                        "--eda-config",
                        examples / "eda_config.example.json",
                    ],
                ),
                (
                    "layout_growth_template.py",
                    [
                        "--candidate",
                        "C001",
                        "--block-plan",
                        examples / "layout_block_plan.example.json",
                    ],
                ),
                (
                    "em_extraction_template.py",
                    [
                        "--candidate",
                        "C001",
                        "--em-plan",
                        examples / "em_plan.example.json",
                    ],
                ),
                (
                    "cosim_embedding_template.py",
                    [
                        "--candidate",
                        "C001",
                        "--embedding-plan",
                        examples / "embedding_plan.example.json",
                    ],
                ),
                (
                    "optimizer_invocation_template.py",
                    [
                        "--candidate",
                        "C001",
                        "--optimizer-plan",
                        examples / "optimizer_plan.example.json",
                    ],
                ),
            ]
            for index, (script, args) in enumerate(cases):
                out = root / f"template_case_{index}"
                proc2 = subprocess.run(
                    [
                        sys.executable,
                        str(harnesses / script),
                        *map(str, args),
                        "--out",
                        str(out),
                        "--dry-run",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(proc2.returncode, 0, f"{script}\nSTDOUT:\n{proc2.stdout}\nSTDERR:\n{proc2.stderr}")
                self.assertIn('"verdict": "dry_run_pass"', proc2.stdout)
                self.assertTrue((out / "evidence.json").exists())


if __name__ == "__main__":
    unittest.main()
