# Layout Growth Policy

Layout is grown as physical evidence, not as a one-shot netlist drawing.

## Growth Loop

1. Place or select one physical block.
2. Draw one connection family.
3. Capture screenshot or equivalent visual review.
4. Run database connectivity audit.
5. Run local cosim or anchor simulation when meaningful.
6. Freeze or repair before adding more.

Do not grow a whole netlist at once. RF layout closure depends on orientation, access length, tapering, return current path, coupling, and nearby shielding. Automatic all-net routing can create a database-connected layout that is physically useless.

## Required Checks

- visual connectivity;
- conductive database connectivity;
- correct pin-to-net intent;
- no floating conductive shapes;
- no scaffold/reference leftovers mistaken for real metal;
- access and return paths included for physical devices.

Pin-level equivalence is not the same as conductive metal continuity. A layout can have every instance pin bound to the intended net while route polygons, reference shapes, or access lines remain floating. Run a geometry net-coverage check before any EM claim.

## RF Layout Discipline

Avoid:

- arbitrary all-net auto-routing;
- right-angle RF transmission lines unless intentional;
- long unrealistic component bodies;
- disconnected stubs;
- unreviewed pad or bias routing;
- promoting a layout without screenshots when GUI review was requested.

Prefer smooth or tapered RF transitions, explicit source/ground returns, physically reasonable component dimensions, local screenshots after each block, and one open main layout window instead of many stale edit windows.

## Block Promotion

A layout block is promotable only when both geometry intent and database connectivity support the intended electrical boundary.

Promotion should leave a compact bundle: layout cell name, screenshot paths, net-coverage summary, changed devices/routes, cosim verdict, and next block.

