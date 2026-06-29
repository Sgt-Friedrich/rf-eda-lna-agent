# History Mining And Remote Audit

Long EDA projects rarely live in one clean local worktree. Branches, forks,
temporary solver directories, GUI-generated cells, and abandoned scripts often
hold different parts of the exploration history. The agent must mine history
before it writes a summary, rebuilds a skill, or declares that a design path has
already been exhausted.

## Required Sources

When history matters, inspect all available evidence classes:

- current local worktree;
- configured Git remotes and selected branches;
- archived snapshots or exported bundles supplied by the user;
- project docs, status logs, candidate registries, and issue/PR records;
- scripts, harness outputs, metric JSON, Touchstone manifests, and layout audit
  reports.

Do not assume the current local checkout is complete. A remote branch may
preserve older architecture notes or negative results that were later deleted
locally.

## Safe Remote Audit Loop

1. Resolve the repository root and remote URL.
2. Fetch remote refs in read-only mode.
3. Create temporary snapshots of selected refs without checking them out over
   the working tree.
4. Inventory local and snapshot trees with the same scanner.
5. Compare docs, scripts, configs, and manifests by path plus content hash.
6. List local-only, remote-only, and changed files.
7. Extract reusable policy from changed files.
8. Never overwrite current local artifacts from a remote snapshot without an
   explicit merge request.

## What To Record

Each history audit should produce:

- sources scanned;
- candidate ID coverage;
- script-family counts;
- remote-only or changed policy files;
- retired branch reasons;
- evidence-level distribution;
- open blockers and missing collateral;
- instructions for what not to repeat.

## Public Export Boundary

For open-source packaging, history mining is used to extract patterns, not to
publish private evidence. Public summaries must avoid:

- local absolute paths;
- proprietary process or PDK names;
- real layout, database, solver, or foundry files;
- project-specific candidate identifiers;
- project-specific metric thresholds;
- screenshots or curves that reveal private implementation details.

Use synthetic candidate IDs such as `C001` in public examples.

## History Lessons To Preserve

The most valuable history is not the final winning row. Preserve:

- false promotions and why they were rejected;
- optimizer objective mistakes;
- EM cut-boundary mistakes;
- GUI/layout connectivity mistakes;
- missing-deck or missing-tool blockers;
- branch retirement rules;
- where a simplified mechanism result stopped being valid evidence.

The skill should guide future agents to ask, "Which past result closed this
neighborhood, and at what evidence level?" before spending another optimization
round.
