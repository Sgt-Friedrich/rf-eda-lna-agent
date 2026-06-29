# Configuration Schema

The agent is project-configured. It must not ship RF targets, EDA paths, PDK paths, library names, or candidate IDs as defaults.

## Required Files

```text
config/project.yaml
config/metrics.yaml
config/artifact_policy.yaml
goal.md
docs/exploration_tree.md
```

## Project Config

`config/project.yaml` records project identity, EDA entrypoints, process profile names, and workflow constraints.

Required concepts:

- project name and privacy level
- workspace root as a user-provided path or environment reference
- candidate prefix and candidate regex
- EDA tool family and commands
- PDK/profile name and signoff collateral paths when applicable
- GUI permission and GitHub repository preference

## Metrics Config

`config/metrics.yaml` is the only source of design targets.

Required concepts:

- analyses and operating range
- hard targets with metric, operator, value, unit, aggregation, and evidence level
- stretch targets
- report-only metrics

The skill must ask the user for missing hard targets before running expensive experiments.

## Artifact Policy

`config/artifact_policy.yaml` controls retention and size budgets.

Required concepts:

- repository size budget
- per-run temporary budget
- which artifact classes to keep
- whether remote snapshots and raw solver directories are retained
- delete-only-inside-workspace safety rule

## Candidate Record

Each candidate should be representable as:

```yaml
id: CANDIDATE_ID
parent: PARENT_ID
branch: branch_name
hypothesis: short claim
seed: seed ID or artifact
changed_variables: []
forbidden_changes: []
evidence_level: E0
metrics: {}
artifacts: []
decision: promote|retire|blocked|continue|provisional
do_not_repeat: []
next_action: short action
```

