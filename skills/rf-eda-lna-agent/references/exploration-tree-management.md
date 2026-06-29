# Exploration Tree Management

The exploration tree is the durable memory of the engineering process.

## Branch Lifecycle

1. Start from a named seed.
2. State one hypothesis.
3. Declare allowed and forbidden changes.
4. Run a bounded harness.
5. Record metrics and evidence.
6. Promote, continue, retire, or block.

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

## Retirement Rules

Retire only when:

- the same hypothesis was tested with enough budget;
- no near-boundary candidate remains;
- the failure reason is understood;
- a do-not-repeat rule is recorded.

## GitHub Policy

When using GitHub:

- commit lightweight config, docs, scripts, summaries, and manifests;
- do not commit raw solver work directories by default;
- use branches for experimental work;
- keep the main branch readable as the exploration tree of record;
- compare local and remote before assuming history is complete.

