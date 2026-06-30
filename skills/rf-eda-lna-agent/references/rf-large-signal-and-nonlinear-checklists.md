# RF Large-Signal And Nonlinear Checklists

Use this reference when a design claim includes compression, intermodulation,
large-signal drive, mixer-like behavior, or nonlinear stability.

## Large-Signal Boundary

Small-signal pass does not imply large-signal pass. Before delivery, record:

- selected nonlinear device model and bias condition;
- drive level sweep range;
- harmonic balance or equivalent nonlinear analysis setup;
- input/output power reference planes;
- convergence settings and any failed points;
- extracted compression and intermodulation metrics configured by the user.

## P1dB / Compression

Required checks:

- Use the same embedding/physical evidence level as the promoted small-signal
  candidate when practical.
- Report whether compression is input-referred or output-referred.
- Verify that gain used for compression is the same gain definition used by the
  project contract.
- Do not reuse schematic-only compression evidence after EM has materially
  changed gain or match.

## IIP3 / OIP3

Required checks:

- Record tone spacing, tone locations, power sweep, and extrapolation method.
- Check that the fundamental and intermodulation products are measured at the
  intended ports.
- Reject a result if the device is near convergence failure or the slope region
  is not linear enough for the reported intercept.

## Nonlinear Stability And Multiple-Device Effects

Required checks:

- Damping or feedback added for small-signal stability must remain present in
  large-signal verification.
- Multiple-device, stacked, balanced, or reuse structures require branch current
  and bias sanity checks.
- If the design uses feedback or coupled paths, record whether large-signal
  phase/amplitude behavior remains bounded.

## Harness Implications

- Provide a large-signal harness family separate from small-signal optimizer
  sweeps.
- Store raw sweep data and extracted metric JSON.
- Keep large-signal evidence tied to candidate ID and evidence level.
- If large-signal simulation is blocked by model availability or tool
  convergence, report a blocker with the smallest unlock action.
