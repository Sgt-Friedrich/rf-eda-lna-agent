# RF EDA LNA Agent

A configurable Codex skill for disciplined RF/LNA design workflows around EDA tools.

This project helps an agent manage:

- user-defined design targets and goals
- exploration trees and candidate history
- simulation and optimizer evidence
- Touchstone and EM/cosim audits
- layout-growth review gates
- signoff-readiness reporting
- artifact and disk-budget hygiene

It does **not** include a PDK, foundry rule deck, private circuit database, private layout, or guaranteed tapeout flow.

## What This Agent Does

The agent acts as a workflow executor and evidence manager. It should not invent RF specs or silently relax goals. Users provide the design contract; the agent creates config files, maintains `goal.md`, updates the exploration tree, runs bounded harnesses, and stops honestly at real blockers.

## Core Principles

- Targets are user supplied. No built-in frequency band, gain, noise, matching, stability, or linearity target is assumed.
- Promotion requires evidence. A candidate must meet the evidence level required by the configured target.
- Optimizer results need verification. Fine-grid or independent verification is required before promotion.
- Layout is grown incrementally. Visual and database connectivity checks are first-class gates.
- Official signoff requires official collateral. DRC/LVS-clean claims require real decks and reports.
- Heavy artifacts stay out of Git unless the user explicitly configures a storage strategy.

## Repository Layout

```text
skills/rf-eda-lna-agent/
  SKILL.md
  references/
    user-intake-and-bootstrap.md
    agent-architecture.md
    harness-contracts.md
    failure-catalog.md
    export-policy.md
  scripts/
    inventory_project.py
    touchstone_audit.py
    status_append.py
examples/synthetic_project/
  config/
  docs/
  scripts/
  results/
```

## First-Run Workflow

1. Ask the user for the design contract.
2. Write `config/project.yaml`, `config/metrics.yaml`, and `config/artifact_policy.yaml`.
3. Create `goal.md` and `docs/exploration_tree.md`.
4. Initialize or connect a GitHub repository if requested.
5. Run the smallest valid harness for the first baseline.

## License

MIT

