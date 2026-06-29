---
name: rf-eda-lna-agent
description: "Use when Codex is asked to assist an RF/LNA EDA workflow: collect user-defined metrics, create a goal file, maintain a GitHub exploration tree, run bounded simulation/optimizer/EM/layout harnesses, audit evidence, and report signoff readiness without assuming a specific process, tool path, frequency band, or target."
---

# RF EDA LNA Agent

Use this skill for configurable RF/LNA design automation around EDA workspaces.

## Required Behavior

1. If no project contract exists, run user intake first.
2. Never invent target values. Frequency range, metrics, thresholds, topology limits, artifact budget, and signoff expectations must come from the user or config.
3. Create or maintain:
   - `config/project.yaml`
   - `config/metrics.yaml`
   - `config/artifact_policy.yaml`
   - `goal.md`
   - `docs/exploration_tree.md`
4. Use the smallest harness that can answer the current question.
5. Promote candidates only when their evidence level matches the configured gate.
6. Use GitHub as the exploration-tree record when requested, but do not push heavy solver artifacts unless explicitly configured.
7. Stop truthfully at missing EDA tools, missing official signoff decks, repeated hard-gate failure, or operations that would exceed the artifact budget.

## Default Execution Protocol

When a user asks the agent to work on an RF/EDA design, follow this protocol:

1. **Orient**: locate `goal.md`, configs, exploration tree, and artifact policy. If they are absent, run intake and bootstrap instead of simulating.
2. **Audit history**: inventory local docs/scripts/results and, when the project uses GitHub or archives, compare remote/snapshot history before claiming a branch is new or exhausted.
3. **Classify the task**: mechanism search, candidate optimization, EM/cosim, layout growth, signoff readiness, report/export, or blocker resolution.
4. **Pick the smallest valid harness**: do not run a broad optimizer when a control embedding, Touchstone audit, or geometry check can answer the question.
5. **Keep hard gates active**: every configured hard metric must be in the optimizer objective or in a mandatory rejection gate.
6. **Verify independently**: optimizer rows, generated layouts, and embedded SnP results need a separate verification run before promotion.
7. **Record evidence**: append status, candidate record, artifact manifest, failure notes, and do-not-repeat rules.
8. **Clean up deliberately**: keep the repository under artifact budget, avoid deleting evidence for the active gate, and do not kill unrelated EDA processes.

## Embedded Lessons

The skill must apply these lessons without waiting for the user to restate them:

- Low-level mechanism evidence is not final candidate evidence.
- Analytical schematic primitives can be optimistic; physical geometry must be verified at the evidence level required by the gate.
- A black-box SnP replacement can invalidate DC, noise, or high-impedance node semantics even when the standalone file looks healthy.
- Coarse-grid optimizer passes, single-metric wins, and near-stability gain peaks are provisional until fine verified.
- Pin/net-name equivalence is not physical metal connectivity.
- Full passive EM is not active/noise signoff unless active/model partitions are reintroduced correctly.
- Missing official signoff decks are external blockers, not clean reports.
- Heavy EDA outputs should be represented by manifests unless the artifact policy explicitly allows storing them.

## Reference Routing

- New project or missing metrics: read `references/user-intake-and-bootstrap.md`.
- Config schema or project file shape: read `references/configuration-schema.md`.
- Candidate history or GitHub exploration tree: read `references/exploration-tree-management.md`.
- Historical project mining, remote branch comparison, or "learn from all prior runs": read `references/history-mining-and-remote-audit.md`.
- Long workflow planning: read `references/agent-architecture.md`.
- Netlist mechanism exploration or simulator harness planning: read `references/netlist-exploration-playbook.md`.
- EDA schematic generation or GUI schematic acceptance: read `references/schematic-generation-playbook.md`.
- Simulation, optimizer, EM, layout, or signoff harness design: read `references/harness-contracts.md`.
- Large script/harness migration into generic templates: read `references/deep-harness-playbook.md`.
- Selecting or copying a standard script template: read `references/template-script-library.md`.
- EDA runtime, GUI/database automation, generated schematics, or tool callback problems: read `references/eda-adapter-patterns.md`.
- RF design reasoning, system budgets, literature-to-primitive adaptation, or mechanism-vs-candidate separation: read `references/rf-design-lessons.md`.
- Optimizer behavior or retuning discipline: read `references/optimizer-policy.md`.
- EM-in-the-loop optimizer closure: read `references/em-cosim-optimizer-playbook.md`.
- EM extraction, Touchstone embedding, or audit-vs-replace decisions: read `references/em-cosim-policy.md`.
- Incremental physical layout construction: read `references/layout-exploration-playbook.md`.
- Layout drawing, screenshot review, or connectivity closure: read `references/layout-growth-policy.md`.
- DRC/LVS or delivery readiness: read `references/signoff-readiness-policy.md`.
- Suspicious optimizer/EM/layout behavior: read `references/failure-catalog.md`.
- Avoiding already-closed neighborhoods and repeated dead ends: read `references/do-not-repeat-patterns.md`.
- Repeated failure, missing collateral, or stop/continue decisions: read `references/blocker-and-failure-playbook.md`.
- Open-source or sharing boundary: read `references/export-policy.md`.

## Bundled Scripts

- `scripts/init_project.py`: create config, goal, docs, manifests, and result folders from user input.
- `scripts/inventory_project.py`: index candidates, docs, scripts, reports, and artifacts.
- `scripts/metrics_gate.py`: evaluate measured metrics against user-supplied target JSON.
- `scripts/touchstone_audit.py`: inspect Touchstone port count, band coverage, and DC handling.
- `scripts/exploration_tree_append.py`: append a candidate record to Markdown and JSONL.
- `scripts/status_append.py`: append a compact status record.
- `scripts/artifact_guard.py`: report artifact size and largest files without deleting.
- `scripts/signoff_readiness.py`: check signoff collateral presence without claiming clean.
- `scripts/process_guard.py`: list possible EDA-related processes without killing by default.
- `scripts/script_family_inventory.py`: classify a large legacy script/doc tree into generic harness families.
- `scripts/history_remote_audit.py`: compare local and snapshot/ref histories by path and hash without overwriting the worktree.
- `scripts/failure_catalog_append.py`: append structured failure/blocker lessons to Markdown and JSONL.
- `scripts/harness_scaffold.py`: create a parameterized simulation/optimizer/EM/layout/signoff harness skeleton.
- `scripts/evidence_gate.py`: reject promotion when evidence level, hard checks, or red flags do not meet the active gate.
- `scripts/materialize_template.py`: copy a bundled schematic/layout/EM/cosim/optimizer template into a project.

## Bundled Templates

- `templates/harnesses/schematic_generation_template.py`
- `templates/harnesses/layout_growth_template.py`
- `templates/harnesses/em_extraction_template.py`
- `templates/harnesses/cosim_embedding_template.py`
- `templates/harnesses/optimizer_invocation_template.py`
- `templates/examples/*.example.json`

## Safety Rules

- No local absolute paths in public artifacts.
- No proprietary PDK files, foundry decks, private layouts, solver outputs, or screenshots in the public package.
- No signoff-clean claim without official reports.
- No silent relaxation of user hard targets.
- No automatic deletion outside the configured workspace.
- No promotion from a result that only satisfies a lower evidence level than the active gate.
