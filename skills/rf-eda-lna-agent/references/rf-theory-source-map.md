# RF Theory Source Map

Use this map when managing source extraction and reading provenance. For the
actual distilled engineering rules, read `rf-textbook-distilled-knowledge.md`.
This file is a reading index, not a copy of any textbook.

## Source Coverage

| Source family | Useful areas for the agent | How to use in workflow |
|---|---|---|
| Microwave network theory | transmission lines, Smith chart, scattering parameters, ABCD matrices, matching sections | validate ports, reference planes, matching targets, and transfer blocks before simulation claims |
| Microwave circuit design | active devices, two-port stability, low-noise amplifier design, noise parameters, cascaded noise, broadband amplifiers | form mechanism hypotheses and system budgets before optimizer runs |
| Nonlinear microwave circuits | nonlinear device models, large-signal scattering, harmonic balance, Volterra/power-series methods, balanced/multiple-device circuits | define compression/intermodulation/HB checks and reject small-signal-only delivery claims |
| RF/microwave lumped elements | inductors, capacitors, resistors, vias, airbridges, transformers, biasing networks, microstrip implementation | audit physical feasibility, parasitic limits, source returns, and bias/decoupling networks |
| RFIC design texts | noise, matching loss, scattering parameters, LNA input matching, passive devices, transmission lines | translate RFIC tradeoffs into hard gates and sanity checks |
| ADS/CAD workflow texts | circuit models, parameter sweeps, optimizer setup, EM/circuit workflow | shape harness contracts and evidence artifacts |

## Current Local Extraction Summary

The following source types have been sampled into chapter-level signals:

- microwave network theory: extracted;
- microwave circuit design and LNA/noise chapters: extracted;
- nonlinear microwave/RF circuit chapters: extracted;
- lumped RF/microwave element chapters: extracted;
- RF microelectronics chapters: extracted.

The following source types require repair, OCR, or manual source review before
being used:

- damaged CMOS RFIC PDF that fails both text extraction and page rendering;
- damaged ADS microwave CAD PDF that fails both text extraction and page rendering;
- microwave transistor amplifier solutions/excerpt file that renders, but the
  sampled pages do not expose enough textbook chapter content for reliable
  knowledge extraction.

## Extraction Status Rules

- A source is usable only after metadata and chapter-level signals are extracted
  or manually reviewed.
- If text extraction fails, record `needs_repair_or_ocr`; do not infer lessons.
- Do not copy textbook body text, figures, tables, or long derivations into the
  public skill.
- Record source titles and chapter-level themes only; write agent guidance as
  original summaries.

## Routing

- Noise or cascade budget questions: read `rf-formula-and-sanity-gates.md`.
- Passive element, via, return path, bias, or layout questions: read
  `rf-passive-and-layout-checklists.md`.
- Compression, intermodulation, HB, or nonlinear questions: read
  `rf-large-signal-and-nonlinear-checklists.md`.
- ADS or CAD loop construction questions: read `rf-ads-cad-workflow-map.md`.

## Knowledge-To-Harness Link

For each theory item, the agent should preserve this chain:

```text
theory premise -> candidate hypothesis -> harness choice -> evidence gate -> exploration-tree record
```

Examples:

- Transmission-line theory informs port reference plane and phase sensitivity
  checks in EM/cosim harnesses.
- Cascaded noise theory informs optimizer objectives and rejects low-noise but
  low-effective-gain candidates.
- Lumped-element parasitic theory informs layout readiness and rejects
  unrealistic ideal passives in final candidates.
- Nonlinear circuit theory informs large-signal checks before delivery.
