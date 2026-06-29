# Optimizer Policy

The optimizer is a bounded evidence generator, not an authority.

## Required Inputs

Each optimizer run needs:

- seed candidate;
- allowed variables and bounds;
- quantization or physical implementation constraints when known;
- hard metric constraints from `config/metrics.yaml`;
- objective terms for all important tradeoffs;
- wall-time and iteration budgets;
- independent verification plan.

## Anti-Degeneracy Rules

Reject a candidate when:

- it passes one metric by sacrificing another hard metric;
- a configured metric is missing from the score;
- a coarse-grid pass fails independent verification;
- a stability-related metric barely clears the target through a narrow peak;
- an ideal model result is not reproducible with the required physical evidence level.

## Verification

After optimization:

1. rerun the candidate outside the optimizer loop;
2. verify on the configured honest grid/range;
3. write metric JSON and Markdown summary;
4. update the exploration tree with pass/fail/provisional status.

## Retuning Boundary

Retuning is valid only when it stays within the branch's allowed variables. If the only path requires forbidden topology or model changes, stop and report a blocked decision.

