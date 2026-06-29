# Deep Harness Playbook

This playbook converts a large collection of project-specific scripts into
reusable harness families. Do not copy private scripts verbatim into a public
agent. Instead, preserve their interfaces, evidence products, gates, and failure
responses.

## Harness Family Map

| Family | Purpose | Typical inputs | Required outputs |
|---|---|---|---|
| Inventory | Discover docs, scripts, candidates, manifests, and result folders | workspace root, candidate regex, include/exclude rules | inventory JSON, Markdown summary, size summary |
| History/remote audit | Compare local history with remote or archived snapshots | repo root, snapshot refs, file filters | path/hash diff, remote-only list, changed-file list |
| Simulation | Build or patch a netlist and run configured analyses | seed, netlist template, tool runner, metric config | raw log, dataset pointer, metric JSON, summary |
| Optimizer | Search bounded variables while enforcing all hard gates | variables, bounds, goals, budgets, resource policy | iteration log, best rows, rejected rows, independent verify |
| Touchstone audit | Decide whether an S-parameter file can be embedded | SnP path, port count, band, DC requirement | verdict, frequency coverage, warnings |
| EM/cosim | Extract physical blocks and embed them into a circuit harness | layout cell, port map, model partition | SnP, embed netlist, equivalence/control result |
| Layout growth | Add physical devices and interconnect one block at a time | layout cell, block plan, screenshot plan | screenshots, geometry net coverage, local cosim |
| GUI control | Open exactly the target schematic/layout and capture evidence | GUI script, window/cell target | screenshot set, window count, lock status |
| Signoff readiness | Check whether final physical verification can be claimed | deck paths, reports, GDS, LVS mapping | ready/blocked status, missing collateral |
| Artifact guard | Keep Git and solver directories under budget | root, size budget, allowlist | largest files, manifest, cleanup proposal |

## Candidate Record Contract

Every candidate or branch record must include:

- candidate ID;
- parent/seed candidate;
- hypothesis;
- changed topology or variables;
- fixed assumptions and forbidden shortcuts;
- harness script and command;
- raw evidence paths;
- metric summary;
- evidence level;
- decision: promote, continue, retire, or blocked;
- do-not-repeat rule when retired;
- next action.

If any of these fields is missing, the candidate is provisional.

## Evidence Levels

Use project-configured names if available. A generic default ladder is:

1. mechanism smoke;
2. schematic simulation;
3. fine-grid schematic verification;
4. physical primitive schematic;
5. block EM plus embedding control;
6. hybrid EM/circuit verification;
7. layout connectivity verification;
8. DRC/LVS clean with official reports.

Promotion requires the evidence level configured for the current gate.

## Harness Design Rules

- One harness answers one question.
- The cheapest harness is acceptable only if it matches the decision being made.
- A control experiment is mandatory before trusting a new embedding method.
- Logs and metric JSON are evidence; screenshots are evidence only for visual
  or layout questions.
- Solver outputs stay outside Git unless the artifact policy explicitly allows
  them.
- A failed harness must leave a blocker record, not a silent partial result.

## Anti-Patterns

- "Run a large optimizer and see what happens."
- "Replace a physical region with SnP because it looks passive."
- "Declare layout connected because pins have matching net names."
- "Declare signoff clean because GDS export succeeded."
- "Delete temporary data before preserving manifests and best evidence."
- "Summarize history from the current worktree without checking remote branches."
