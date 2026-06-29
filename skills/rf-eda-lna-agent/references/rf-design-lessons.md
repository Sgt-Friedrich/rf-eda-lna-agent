# RF Design Lessons

This skill is target-agnostic. It should not ship fixed RF targets, a fixed
process, or a fixed topology. It should preserve reusable design reasoning that
an agent can apply after the user supplies a design contract.

## System Budget Before Local Optimum

A low-noise or high-gain local result can be useless if it fails the system
budget. For cascaded RF blocks, score early-stage candidates with the user's
configured cascade or system equation, not with a single local metric alone.

For noise-sensitive designs, keep the standard linear-domain cascade relation
available in the report/harness layer, but let the user configure which stages
and metrics matter.

## Mechanism Lane Versus Candidate Lane

Separate two lanes:

- mechanism lane: simplified experiments that prove a physical mechanism can
  work;
- candidate lane: full evidence path with physical primitives, bias/return
  networks, EM checks, layout checks, and signoff gates.

A mechanism result cannot be promoted as a final candidate unless it is rebuilt
under the candidate-lane evidence gates.

## Literature Adaptation

Do not copy a paper topology literally into another PDK or process. Map the
mechanism into:

- available active devices;
- physical passive primitives;
- bias and return constraints;
- manufacturable layout geometry;
- optimizer variables with physical bounds.

Negative results from an exact fixture do not necessarily retire the mechanism.
Retire a branch only after the failure mode is classified.

## Objective Discipline

All hard metrics must remain active in optimizer goals or rejection checks.
Typical degenerate patterns:

- improving one metric by sacrificing an unconstrained hard metric;
- creating a narrow gain peak that passes sampled points;
- reporting a pass on a coarse grid that fails fine verification;
- using an ideal or analytic model to claim physical margin;
- moving a layout variable without syncing the actual geometry.

## Physical Readiness

A design is not physically ready only because schematic metrics pass. The agent
must check:

- bias and decoupling are modeled as physical networks or explicitly audit-mode;
- no final circuit element is an ideal placeholder forbidden by the user;
- source/ground returns are physical;
- line lengths, widths, capacitor dimensions, and access lines are tied to
  manufacturable geometry;
- every EM replacement has a control experiment or a clear audit-mode reason.
