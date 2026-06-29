# Exploration Tree Management

The exploration tree is the durable memory of the engineering process.

## Branch Lifecycle

1. Start from a named seed.
2. State one hypothesis.
3. Declare allowed and forbidden changes.
4. Run a bounded harness.
5. Record metrics and evidence.
6. Promote, continue, retire, or block.

Each lifecycle step must leave an artifact. A branch that only exists in chat is
not durable enough for long EDA work.

## Status Vocabulary

Use controlled statuses:

```text
active
active_warning
boundary
promoted
retired
blocked_external
blocked_tool
blocked_physics
superseded
```

## Promotion Rules

Promote only when:

- every configured hard target passes;
- the required evidence level is met;
- the verification harness is independent enough for the claim;
- the artifact manifest points to reproducible evidence.

Promotion is invalid when:

- the result was produced on a lower-fidelity model than the gate requires;
- any hard metric was omitted from the objective or post-check;
- a lower-level placeholder artifact is being used as a signoff artifact;
- the layout geometry has not been synchronized to the promoted variables.

## Retirement Rules

Retire only when:

- the same hypothesis was tested with enough budget;
- no near-boundary candidate remains;
- the failure reason is understood;
- a do-not-repeat rule is recorded.

Do not retire a broad architecture because one fixture failed. Retire the exact
mechanism/fixture boundary that evidence supports.

## GitHub Policy

When using GitHub:

- commit lightweight config, docs, scripts, summaries, and manifests;
- do not commit raw solver work directories by default;
- use branches for experimental work;
- keep the main branch readable as the exploration tree of record;
- compare local and remote before assuming history is complete.

Remote branches should be inventoried, not blindly merged. When local and remote
history diverge, write a comparison summary with local-only, remote-only, and
changed docs/scripts before rewriting the public narrative.

## Exploration Tree Schema

Recommended JSONL record:

```json
{
  "id": "C001",
  "parent": "C000",
  "branch": "short-name",
  "hypothesis": "one sentence",
  "allowed_changes": [],
  "forbidden_changes": [],
  "harness": "script or GUI protocol",
  "metrics": {},
  "evidence_level": "E2",
  "artifacts": [],
  "decision": "continue",
  "retirement_reason": "",
  "do_not_repeat": [],
  "next_action": ""
}
```

Markdown summaries should be human-readable, but JSONL is the source for
automation.

