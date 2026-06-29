# Harness Contracts

Harnesses are the agent's main execution units.

## Inventory Harness

Indexes docs, scripts, reports, results, and candidate IDs.

Requirements:

- configurable candidate regex
- local and remote repository support
- no automatic overwrite from remote
- heavy remote snapshots removed after inventory

Evidence products:

- inventory JSON and Markdown summary;
- candidate ID coverage;
- script-family histogram;
- largest-artifact summary.

## Simulation Harness

Runs user-configured analyses reproducibly.

Requirements:

- explicit seed
- generated or patched netlist stored as evidence
- structured metric JSON
- Markdown summary
- independent verification before promotion

A metric row without the input netlist, command, and log is not enough to debug a later regression.

## Optimizer Harness

Runs bounded optimizer rounds.

Requirements:

- variables with bounds, quantization, and physical meaning
- every hard metric represented in constraints or score
- wall-time and iteration budgets
- rejection of degenerate candidates
- final verification independent from optimizer grid

Reject raw optimizer rows until they are quantized, rerun outside the optimizer grid, and checked against every configured hard metric.

## Touchstone Audit Harness

Checks whether an S-parameter file is safe to embed.

Checks:

- expected port count
- required frequency coverage
- DC handling when needed
- port order and reference plane notes
- basic passive-network sanity
- verdict: embed_safe, audit_only, band_limited, dc_missing, port_uncertain, or reject

The Touchstone audit decides embedding eligibility; it does not prove the circuit will still meet system gates.

## EM/Cosim Harness

Rules:

- Replace-mode requires a control test.
- Audit-mode is valid when the PDK/model primitive remains the correct electrical model.
- Bias-carrying paths and noise-reference paths need special care.
- Passive-only EM is not active/noise signoff.

Every cut boundary should document port name, schematic node, physical reference plane, DC behavior, noise sensitivity, and what model remains outside the EM block.

## Layout Harness

Rules:

- grow one block or connection family at a time
- capture screenshots or equivalent visual proof
- verify conductive connectivity, not only labels
- avoid automatic routing that destroys RF intent

Growth products include pre/post screenshots, geometry net-coverage report, focused cosim when meaningful, and rollback notes for rejected blocks.

## Signoff Harness

Rules:

- signoff-clean requires official reports
- missing DRC/LVS collateral is an external blocker
- signoff-ready is not signoff-clean

If decks are absent, the harness may produce a signoff-ready package, but the state must remain blocked or ready-for-official-deck, never clean.
