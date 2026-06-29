# Agent Architecture

The agent is a workflow executor and evidence manager, not a universal RF optimizer.

The agent must behave like a disciplined RF design flow runner:

- clarify the design contract before running tools;
- build one bounded experiment at a time;
- keep every candidate tied to evidence;
- refuse promotion when the evidence level is too low;
- preserve negative results as do-not-repeat rules;
- keep local and GitHub histories synchronized at the text/manifest level;
- keep heavy EDA data outside Git unless the user explicitly changes policy.

## State Machine

```text
S0 orient
S1 classify task
S2 select harness
S3 run bounded experiment
S4 verify evidence
S5 update exploration tree
S6 promote / retire / block
S7 cleanup resources
```

## Operating Loop

For every non-trivial design action:

1. Read the active `goal.md` and metric config.
2. Identify the current gate and required evidence level.
3. Select the smallest harness that can answer that gate.
4. Run the harness with a time/artifact budget.
5. Verify results independently of the producing optimizer or GUI action.
6. Append candidate status and artifacts to the exploration tree.
7. If a hard gate fails, record the failure mode before retuning.
8. If a blocker is external, stop with the smallest unlock action.

Do not skip directly from schematic metrics to layout/signoff claims.

## Evidence Levels

| Level | Name | Meaning |
|---:|---|---|
| E0 | Hypothesis | Design idea or literature mechanism; not simulated. |
| E1 | Harness compiles | Netlist/script/setup compiles or opens. |
| E2 | Schematic simulation | Circuit-level evidence for user-configured analyses. |
| E3 | Fine-grid verified | Optimizer result verified on an honest grid. |
| E4 | Physical schematic | Uses physical primitives or documented audit models. |
| E5 | Block EM embedded | One or more passive/layout blocks extracted and embedded. |
| E6 | Hybrid EM/circuit | Active/noise models and EM blocks co-simulated together. |
| E7 | Complete layout connectivity | Layout connectivity checked visually and by database/net extraction. |
| E8 | Signoff-ready | Layout prepared for official DRC/LVS, but not claimed clean. |
| E9 | Signoff-clean | Official DRC/LVS reports are clean. |
| E10 | Delivery | GDS/package/report exported with evidence. |

## Candidate Record

```yaml
id: CANDIDATE_ID
parent: PARENT_ID
branch: branch_name
hypothesis: short claim
seed: seed ID or artifact
changed_variables: []
forbidden_changes: []
evidence_level: E0
metrics: {}
artifacts: []
decision: promote|retire|blocked|continue
do_not_repeat: []
next_action: short action
```

The record is incomplete if it lacks the command/script, evidence path, or
decision reason. Incomplete records may be useful notes, but they cannot drive
promotion.

## Branch Classes

- mechanism branch: tests a physical idea with simplified fixtures;
- candidate branch: pursues a full design under configured gates;
- diagnostic branch: isolates a failure mode;
- layout-growth branch: adds physical geometry one block at a time;
- signoff branch: verifies final artifacts and collateral.

Mechanism branches are allowed to use simplified assumptions only when they are
explicitly labeled and retired before final promotion.

## Promotion Rule

Promote only when:

```text
configured hard targets pass
required evidence level is met
verification harness is independent enough for the claim
artifact manifest points to reproducible evidence
```

Retire only when enough bounded attempts support the same negative conclusion.

## Resource Discipline

EDA projects can produce large solver trees quickly. The agent must keep:

- Git lightweight;
- solver directories under the configured artifact budget;
- manifests for heavy artifacts;
- no automatic deletion outside the configured workspace;
- no destructive cleanup before preserving evidence for the active gate.

## Human/GUI Boundary

Headless scripts are preferred for repeatability, but GUI review is a valid
harness when the question is visual or pCell/database related. GUI gates should
open the fewest windows possible, capture screenshots, and then close or leave a
clear window state.
