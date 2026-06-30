# Optimizer Policy

The optimizer is a bounded evidence generator, not an authority.

## Required Inputs

Each optimizer run needs:

- seed candidate;
- allowed variables and bounds;
- quantization or physical implementation constraints when known;
- hard metric constraints from `config/metrics.yaml`;
- RF sanity gates selected from the active design claim;
- objective terms for all important tradeoffs;
- wall-time and iteration budgets;
- independent verification plan.

## Anti-Degeneracy Rules

Reject a candidate when:

- it passes one metric by sacrificing another hard metric;
- a configured metric is missing from the score;
- a relevant RF sanity gate is absent from the plan;
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

## EM-In-The-Loop Discipline

Live EM inside every optimizer iteration is often too expensive. The preferred pattern is:

1. generate a small set of physically meaningful EM variants;
2. freeze each validated EM artifact into the circuit harness;
3. optimize nearby schematic or layout variables against the frozen artifact;
4. quantize and resynchronize geometry;
5. rerun the EM/circuit verification at the active evidence level.

Do not return to an ideal or analytic primitive to claim final margin once a true EM artifact has exposed different phase, loss, or coupling behavior.

## Textbook-Derived Objective Discipline

- Cascade noise and gain must be scored together when the design contains
  multiple active stages.
- Matching, transducer gain, and stability must remain active when the optimizer
  changes source/load or interstage conditions.
- Physical line length, access metal, via return, and passive geometry should be
  variables or frozen EM artifacts; do not tune around them as invisible
  constants.
- Large-signal goals require separate nonlinear verification; small-signal
  optimizer rows cannot claim compression or intercept performance.

## Degenerate Result Rejection

Reject or demote a result when:

- a hard metric was not active in the objective or configured gate;
- the result improves one target by worsening an unconstrained hard gate;
- a required RF sanity gate is omitted;
- the pass depends on a narrow ripple, spike, or sampled-grid artifact;
- layout variables were not synchronized back to real geometry;
- the optimizer used a lower-fidelity model after higher-fidelity physical evidence showed a mismatch.

