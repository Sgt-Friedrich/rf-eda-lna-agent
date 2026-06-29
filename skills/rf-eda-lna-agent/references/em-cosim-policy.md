# EM/Cosim Policy

EM/cosim is used to replace optimism with physical evidence. It must be run with explicit boundaries.

## Modes

### Replace-Mode

Use replace-mode only when:

- the block is passive;
- it does not carry required DC behavior that the circuit still needs;
- it does not remove an active-device noise reference;
- a known-good control embedding reproduces the anchor.

### Audit-Mode

Use audit-mode when:

- the PDK primitive remains the correct circuit model;
- EM is needed to inspect access metal, return geometry, coupling, or layout sanity;
- black-box replacement would create artificial bias/noise failures.

### Hybrid Mode

Use hybrid EM/circuit mode when active/noise devices or model primitives must remain in the circuit while surrounding passive geometry is extracted.

## Touchstone Gate

Before embedding:

- check port count;
- check frequency coverage;
- check DC handling when needed;
- document port order;
- document reference plane;
- run passive sanity checks.

## Failure Handling

If embedding a near-ideal block causes a large circuit change, do not retune immediately. First check port mapping, reference plane, DC behavior, and whether replace-mode is valid.

