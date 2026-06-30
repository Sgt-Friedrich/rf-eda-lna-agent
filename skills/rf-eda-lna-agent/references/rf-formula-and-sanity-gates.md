# RF Formula And Sanity Gates

Use these checks before trusting optimizer, schematic, EM, or layout evidence.
The user configuration supplies the actual numeric targets.

## Cascade And Noise Budget

Required checks:

- Convert noise figure and gain to linear domain before cascade calculations.
- Score early stages by effective noise contribution and effective gain, not by
  noise figure alone.
- Record a predicted cascade metric for any stage-level candidate that will feed
  another active stage.
- Reject a candidate that looks low-noise only because the downstream burden is
  hidden or disconnected.

Harness implications:

- Optimizer objectives must include both noise and gain-related terms when the
  design is a cascade.
- Verification must recompute cascade estimates outside the optimizer.
- Exploration records must state what downstream reference was assumed.

## Matching And Gain Transfer

Required checks:

- Treat match, available gain, transducer gain, and noise match as coupled.
- Record whether a result is evaluated at source/load terminations, embedded
  ports, or de-embedded internal reference planes.
- Flag any passive network whose apparent reflection magnitude exceeds passive
  sanity expectations after embedding.
- When a matching network is physicalized, compare phase, insertion loss, and
  reference-plane position against the schematic model.

Harness implications:

- Fine-grid verification is mandatory after optimizer runs.
- EM-in-the-loop closure should optimize around frozen physical artifacts, not
  return to a lower-fidelity ideal primitive after physical mismatch appears.

## Stability

Required checks:

- Evaluate stability over the configured wide range, not only the operating
  band, whenever active devices are present.
- Treat near-unity stability margin as provisional unless the project explicitly
  accepts the margin.
- Reject low-noise or high-gain points created by narrow instability-adjacent
  peaks.
- Preserve the damping mechanism and its physical implementation in layout
  evidence.

Harness implications:

- Stability metrics are hard gates when configured.
- Optimizer score functions must keep stability active, even when the main
  objective is gain, noise, or match.

## Frequency Grid And Band Coverage

Required checks:

- Coarse-grid passes are not promotion evidence.
- Fine-grid verification must cover the configured band and any required
  out-of-band stability range.
- Touchstone files used for embedding must cover the required frequency range;
  extrapolated high-frequency behavior is a red flag.
- If DC behavior matters, the file or embedding model must provide a deliberate
  DC strategy.

Harness implications:

- `touchstone_audit.py` should run before embedding.
- Candidate records must state grid step, frequency coverage, and whether any
  extrapolation was used.

## Model-Fidelity Progression

Required checks:

- A lower-fidelity model cannot overrule a higher-fidelity failure without a
  control experiment.
- Ideal inductors, ideal chokes, and lossless transformers may be used only for
  short mechanism tests and must not appear in final delivery evidence unless
  the user explicitly changes the design contract.
- Physical primitive, EM block, hybrid EM/circuit, and signoff evidence are
  distinct levels.

Harness implications:

- The exploration tree must carry evidence level and model fidelity.
- Promotions must satisfy the active gate's evidence level, not merely the best
  schematic result.
