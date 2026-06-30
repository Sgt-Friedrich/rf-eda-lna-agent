#!/usr/bin/env python3
"""Convert a sanitized book inventory into RF agent knowledge cards.

The input is produced by `book_knowledge_inventory.py`. The output contains
topic cards derived from chapter headings and keyword signals only. It does not
copy textbook body text.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


TOPIC_RULES: dict[str, dict] = {
    "transmission_lines_and_reference_planes": {
        "patterns": ["transmission", "microstrip", "stripline", "smith", "abcd", "scattering", "quarter-wave", "tapered"],
        "agent_use": "Check port reference planes, physical/electrical line consistency, matching bandwidth, and EM frequency coverage.",
        "harness_links": ["em_cosim", "optimizer", "touchstone_audit"],
        "sanity_gates": ["reference_plane_consistency", "frequency_coverage", "line_geometry_physicalized"],
    },
    "matching_gain_and_two_port_stability": {
        "patterns": ["matching", "two-port", "stability", "power gains", "transducer", "lna"],
        "agent_use": "Keep gain, match, and stability coupled in objectives and verification.",
        "harness_links": ["optimizer", "simulation", "metrics_gate"],
        "sanity_gates": ["all_hard_metrics_active", "fine_grid_verify", "stability_range_covered"],
    },
    "noise_parameters_and_cascade_budget": {
        "patterns": ["noise", "noise figure", "noise parameters", "cascaded", "noise circles", "fet noise"],
        "agent_use": "Score low-noise candidates by system cascade burden, effective gain, and input passive loss.",
        "harness_links": ["simulation", "optimizer", "cosim_embedding"],
        "sanity_gates": ["linear_domain_noise_budget", "downstream_burden_recorded", "input_loss_audited"],
    },
    "physical_passives_and_layout_returns": {
        "patterns": ["inductor", "capacitor", "resistor", "via", "airbridge", "crossover", "transformer", "balun", "biasing"],
        "agent_use": "Audit passive feasibility, access metal, self-resonance risk, via/source return, and bias/decoupling geometry.",
        "harness_links": ["layout_growth", "em_extraction", "audit_diagnostic"],
        "sanity_gates": ["no_unrealistic_ideal_passives", "access_and_return_included", "conductive_geometry_checked"],
    },
    "nonlinear_and_large_signal": {
        "patterns": ["nonlinear", "large-signal", "harmonic", "volterra", "intermodulation", "compression", "power amplifier"],
        "agent_use": "Require separate nonlinear verification for compression and intercept claims.",
        "harness_links": ["large_signal", "simulation", "metrics_gate"],
        "sanity_gates": ["drive_sweep_recorded", "tone_setup_recorded", "convergence_checked"],
    },
    "cad_and_eda_workflow": {
        "patterns": ["cad", "ads", "simulation", "exact designs", "parameter extraction"],
        "agent_use": "Require setup, logs, extracted metrics, and independent verification for CAD-generated evidence.",
        "harness_links": ["schematic_generation", "optimizer", "process_artifact"],
        "sanity_gates": ["raw_log_saved", "metric_json_saved", "independent_verify"],
    },
}


def normalize_source_name(file_name: str) -> str:
    name = Path(file_name).stem
    name = re.sub(r"^\d+_", "", name)
    name = name.replace("_", " ")
    return name


def classify_signal(signal: str) -> list[str]:
    lowered = signal.lower()
    topics = []
    for topic, rule in TOPIC_RULES.items():
        if any(pattern in lowered for pattern in rule["patterns"]):
            topics.append(topic)
    return topics


def build_cards(inventory: dict) -> list[dict]:
    bucket: dict[str, dict] = {}
    blockers: list[dict] = []
    for record in inventory.get("records", []):
        source = normalize_source_name(record.get("file_name", "unknown"))
        status = record.get("status", "unknown")
        if status != "extracted":
            blockers.append(
                {
                    "source": source,
                    "status": status,
                    "blocker": record.get("toc_error") or record.get("metadata_error") or "text extraction unavailable",
                }
            )
            continue
        signals = list(record.get("chapter_or_toc_signals", [])) + list(record.get("keyword_signals", []))
        for signal in signals:
            for topic in classify_signal(signal):
                item = bucket.setdefault(
                    topic,
                    {
                        "topic": topic,
                        "sources": set(),
                        "source_signals": [],
                        "agent_use": TOPIC_RULES[topic]["agent_use"],
                        "harness_links": TOPIC_RULES[topic]["harness_links"],
                        "sanity_gates": TOPIC_RULES[topic]["sanity_gates"],
                    },
                )
                item["sources"].add(source)
                if len(item["source_signals"]) < 18 and signal not in item["source_signals"]:
                    item["source_signals"].append(signal)

    cards = []
    for topic in sorted(bucket):
        card = bucket[topic]
        card["sources"] = sorted(card["sources"])
        cards.append(card)
    if blockers:
        cards.append(
            {
                "topic": "extraction_blockers",
                "sources": sorted({b["source"] for b in blockers}),
                "source_signals": [f"{b['source']}: {b['status']}" for b in blockers],
                "agent_use": "Do not derive lessons from unavailable source text; repair/OCR or manually review first.",
                "harness_links": ["book_knowledge_inventory"],
                "sanity_gates": ["no_unread_source_claims"],
            }
        )
    return cards


def write_markdown(path: Path, cards: list[dict]) -> None:
    lines = [
        "# RF Textbook Knowledge Cards",
        "",
        "Generated from sanitized metadata, chapter headings, and keyword signals.",
        "Do not treat this file as copied textbook content.",
        "",
    ]
    for card in cards:
        lines.append(f"## {card['topic'].replace('_', ' ').title()}")
        lines.append("")
        lines.append("- Sources: " + (", ".join(card["sources"]) if card["sources"] else "none"))
        lines.append("- Agent use: " + card["agent_use"])
        lines.append("- Harness links: " + ", ".join(card["harness_links"]))
        lines.append("- Sanity gates: " + ", ".join(card["sanity_gates"]))
        if card.get("source_signals"):
            lines.append("- Chapter/theme signals:")
            for signal in card["source_signals"][:12]:
                lines.append(f"  - {signal}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
    cards = build_cards(inventory)
    args.out.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "card_count": len(cards),
        "cards": cards,
        "copyright_boundary": "derived from metadata/headings/signals only; no textbook body text",
    }
    (args.out / "book_knowledge_cards.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(args.out / "book_knowledge_cards.md", cards)
    print(json.dumps({"verdict": "ok", "card_count": len(cards), "out": str(args.out)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
