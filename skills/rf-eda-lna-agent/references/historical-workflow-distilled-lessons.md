# Historical Workflow Distilled Lessons

This reference distills a large private RF/EDA project history into generic
agent behavior. It does not publish private scripts, circuit data, layouts,
tool paths, PDK names, candidate IDs, or measured targets.

## Sanitized Inventory Shape

A local legacy scan classified thousands of script and document artifacts into
these reusable harness families:

| Harness family | Relative weight | What it means for the skill |
|---|---:|---|
| process/artifact guard | high | long EDA runs need size budgets, manifests, cleanup policy, and process hygiene |
| layout GUI/growth | high | RF layout work cannot be reduced to net names; visual and database connectivity gates are required |
| EM/cosim | high | physical evidence dominates late-stage RF closure; port and model partition discipline is central |
| netlist/schematic generation | medium | schematic/database generation needs explicit connectivity and acceptance artifacts |
| optimizer/sweep | medium | optimizers need hard-gate objectives, verification, and degenerate-result rejection |
| audit/diagnostic | medium | small diagnostic fixtures save time before broad retuning |
| large-signal | smaller but required | nonlinear metrics need their own harness after small-signal closure |
| signoff | smaller but decisive | DRC/LVS clean claims are external-collateral dependent |

The conclusion is structural: a useful RF EDA agent must be a workflow system,
not just a simulator wrapper.

## Script Family Lessons

### Netlist And Schematic Generation

Lessons:

- Explicit wire connectivity is safer than label-only connectivity for RF and
  bias-critical nodes.
- Generated schematics need an acceptance artifact: instance list, named nodes,
  dangling-wire check, netlist generation result, and screenshot when GUI review
  is part of the gate.
- Ground naming must be simulator-compatible and project-configured.
- Bias, decoupling, source return, and simulation setup should remain visible
  in the schematic; hiding them weakens review and later layout handoff.

Skill response:

- Keep schematic generation as a dedicated harness family.
- Require `schematic_design_spec` plus `eda_config`.
- Treat screenshot evidence and netlist evidence as separate gates.

### Optimizer And Sweep

Lessons:

- Optimizers repeatedly find degenerate points when a hard gate is missing from
  the objective.
- Coarse-grid wins can disappear on fine-grid verification.
- A low-noise or high-gain point near instability is a red flag, not a win.
- Physical line phase, passive access, via return, and model fidelity must be in
  the variable set or frozen as verified EM artifacts.

Skill response:

- Require hard targets, RF sanity gates, physical meaning, bounds, and
  independent verification in optimizer plans.
- Add `degeneracy_checks` to candidate evidence.
- Reject promotion when sanity gates are omitted.

### EM/Cosim

Lessons:

- Standalone low-loss S-parameters are not enough; embedding can fail because
  the cut boundary breaks DC, noise reference, high-impedance coupling, or port
  reference-plane semantics.
- Replace-mode is safe only after a control embedding reproduces the anchor.
- Audit-mode is often the correct answer for model-owned passives or
  noise-critical structures.
- Hybrid EM/circuit is required when active/noise models must remain in circuit
  while passive geometry is extracted.

Skill response:

- Treat Touchstone audit, control embedding, mode selection, and model
  partition as separate steps.
- Require frequency coverage and deliberate DC/noise strategy.
- Never retune immediately after a suspicious embed shift; diagnose boundary
  validity first.

### Layout GUI And Growth

Lessons:

- Pin-net equality is not physical metal connectivity.
- Full-netlist auto-routing produces unusable RF floorplans.
- Stale GUI windows, locks, and pCell callback differences can make scripts
  edit or inspect the wrong object.
- Each physical block should be placed, connected, screenshot-reviewed, and
  locally audited before the next block is added.

Skill response:

- Enforce block-growth protocol: one block/connection family at a time.
- Require screenshots plus conductive-shape/net coverage.
- Keep GUI review as a valid harness, not an afterthought.
- Close or control windows before editing.

### Process And Artifact Guard

Lessons:

- EM and EDA workspaces grow quickly; uncontrolled solver data can exceed local
  budgets and pollute Git.
- Evidence can be destroyed by cleanup if manifests are not written first.
- Remote/GitHub history may contain decisions absent from the current worktree.

Skill response:

- Use artifact budgets and manifests.
- Keep heavy solver/layout data out of public Git by default.
- Audit local and remote history before claiming a branch is new or exhausted.

### Large-Signal And Signoff

Lessons:

- Small-signal pass is not evidence for compression or intermodulation.
- GDS export is not DRC/LVS clean.
- Missing official decks are external blockers, not engineering passes.

Skill response:

- Keep large-signal harness separate from SP/NF/stability harnesses.
- Require official signoff collateral before clean claims.
- Report smallest unlock action for blockers.

## Migration Pattern

When converting private history into the public skill:

1. inventory the private tree;
2. classify scripts/docs into harness families;
3. extract interfaces, evidence products, gates, and failure responses;
4. rewrite as parameterized templates and references;
5. discard private paths, metrics, circuit names, screenshots, raw solver data,
   and PDK-specific content;
6. test with synthetic projects only.

## Do-Not-Repeat Patterns

- Do not summarize a long RF project from the latest result alone.
- Do not promote optimizer output without independent verification.
- Do not switch from physical evidence back to an ideal model to claim margin.
- Do not treat a black-box S-parameter replacement as harmless by default.
- Do not let GUI screenshots substitute for netlist/geometry checks, or vice
  versa.
- Do not claim signoff without official reports.
