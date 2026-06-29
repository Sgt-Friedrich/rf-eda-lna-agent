# Layout Exploration Playbook

Layout exploration must grow from verified physical blocks. The agent should not
convert an entire netlist into arbitrary wiring and then try to debug the whole
thing at once.

## Block-Growth Protocol

1. Start from the latest verified layout seed.
2. Select one physical block or one connection family.
3. Place or redraw it with RF floorplan intent.
4. Capture focused screenshots.
5. Run geometry net-coverage and pin-net checks.
6. Run local cosim or equivalence check when the block can affect metrics.
7. Freeze, repair, or roll back before adding the next block.

## Layout Questions The Agent Must Ask

- Is the geometry physically plausible for the target process and user rules?
- Are access lines, returns, and vias included?
- Does a screenshot show the same connectivity the database claims?
- Does the block preserve the intended EM cut boundary?
- Does the layout variable value match the schematic/model variable?
- Does this block require audit-mode instead of black-box replacement?

## Connectivity Levels

| Level | Meaning | Promotion use |
|---|---|---|
| pin intent | instance pins are assigned intended nets | useful but insufficient |
| database net | shapes are assigned nets | still not enough if reference shapes are fake |
| conductive geometry | physical metal/via continuity exists | required before EM |
| visual RF review | screenshots match RF floorplan intent | required when GUI review is requested |
| local cosim | circuit anchor survives the block | required for metric-sensitive growth |

## Forbidden Shortcuts

- one-shot all-net auto-routing for RF-critical layout;
- right-angle or arbitrary routing where the project requires transmission-line discipline;
- keeping scaffold/reference shapes as if they were real metal;
- relying on pin-net equality when unnetted conductive shapes remain;
- promoting a layout that cannot be opened or inspected in the GUI.

## Evidence Bundle

For each layout growth step:

- layout cell and block name;
- changed shapes/devices;
- before/after screenshots;
- net-coverage summary;
- local cosim result or reason not applicable;
- decision and next block.
