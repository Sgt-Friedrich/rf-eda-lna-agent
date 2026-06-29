# EM/Cosim Policy

EM/cosim is used to replace optimism with physical evidence. It must be run with explicit boundaries.

## Modes

### Replace-Mode

Use replace-mode only when:

- the block is passive;
- it does not carry required DC behavior that the circuit still needs;
- it does not remove an active-device noise reference;
- a known-good control embedding reproduces the anchor.

Additional replace-mode blockers:

- the conductor carries device DC bias that would be removed by a pure SnP;
- the cut severs a noise reference or source/ground return;
- the port plane includes extra geometry not present in the replaced primitive;
- the file lacks DC or full simulation-band coverage required by the harness;
- the block is part of a coupled structure that must be extracted together.

### Audit-Mode

Use audit-mode when:

- the PDK primitive remains the correct circuit model;
- EM is needed to inspect access metal, return geometry, coupling, or layout sanity;
- black-box replacement would create artificial bias/noise failures.

Audit mode still requires evidence: record the geometry inspected, screenshots or layout references, and why the model primitive remains the more truthful electrical representation.

### Hybrid Mode

Use hybrid EM/circuit mode when active/noise devices or model primitives must remain in the circuit while surrounding passive geometry is extracted.

Hybrid mode should define internal ports at model terminals, not arbitrary points inside bias or noise-critical paths. Port reference planes must match the block-level control harness or the comparison is ambiguous.

## Touchstone Gate

Before embedding:

- check port count;
- check frequency coverage;
- check DC handling when needed;
- document port order;
- document reference plane;
- run passive sanity checks.

If a passive S-parameter embedding produces impossible behavior such as a reflection magnitude above unity, treat it as a connection, reference, or embedding failure before considering RF tradeoffs.

## Full-Chip Passive EM Boundary

Full-chip passive EM is useful for coupling and metal loss, but it does not prove active/noise signoff by itself. Active devices and model-only passives must be reintroduced through a hybrid or partitioned circuit harness before promotion.

## Failure Handling

If embedding a near-ideal block causes a large circuit change, do not retune immediately. First check port mapping, reference plane, DC behavior, and whether replace-mode is valid.

