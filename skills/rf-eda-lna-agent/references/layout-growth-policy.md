# Layout Growth Policy

Layout is grown as physical evidence, not as a one-shot netlist drawing.

## Growth Loop

1. Place or select one physical block.
2. Draw one connection family.
3. Capture screenshot or equivalent visual review.
4. Run database connectivity audit.
5. Run local cosim or anchor simulation when meaningful.
6. Freeze or repair before adding more.

## Required Checks

- visual connectivity;
- conductive database connectivity;
- correct pin-to-net intent;
- no floating conductive shapes;
- no scaffold/reference leftovers mistaken for real metal;
- access and return paths included for physical devices.

## RF Layout Discipline

Avoid:

- arbitrary all-net auto-routing;
- right-angle RF transmission lines unless intentional;
- long unrealistic component bodies;
- disconnected stubs;
- unreviewed pad or bias routing;
- promoting a layout without screenshots when GUI review was requested.

## Block Promotion

A layout block is promotable only when both geometry intent and database connectivity support the intended electrical boundary.

