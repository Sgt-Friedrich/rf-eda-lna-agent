# Do-Not-Repeat Patterns

This file distills long exploration histories into reusable negative rules. It
does not preserve private candidate IDs or project-specific numbers. It records
the patterns an agent should avoid repeating unless the user explicitly changes
the design contract.

## Exploration Discipline

- Do not launch blind full-chain optimizers before device/system budgets,
  mechanism probes, and physicalization evidence exist.
- Do not treat a bare device or primitive data row as a circuit candidate.
- Do not use an ideal mechanism probe as promotion evidence.
- Do not continue scalar tuning after repeated failures show a mechanism or
  boundary problem.
- Do not retire an entire architecture from one bad fixture; retire the exact
  fixture or mechanism family that evidence supports.

## Cascade And System Budget

- Do not rank early-stage candidates by local noise or gain alone when the
  system budget depends on cascade behavior.
- Do not attach a noisy or mismatched downstream stage and hope later gain fixes
  the upstream budget.
- Do not connect the next stage until the current block meets its configured
  match, gain/noise, and stability prerequisites.

## Optimizer Traps

- Do not promote a coarse-grid pass before fine-grid verification.
- Do not optimize one hard metric while leaving another hard metric out of the
  score.
- Do not accept narrow gain peaks, flatness collapse, or stability razor-edge
  points as real margin.
- Do not continue the same small passive tweak family after multiple bounded
  attempts show near-zero leverage.
- Do not promote unquantized optimizer values or values not synchronized to
  physical layout geometry.

## Physicalization Traps

- Do not convert an ideal line/capacitor/inductor mechanism directly into final
  evidence without physical access lines, returns, losses, and model semantics.
- Do not keep optimizing analytic line lengths after true EM shows phase or loss
  mismatch.
- Do not call a schematic layout-ready if bias, decoupling, or source/ground
  return paths are still ideal placeholders forbidden by the project.
- Do not use a final circuit element that the user has explicitly banned.

## EM/Cosim Traps

- Do not black-box replace a path that carries device DC, noise reference, or
  source/ground return semantics unless a control harness proves equivalence.
- Do not cut through a coupled structure and then interpret the broken result as
  circuit physics.
- Do not embed a Touchstone file with insufficient frequency coverage or missing
  DC behavior when the circuit needs it.
- Do not retune immediately after an embedding causes an impossible or huge
  shift; first audit ports, reference planes, DC, and boundary validity.
- Do not claim passive-only full-chip EM proves active/noise signoff.

## Layout Traps

- Do not build the whole RF layout with all-net autorouting and then debug every
  connection at once.
- Do not claim layout connectivity from pin-net equality while conductive shapes
  remain floating.
- Do not keep scaffold or reference polygons in the final layout unless they are
  converted into real circuit metal.
- Do not skip screenshots when the user or gate requires visual review.
- Do not ignore pCell artwork, GUI locks, or stale windows as if they were
  cosmetic.

## Signoff Traps

- Do not claim DRC/LVS clean without official decks and reports.
- Do not treat GDS export as physical verification.
- Do not hide missing foundry or PDK collateral behind local ad hoc checks.
- Do not delete heavy evidence before writing manifests for the active gate.

## How To Use

When a branch fails, convert the specific lesson into one of these generic
patterns plus a project-specific do-not-repeat record in the exploration tree.
The public agent keeps the generic pattern; the private project keeps the
specific evidence.
