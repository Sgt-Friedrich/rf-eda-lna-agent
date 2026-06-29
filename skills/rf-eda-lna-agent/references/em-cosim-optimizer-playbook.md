# EM/Cosim Optimizer Playbook

The most robust flow is not "optimize ideal schematic, then hope layout works."
It is a closed loop between physical geometry, EM evidence, and circuit
optimization.

## Recommended Loop

1. Select a physically meaningful block or variable family.
2. Generate a small set of manufacturable geometry variants.
3. EM-extract each variant with documented ports and reference planes.
4. Audit each Touchstone file.
5. Embed eligible artifacts into the circuit harness.
6. Optimize nearby schematic/layout variables with EM artifacts frozen.
7. Quantize the result and sync geometry.
8. Rerun independent SP/noise/stability/linearity checks configured by the user.
9. Record the result and failure modes.

## What Should Be Optimized

Optimizer variables should correspond to physical or circuit degrees of freedom:

- line length, width, taper, access length;
- capacitor side length or selectable model value;
- resistor geometry or selectable model value;
- bias values inside user-approved limits;
- damping/stabilization values inside user-approved limits.

The optimizer should not invent hidden ideal elements or silently remove physical
constraints.

## Hard-Gate Handling

All configured hard gates must be active during scoring or rejection. If a metric
is expensive to compute in-loop, run it as a mandatory post-check and demote any
candidate that fails it.

## Control Experiments

Before trusting a new EM/cosim method:

- embed a known-good equivalent artifact;
- compare against the anchor;
- permute or audit ports only if the failure signature suggests port mapping;
- verify frequency coverage and DC behavior;
- confirm the same harness can reproduce a known state before retuning.

## Failure Interpretation

- Low-loss EM block causes huge circuit shift: suspect boundary, DC, reference
  plane, or missing model semantics.
- EM line has correct loss but wrong circuit response: check phase/reference
  plane and geometry synchronization.
- Optimizer improves metric but destroys ripple or stability: reject as
  degeneration.
- Full-cell EM is too large: partition by honest electrical boundaries and keep
  a manifest of what coupling is not yet covered.
