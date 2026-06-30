# RF ADS/CAD Workflow Map

Use this reference when adapting the skill to an EDA environment such as ADS or
another RF CAD tool. Keep tool paths, PDK names, library names, and cell names in
project config, not in the public skill.

## EDA Adapter Layers

| Layer | Responsibility | Evidence |
|---|---|---|
| Config | tool executable, workspace, library/cell names, user metrics | config files |
| Database builder | schematic/layout creation or patching | generated script, openable cell |
| Simulator runner | SP, noise, stability, HB, EM, or cosim invocation | raw log, dataset path |
| Extractor | convert dataset to metric JSON | metrics JSON, plots if needed |
| Gate | compare metrics with user targets | pass/fail/provisional JSON |
| Recorder | update goal, exploration tree, manifests | Markdown/JSONL records |

## Schematic Generation

Required rules:

- Prefer explicit wire-to-wire connectivity over hidden labels for critical
  nodes.
- Reserve hidden labels for deliberate internal nets, and document them.
- Keep instance parameters in a structured design spec.
- After generation, open or validate the cell with the EDA database runtime.
- Store an acceptance artifact that names the cell and confirms connectivity.

## Optimizer Invocation

Required rules:

- Native optimizer use is valid when hard gates and variable bounds are
  explicit.
- Keep every hard target in the objective or in a mandatory rejection gate.
- Save optimizer plan, iteration summary, best row, rejected rows, and
  independent verification.
- Separate coarse search from fine verification.
- Do not synchronize optimizer values to layout until the result survives the
  configured verification level.

## EM/Cosim

Required rules:

- Extract one block or one clearly defined partition at a time unless the
  project is explicitly in full-chip hybrid verification.
- Define port count, port order, reference planes, ground reference, frequency
  range, and DC/noise strategy before solving.
- Run a control embedding when using a new SnP replacement pattern.
- Use audit-mode when black-box replacement would break DC, noise, or
  high-impedance coupled semantics.

## GUI And Screenshot Review

Required rules:

- Use GUI review when geometry, pCell artwork, visual connectivity, or window
  state matters.
- Keep window count controlled; close obsolete layout/schematic windows.
- Capture focused screenshots per block and a full-chip overview at milestones.
- Do not claim visual connectivity from script intent alone.

## Signoff Readiness

Required rules:

- Distinguish ready-for-DRC/LVS from DRC/LVS-clean.
- Official decks and reports are required for clean claims.
- Missing decks are external blockers, not engineering passes.
- GDS export is delivery evidence, not proof of LVS or DRC.
