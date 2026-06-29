# Agent Architecture

The agent is a workflow executor and evidence manager, not a universal RF optimizer.

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

## Promotion Rule

Promote only when:

```text
configured hard targets pass
required evidence level is met
verification harness is independent enough for the claim
artifact manifest points to reproducible evidence
```

Retire only when enough bounded attempts support the same negative conclusion.

