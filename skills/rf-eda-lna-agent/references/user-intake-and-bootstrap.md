# User Intake And Bootstrap

The agent starts by collecting a design contract. It must not use target values from any prior project.

## Minimal Questions

Ask the user:

```text
1. What circuit/application and operating range should this project target?
2. Which metrics are hard pass/fail requirements, and which are stretch or report-only?
3. Which EDA tool, PDK/profile, workspace, and GitHub repository should the agent use or create?
4. What artifact-size budget and GUI policy should the agent follow?
```

## Project Files

After intake, create:

```text
config/project.yaml
config/metrics.yaml
config/artifact_policy.yaml
goal.md
docs/exploration_tree.md
docs/decision_log.md
docs/failure_catalog.md
manifests/artifact_manifest.json
```

## Metrics Schema

```yaml
analyses:
  - name: USER_ANALYSIS_NAME
    type: small_signal|noise|large_signal|em|layout|signoff|custom
    range:
      start: USER_VALUE_OR_TBD
      stop: USER_VALUE_OR_TBD
      unit: USER_UNIT_OR_TBD

hard_targets:
  - metric: USER_METRIC_NAME
    analysis: USER_ANALYSIS_NAME
    operator: USER_OPERATOR
    value: USER_VALUE
    unit: USER_UNIT
    aggregation: min|max|avg|worst|point|custom
    evidence_required: EVIDENCE_LEVEL

stretch_targets: []
report_only: []
```

## Initial Goal Template

```markdown
# Goal

## Design Contract

- circuit/application: USER_TEXT
- analyses: see `config/metrics.yaml`
- hard targets: see `config/metrics.yaml`
- stretch targets: see `config/metrics.yaml`
- deliverables: USER_TEXT

## Rules

- User hard targets cannot be changed without user approval.
- No result is promoted unless it reaches the required evidence level.
- No signoff-clean claim without required official reports.
- Heavy artifacts are governed by `config/artifact_policy.yaml`.
- Every candidate must update `docs/exploration_tree.md`.

## Current State

- latest candidate: none
- evidence level: E0
- blocker: none
- next action: build baseline harness
```

## GitHub Setup

When GitHub maintenance is requested:

1. Create or connect the repository.
2. Commit config, goal, and docs scaffolding first.
3. Use lightweight commits for candidate summaries and manifests.
4. Keep heavy artifacts out of Git unless the user configures a large-file strategy.

