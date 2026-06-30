# RF Passive And Layout Checklists

Use this reference when a candidate depends on physical passives, layout
interconnect, return paths, pads, vias, or bias/decoupling networks.

## Physical Passive Feasibility

For every passive that affects RF behavior, record:

- element type and whether it is ideal, PDK primitive, parameterized geometry,
  or EM-extracted layout;
- physical dimensions and whether they are realistic for the selected process;
- access lines, bends, crossings, vias, and ground return structures;
- expected parasitic mechanisms: loss, self-resonance, coupling, series
  inductance, shunt capacitance, and substrate return.

Reject final promotion if a metric-sensitive passive remains ideal without a
documented user waiver.

## Transmission Lines

Required checks:

- Preserve reference-plane consistency between schematic line, layout line, and
  EM port.
- Compare true physical length and electrical length; do not assume analytic
  and EM models agree at the same drawn length.
- Avoid arbitrary right-angle routing in RF-critical lines unless the process
  design style explicitly allows and verifies it.
- Quantize line geometry to layout-realizable values before final verification.

## Vias, Source Returns, And Grounding

Required checks:

- Treat source/emitter return and shunt-cap ground paths as RF elements, not
  bookkeeping nodes.
- Include via count, via spacing, strap width, and return path length in layout
  evidence.
- A pin-level ground name is insufficient; verify conductive geometry to the
  intended ground structure.
- When source degeneration or shunt return is central to a design, compare EM
  extracted return impedance against the schematic assumption.

## Capacitors, Resistors, And Bias Networks

Required checks:

- Model access metal and ground return for bypass and shunt capacitors.
- Separate high-frequency local bypass, midband stabilization, and low-frequency
  supply storage roles when the design uses multiple decoupling scales.
- Do not rely on a single ideal large capacitor as a millimeter-wave short.
- Treat long resistors, lossy damping elements, and bias feeds as layout items
  with length, noise, and parasitic consequences.

## Airbridges, Crossovers, Transformers, And Coupled Lines

Required checks:

- Verify crossings and coupled lines with the correct layer stack and return
  path.
- Record intended coupling direction and phase when a transformer or coupled
  line is used as a matching or feedback element.
- Do not replace a coupled structure with an independent scalar capacitor unless
  the branch is explicitly a mechanism test.

## Layout Growth Gate

Each block-growth step must produce:

- focused screenshot before and after the change;
- instance-pin mapping;
- conductive-shape/net coverage;
- unnetted-shape list or confirmation of zero unnetted conductors;
- local EM/cosim or a reason why the block is audit-only;
- exploration-tree update.

Do not grow the next block if the current block has visual open circuits,
unnetted RF metal, wrong layer transitions, or unresolved port/reference-plane
ambiguity.
