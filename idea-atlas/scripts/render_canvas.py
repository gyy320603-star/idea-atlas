#!/usr/bin/env python3
"""Build an offline atlas from the run's JSON manifest using Python 3.8+.

Usage: python3 scripts/render_canvas.py visual/manifest.json visual/atlas.html
The template lives in ../templates relative to this script, irrespective of cwd.
"""

import argparse
import json
import math
import os
from pathlib import Path
import tempfile


STATUSES = {"live", "needs-evidence", "killed", "duplicate", "seed", "variant"}
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "atlas-canvas.html"
CARD_TEXT = ("family", "role", "occasion", "freq", "current", "relationship",
             "sub", "gap", "promise", "mechanism", "how", "action", "tradeoff",
             "proof", "kill", "claim", "insight", "statusReason", "evidence", "evidenceNotes")


def mapping(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return value


def required_text(obj, key, label):
    item = obj.get(key)
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{label}.{key} must be nonempty text")
    return item


def optional_text(obj, keys, label):
    for key in keys:
        if obj.get(key) is not None and not isinstance(obj[key], str):
            raise ValueError(f"{label}.{key} must be text")


def validate(data):
    mapping(data, "manifest")
    optional_text(data, ("language",), "manifest")
    project = mapping(data.get("project"), "project")
    required_text(project, "title", "project")
    optional_text(project, ("subtitle",), "project")
    reframed = "readings" in data
    readings = mapping(data.get("readings", {}), "readings")
    if reframed and not readings:
        raise ValueError("readings must contain at least one reading")
    for key, reading in readings.items():
        label = f"readings[{key!r}]"
        if not key.strip():
            raise ValueError("reading IDs must be nonempty")
        mapping(reading, label)
        for field in ("name", "q", "premise", "audience", "check"):
            required_text(reading, field, label)

    lenses = mapping(data.get("lenses", {}) if reframed else data.get("lenses"), "lenses")
    cards = mapping(data.get("cards"), "cards")
    if not reframed and (not lenses or not cards):
        raise ValueError("provide at least one lens and one card")
    for key, lens in lenses.items():
        label = f"lenses[{key!r}]"
        mapping(lens, label)
        if required_text(lens, "name", label) != key:
            raise ValueError(f"{label}.name must equal its key")
        required_text(lens, "q", label)
        optional_text(lens, ("code",), label)
    for key, card in cards.items():
        label = f"cards[{key!r}]"
        mapping(card, label)
        prefix = "reading:" if reframed else "lens:"
        if required_text(card, "id", label) != key or key == "root" or key.startswith(prefix):
            raise ValueError(f"{label}.id must equal its key and be distinct from navigation keys")
        required_text(card, "title", label)
        if required_text(card, "status", label) not in STATUSES:
            raise ValueError(f"{label}.status must be one of {', '.join(sorted(STATUSES))}")
        if reframed:
            if required_text(card, "reading", label) not in readings:
                raise ValueError(f"{label}.reading must reference a declared reading")
        elif "reading" in card:
            raise ValueError(f"{label}.reading requires manifest.readings")
        if (not reframed or "lens" in card) and required_text(card, "lens", label) not in lenses:
            raise ValueError(f"{label}.lens must reference a declared lens")
        optional_text(card, CARD_TEXT, label)
        links = card.get("links")
        if isinstance(links, list):
            if any(not isinstance(link, str) or not link.strip() for link in links):
                raise ValueError(f"{label}.links array must contain nonempty text")
        else:
            optional_text(card, ("links",), label)
        if card.get("short") is not None:
            short = mapping(card["short"], f"{label}.short")
            optional_text(short, ("why", "risk", "test"), f"{label}.short")
            if "rank" in short and (type(short["rank"]) is not int or short["rank"] < 1):
                raise ValueError(f"{label}.short.rank must be a positive integer")
        if card.get("scores") is not None:
            scores = mapping(card["scores"], f"{label}.scores")
            for dimension, value in scores.items():
                if type(value) not in (int, float) or not math.isfinite(value) or not 1 <= value <= 5:
                    raise ValueError(f"{label}.scores.{dimension} must be a number from 1 to 5")
    handoff = data.get("handoff", [])
    if not isinstance(handoff, list) or any(not isinstance(key, str) or key not in cards for key in handoff):
        raise ValueError("handoff must be an array of known card IDs")
    if len(set(handoff)) != len(handoff):
        raise ValueError("handoff contains duplicate IDs")
    for key, record in mapping(data.get("grill", {}), "grill").items():
        label = f"grill[{key!r}]"
        if key not in cards:
            raise ValueError(f"{label} references an unknown card")
        mapping(record, label)
        required_text(record, "verdict", label)
        optional_text(record, ("note",), label)
        rounds = record.get("rounds")
        if not isinstance(rounds, list) or not rounds:
            raise ValueError(f"{label}.rounds must be a nonempty array")
        for number, entry in enumerate(rounds, 1):
            round_label = f"{label} round {number}"
            mapping(entry, round_label)
            for field in ("q", "consider", "decision"):
                required_text(entry, field, round_label)


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key {key!r}")
        obj[key] = value
    return obj


def render(manifest, output):
    if output.resolve() in (manifest.resolve(), TEMPLATE.resolve()):
        raise ValueError("give the rendered HTML its own output path")
    data = json.loads(manifest.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    validate(data)
    template = TEMPLATE.read_text(encoding="utf-8")
    marker = "__ATLAS_DATA__"
    if template.count(marker) != 1:
        raise ValueError(f"{TEMPLATE.name} must contain exactly one {marker} marker")
    # Older manifests may carry alternate copy. The viewer always renders the source records.
    source = {key: value for key, value in data.items() if key != "translations"}
    payload = json.dumps(source, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    # JSON inside an HTML script element is still parsed as raw text by the browser.
    payload = payload.replace("<", r"\u003c").replace(">", r"\u003e").replace("&", r"\u0026")
    result = template.replace(marker, payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent,
                                         suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(result)
        os.replace(temporary, output)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()
    return len(data.get("readings") or data["lenses"]), len(data["cards"])


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        branches, cards = render(args.manifest, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot build canvas: {exc}\n")
    print(f"{args.output} ({branches} branches, {cards} cards)")


if __name__ == "__main__":
    main()
