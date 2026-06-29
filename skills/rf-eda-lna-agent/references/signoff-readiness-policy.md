# Signoff Readiness Policy

Signoff-ready is not signoff-clean.

## Readiness

A project is signoff-ready when:

- the final layout is complete;
- configured electrical evidence is present;
- known connectivity blockers are resolved;
- required pads and pins are present;
- artifact manifest points to final evidence;
- official signoff collateral is available or explicitly blocked.

## Clean Signoff

Claim signoff-clean only with:

- official DRC report;
- official LVS report;
- required layer map;
- required device-recognition map;
- no waived errors unless user-approved and documented.

## External Blocker

If decks or maps are unavailable:

```text
verdict: blocked_external
minimum unlock action: obtain official signoff collateral
```

Do not fabricate substitute DRC/LVS results.

