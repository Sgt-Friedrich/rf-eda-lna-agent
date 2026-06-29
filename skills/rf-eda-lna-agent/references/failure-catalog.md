# Failure Catalog

Common failure modes the agent should detect and avoid.

## Optimizer Failures

- Coarse-grid overfit.
- Single-metric optimization sacrificing another hard metric.
- Ripple/flatness omitted from the score.
- Stability metric barely clears the target through a gain peak.
- Ideal schematic model gives margin that physical EM removes.

Response:

```text
reject candidate, add missing metric to score, fine-grid verify, restart from last non-degenerate seed
```

## EM/Cosim Failures

- S-parameter file lacks required frequency coverage.
- Missing DC handling on a bias-sensitive embedded block.
- Port order or reference plane differs from schematic.
- Black-box replacement removes a required bias or noise reference.
- Passive-only EM is mistaken for active/noise signoff.

Response:

```text
run control embedding, audit Touchstone, switch to audit-mode or hybrid mode when replacement is invalid
```

## Layout Failures

- Pin labels match but metal is not connected.
- Scaffold/reference polygons remain in final layout.
- Automatic routing creates non-RF geometry.
- Visual screenshot shows a gap that the script ignored.
- A component footprint exists but its access line or return path is wrong.

Response:

```text
stop layout growth, repair one connection, screenshot, rerun connectivity audit
```

## Signoff Failures

- No official DRC deck.
- No official LVS deck.
- No layer map or device-recognition map.
- GDS exports but layout has known connectivity blockers.

Response:

```text
report external blocker or readiness gap; do not claim clean
```

