# EDA Adapter Patterns

EDA automation needs a thin adapter layer around vendor tools. The adapter is
not just a command runner; it protects database connectivity, GUI state,
processes, and evidence capture.

## Runtime Selection

Use the EDA-vendor Python or scripting runtime when touching an EDA database.
System Python is acceptable for text processing, manifests, and generic audits,
but it usually cannot import vendor database APIs.

Record the runtime in `config/project.yaml`:

```yaml
eda:
  vendor: "<user supplied>"
  version: "<user supplied>"
  python: "<path or command supplied by user>"
  gui_launcher: "<path or command supplied by user>"
```

No public template should hard-code a tool install directory.

## Schematic Generation Rules

- Draw real wires between component pins.
- Use labels only as intentional node names, not as invisible jumpers.
- Keep ground naming consistent with the simulator.
- Probe symbol pin order before generating a new device family.
- Keep RF, DC, bias, ground return, and simulation setup visually traceable.
- Run netlist audits for dangling nodes, same-node device shorts, and missing
  required instances.

## GUI Rules

Some operations should deliberately use GUI or computer-use:

- pCell artwork refresh;
- visual inspection of dense RF layout;
- screenshot evidence requested by the user;
- resolving database locks or stale windows;
- validating that auto-generated geometry follows RF floorplan intent.

Keep GUI usage disciplined:

- open only the target cell/window;
- close stale windows before new attempts;
- capture focused screenshots after each layout growth step;
- do not rely on screenshots as a replacement for database connectivity.

## Common Tool Errors

| Symptom | Likely cause | Response |
|---|---|---|
| Vendor Python module missing | system Python used for database task | rerun with configured EDA Python |
| Database lock error | stale GUI/session holds the cell | close target windows, clear stale lock only if safe |
| Protected scripting word assignment | local variable/function conflicts with EDA language | rename the symbol and rerun |
| Missing DLL from GUI callback | launcher environment lacks runtime path | launch through configured environment wrapper |
| Headless pCell artwork wrong | callback needs GUI/artwork refresh | open GUI and refresh/capture proof |

## Acceptance Artifacts

For every generated schematic or layout cell, write an acceptance bundle:

- command line or GUI action;
- runtime used;
- created or modified cell names;
- netlist or connectivity audit summary;
- screenshot paths when GUI was part of the gate;
- known limitations;
- next gate.
