# Failure Catalog

Common failure modes the agent should detect and avoid.

## Optimizer Failures

- Coarse-grid overfit.
- Single-metric optimization sacrificing another hard metric.
- Ripple/flatness omitted from the score.
- Stability metric barely clears the target through a gain peak.
- Ideal schematic model gives margin that physical EM removes.
- Physical line length or phase frozen from an analytic model after EM changes the result.
- Final promotion from an unquantized optimizer row.
- Textbook sanity gate absent from the optimizer plan.

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
- A healthy-looking low-loss SnP causes a large circuit shift because the cut boundary is invalid.
- Reflection magnitude above unity appears after embedding a passive block.
- A full-cell EM attempt times out, but no partition plan is recorded.
- EM line, via, or return-path parasitic contradicts the schematic primitive but the optimizer continues tuning the wrong variable.

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
- GUI pCell artwork differs from headless database expectations.
- Stale layout windows keep locks or make the script edit the wrong cell.
- A reference layout style is read but not translated into a real block-growth plan.
- Physical passive geometry violates the role implied by the circuit model, such as an unrealizable choke, excessive resistor length, or missing local return path.

Response:

```text
stop layout growth, repair one connection, screenshot, rerun connectivity audit
```

## Signoff Failures

- No official DRC deck.
- No official LVS deck.
- No layer map or device-recognition map.
- GDS exports but layout has known connectivity blockers.
- Signoff-ready package is reported as signoff-clean.
- A missing deck is worked around with ad hoc geometry checks without labeling the blocker.

Response:

```text
report external blocker or readiness gap; do not claim clean
```
