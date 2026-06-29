# Schematic Generation Playbook

Generated schematics must be reviewable engineering drawings, not just netlist
containers. A reviewer should be able to trace RF, DC, bias, return, and
simulation setup directly from the schematic.

## Runtime Rule

Use the EDA vendor runtime for database edits. System Python or generic scripts
may prepare data, but database creation, symbol placement, and pCell work should
run through the configured EDA adapter.

## Drawing Rules

- Place real components with recorded library/cell names.
- Connect pins with real wires or explicit metal/database connections.
- Do not use terminal labels as invisible jumpers.
- Use hidden wire labels only after the physical wire exists.
- Keep ground naming consistent with the simulator.
- Keep parameters visible near the related device.
- Draw bias and decoupling networks explicitly.
- Keep simulation controllers and equations visible for review.

## Acceptance Checks

Run these before declaring a schematic ready:

- required instance list present;
- required probes or named nodes present;
- no dangling wire endpoints;
- no unintended same-node shorts on multi-terminal devices;
- no hidden label-only connections unless explicitly allowed;
- no forbidden ideal elements in final candidates;
- netlist generation succeeds;
- GUI screenshot or review artifact exists when requested.

## Schematic Evidence Bundle

Each generated schematic should produce:

- cell identifier;
- generator script and command;
- netlist path or netlist manifest;
- audit JSON;
- screenshots if GUI review is part of the gate;
- known limitations;
- next required evidence level.

## Common Failures

| Failure | Meaning | Response |
|---|---|---|
| schematic looks wired but netlist differs | label or terminal API changed connectivity | switch to explicit wire connections and audit netlist |
| bias network hidden behind net labels | reviewer cannot verify physical intent | draw bias/feed/decap blocks explicitly |
| generated pCell differs in GUI | headless callback/artwork mismatch | refresh in GUI and capture evidence |
| many stale windows lock cells | GUI state is uncontrolled | close stale windows and open one target cell |
