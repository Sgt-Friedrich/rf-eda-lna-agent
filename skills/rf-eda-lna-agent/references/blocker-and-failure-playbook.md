# Blocker And Failure Playbook

This playbook tells the agent when to continue, when to repair, and when to stop
truthfully. A blocker is not a failure of effort; it is a gate that cannot be
passed without a specific missing action, tool, artifact, or user decision.

## Blocker Record

Every blocker report must include:

- gate name;
- failed hard requirement;
- exact evidence path or command output;
- why workaround is unsafe;
- smallest unlock action;
- whether the blocker is internal, external, or user-decision gated.

## Hard Red Flags

| Red flag | Meaning | Required response |
|---|---|---|
| Reflection magnitude above unity in a passive embedding | connection, reference, or embedding error | stop and audit ports/reference/connectivity |
| Stability appears to pass only through a narrow gain spike | optimizer degeneration | reject and restore flatness/stability goals |
| A healthy standalone SnP breaks the circuit | invalid cut boundary or missing DC/noise semantics | run control embedding, switch to audit-mode if needed |
| Fine sweep fails after coarse pass | grid overfit | demote candidate and fine-grid optimize/verify |
| Pin-level net names match but metal is unnetted | layout intent is not conductive connectivity | repair physical metal, screenshot, rerun geometry audit |
| Full passive EM passes but active/noise sim fails or is unrun | wrong evidence level | build hybrid EM/circuit or document limitation |
| DRC/LVS deck missing | external signoff collateral missing | report external blocker; do not claim clean |

## Stop Conditions

Stop and report instead of improvising when:

- a configured hard gate fails for two bounded repair attempts without trend;
- the only apparent fix violates a user topology or artifact constraint;
- official signoff collateral is absent;
- tool execution is blocked by a license/runtime/database lock that cannot be
  safely cleared;
- repository or artifact size would exceed the configured budget;
- a GUI operation would modify a frozen or unrelated cell.

## Do-Not-Repeat Rules

When retiring a branch, write a do-not-repeat rule specific enough to prevent
waste, but not so broad that it incorrectly kills a mechanism. Good examples:

- "Do not use this cut boundary for bias-carrying lines."
- "Do not promote optimizer rows without the flatness goal active."
- "Do not trust this analytic line length without true EM phase verification."

Bad examples:

- "This topology never works."
- "EM is unreliable."
- "Optimizer is useless."

## Reporting Language

Use precise status words:

- `pass`: all configured gates and evidence level satisfied;
- `provisional`: useful but below required evidence level;
- `fail`: hard gate failed with valid evidence;
- `blocked_internal`: fixable by project work;
- `blocked_external`: missing tool, deck, license, or user-supplied artifact;
- `needs_user_decision`: several valid engineering paths exist and exceed the
  agent's authority.
