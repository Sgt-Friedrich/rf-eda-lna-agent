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

## Reference Routing

- New project or missing metrics: read `references/user-intake-and-bootstrap.md`.
- Config schema or project file shape: read `references/configuration-schema.md`.
- Candidate history or GitHub exploration tree: read `references/exploration-tree-management.md`.
- Long workflow planning: read `references/agent-architecture.md`.
- Simulation, optimizer, EM, layout, or signoff harness design: read `references/harness-contracts.md`.
- Optimizer behavior or retuning discipline: read `references/optimizer-policy.md`.
- EM extraction, Touchstone embedding, or audit-vs-replace decisions: read `references/em-cosim-policy.md`.
- Layout drawing, screenshot review, or connectivity closure: read `references/layout-growth-policy.md`.
- DRC/LVS or delivery readiness: read `references/signoff-readiness-policy.md`.
- Suspicious optimizer/EM/layout behavior: read `references/failure-catalog.md`.
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

## Safety Rules

- No local absolute paths in public artifacts.
- No proprietary PDK files, foundry decks, private layouts, solver outputs, or screenshots in the public package.
- No signoff-clean claim without official reports.
- No silent relaxation of user hard targets.
- No automatic deletion outside the configured workspace.
