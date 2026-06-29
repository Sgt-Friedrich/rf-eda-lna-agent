# Netlist Exploration Playbook

Netlist exploration is the cheapest way to test mechanisms, but it is also where
many false wins begin. The agent must keep netlist exploration bounded,
traceable, and separated from physical readiness.

## When To Use

Use netlist exploration for:

- mechanism smoke tests;
- variable-range discovery;
- topology screening before layout work;
- reproducing a reported candidate;
- building optimizer seeds;
- isolating whether a failure is circuit-level or layout/EM-level.

Do not use netlist-only evidence to claim layout or signoff readiness.

## Required Inputs

- project metric contract;
- seed candidate or baseline netlist;
- allowed variables and bounds;
- forbidden ideal elements or forbidden topology changes;
- simulator runner configured by the user;
- metric extraction rules.

## Netlist Harness Contract

Every netlist harness must write:

- generated netlist or patch file;
- command used to run the simulator;
- simulator log;
- extracted metric JSON;
- Markdown summary with pass/fail/provisional status;
- candidate record update.

## Exploration Modes

### Mechanism Smoke

Small, fast, and explicitly provisional. It may use simplified fixtures only if
the simplification is stated in the candidate record.

Promotion target: mechanism evidence only.

### Bounded Sweep

Tests a small physical or electrical window. Use it to map sensitivity and close
local neighborhoods.

Promotion target: candidate seed or branch retirement.

### Full Candidate Verify

Runs the configured analysis set against all hard gates. It should not contain
hidden ideal elements forbidden by the project.

Promotion target: schematic or physical schematic evidence, depending on model
fidelity.

## Common Pitfalls

- optimizing a single stage while ignoring cascade/system burden;
- using local component metrics instead of configured system metrics;
- using labels or net aliases that change electrical connectivity;
- accepting a pass with a missing hard metric;
- copying literature values without mapping them to available primitives;
- leaving ideal placeholders in a final netlist.

## Required Do-Not-Repeat Records

When a netlist branch fails, record whether the failure was:

- topology-level;
- fixture/boundary-level;
- variable-range-level;
- optimizer-objective-level;
- model-fidelity-level.

This prevents retiring a broad mechanism because a narrow fixture was wrong.
