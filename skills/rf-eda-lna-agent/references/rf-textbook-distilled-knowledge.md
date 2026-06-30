# RF Textbook Distilled Knowledge

This file distills RF/microwave textbook material into reusable agent behavior.
It does not copy textbook body text, derivations, tables, or figures. Use it as
an engineering checklist when constructing RF/EDA harnesses.

## Source Extraction Status

| Source | Extraction status | Usable signals |
|---|---|---|
| Microwave engineering network text | extracted | transmission line theory, Smith chart, scattering matrix, ABCD, matching, resonators, couplers, filters, noise/nonlinear distortion |
| Microwave circuit design text | extracted | lumped/distributed transition, active devices, two-port stability, LNA examples, noise parameters, cascaded noise, broadband and multistage amplifiers |
| Nonlinear microwave/RF circuits text | extracted | nonlinear device models, large-signal S-parameters, harmonic balance, multitone intermodulation, Volterra/power series, small-signal amplifier nonlinearities |
| RF/microwave lumped elements text | extracted | inductors, capacitors, resistors, vias, airbridges, transformers, matching networks, biasing networks, fabrication and microstrip overview |
| RF microelectronics text | extracted | RF nonlinearity/noise basics, matching loss, S-parameters, LNA input matching/topologies, passive devices, transmission lines |
| CMOS RFIC design text | needs repair/OCR | current PDF cannot be rendered or text-extracted; do not use until a readable source is provided |
| ADS microwave CAD text | needs repair/OCR | current PDF cannot be rendered or text-extracted; do not use until a readable source is provided |
| microwave transistor amplifier solutions/excerpt | manual review required | renderable, but sampled pages expose solution material and chapter numbers rather than usable chapter titles; do not infer lessons without the actual readable text |

## Distilled Agent Knowledge

### Transmission Lines And Reference Planes

Textbook signals: transmission-line circuit models, terminated lines, Smith
chart, lossy lines, microstrip, stripline, ABCD matrices, scattering matrices,
quarter-wave and multisection transformers.

Agent rules:

- Never treat a physical line length as equivalent to an analytic line length
  after EM has shown different phase or loss.
- Record reference-plane location for every port in schematic, EM, and
  embedded circuit representations.
- Use ABCD/cascade reasoning for interconnect chains, but verify with S
  parameters when loss, dispersion, coupling, or discontinuities are relevant.
- For broadband matching, prefer explicit bandwidth-aware structures and
  fine-grid verification over single-frequency match wins.
- Add a red flag when a matching result depends on an unverified stub, short
  line, or transformer that has not been checked as physical geometry.

Harness implications:

- EM plans must include port order, port planes, substrate/profile reference,
  frequency coverage, and whether de-embedding is applied.
- Optimizer plans must include physical variables for metric-critical line
  length/width when a true EM line replaces an analytic primitive.

### Two-Port Stability, Gain, And Matching

Textbook signals: two-port S parameters, stability, power gains, transducer
gain, low-noise/high-power amplifier examples, LNA design examples.

Agent rules:

- Separate available gain, transducer gain, insertion gain, and stage gain in
  candidate records.
- Do not promote a design that passes gain but omits configured input/output
  match or stability checks.
- Treat stability over the configured wide range as a different claim from
  in-band small-signal performance.
- A low-noise point with weak effective gain must be scored against downstream
  noise burden before being considered a useful front-end candidate.

Harness implications:

- Candidate metric JSON should include the gain definition used.
- Optimizer objectives must keep match, stability, gain, and noise active when
  they are configured hard gates.

### Noise Parameters And Cascade Budget

Textbook signals: noise figure measurements, noise parameters, noise
correlation matrices, cascaded networks, noise circles, FET noise models,
external parasitic influence, LNA input matching problem.

Agent rules:

- Convert dB noise figure and gain to linear domain for cascade reasoning.
- Record whether a stage is optimized for minimum noise, source match,
  transducer gain, or a weighted system objective.
- A matching network loss before the first active device directly degrades
  input-referred noise; treat that loss as a hard audit item.
- Source return, gate access, bias feed, and shunt capacitor ground paths are
  noise-relevant physical elements.
- If a stage-level candidate will drive another stage, compute a predicted
  downstream noise burden or mark the evidence incomplete.

Harness implications:

- Stage-only harnesses need a downstream reference assumption.
- EM/cosim harnesses must not black-box replace a noise-critical path without a
  control experiment.

### Passive Elements, Vias, And Layout

Textbook signals: lumped-element modeling, printed inductors on different
substrates, MIM capacitor models, resistor noise/stability, via-hole models,
via fences, airbridges, transformers/baluns, passive matching and biasing
circuits.

Agent rules:

- Physical passives are geometry plus access plus return path, not only a
  scalar value.
- Large ideal inductors or chokes are mechanism placeholders only unless the
  selected process has a verified physical implementation.
- Capacitors require access-line and ground-return modeling when they affect RF
  match, noise, or stability.
- Vias and backside/source returns can dominate apparently small RF paths; do
  not trust pin-ground names without geometry evidence.
- Long resistors and damping networks must be checked for area, parasitic
  capacitance, noise, and RF placement.
- Airbridges/crossovers/transformers require layer and coupling intent checks,
  not only netlist equivalence.

Harness implications:

- Layout growth must include screenshots plus conductive-geometry audit.
- EM partitions should isolate the passive element and its real access/return
  path, not an artificial scalar component boundary.

### Nonlinear And Large-Signal Behavior

Textbook signals: nonlinear device models, nonlinear lumped elements,
large-signal S-parameters, harmonic balance, multitone excitation,
intermodulation, Volterra/power-series analysis, small-signal amplifier
nonlinearities, power-amplifier HB analysis.

Agent rules:

- Small-signal pass is not delivery evidence for compression or intercept
  claims.
- Record tone spacing, drive level, harmonics, and reference planes for every
  large-signal result.
- Reject IIP3/OIP3 results that do not show a valid slope region or depend on
  convergence artifacts.
- Preserve the same physical/cosim evidence level for large-signal checks when
  layout parasitics materially changed small-signal metrics.

Harness implications:

- Provide separate HB/large-signal harnesses and attach their results to the
  same candidate ID.
- If nonlinear model availability blocks the test, report a model/tool blocker
  rather than claiming large-signal readiness.

### CAD/ADS Workflow Discipline

Textbook signals: modern CAD for nonlinear circuit analysis, exact designs and
CAD tools, harmonic-balance simulation, ADS-oriented workflow source pending
repair/OCR.

Agent rules:

- CAD output is evidence only with its setup, raw log, extracted metric JSON,
  and independent verification.
- Native optimizers are acceptable when hard gates, variables, bounds, and
  verification grids are explicit.
- GUI work is valid evidence for visual/layout questions but must produce
  screenshots and avoid uncontrolled window state.
- Missing official decks, model files, or broken PDF/tool collateral are
  blockers; do not infer unavailable evidence.

Harness implications:

- Every EDA adapter must have dry-run validation and a project-specific hook.
- Heavy solver data belongs in artifact manifests or external storage unless a
  project policy explicitly allows it.

## Mapping From Historical Failures To Textbook Checks

| Historical pattern | Textbook-derived check | Agent response |
|---|---|---|
| coarse optimizer grid hides ripple | broadband matching and frequency coverage | fine-grid verify before promotion |
| single metric optimized while another hard gate collapses | multi-objective gain/noise/match/stability coupling | reject degenerate result and add missing hard gate |
| analytic line works but EM line loses gain or shifts phase | transmission-line loss and reference-plane consistency | optimize true physical line variables in EM loop |
| SnP replacement breaks a bias or noise-sensitive path | two-port boundary and noise reference semantics | require control embedding; switch to audit/hybrid mode if invalid |
| pin names match but metal is open | via/airbridge/geometry continuity | require conductive-shape audit and screenshot review |
| passive full-chip EM reported as active/noise signoff | model partition and active noise requirements | require hybrid EM/circuit embedding |
| missing DRC/LVS decks treated as clean | signoff collateral boundary | report external blocker, not pass |
