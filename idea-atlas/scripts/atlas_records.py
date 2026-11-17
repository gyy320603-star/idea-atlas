"""Project a frozen independent response into the existing atlas file formats."""

import html
import json
import os
from pathlib import Path
import re
import tempfile

from render_canvas import render, required_text, validate


# Each member is used on both the individual card and its standalone table.
FIELDS = (
    ("status", "初筛", "Initial gate"), ("statusReason", "初筛理由", "Gate reason"),
    ("family", "家族", "Family"), ("reading", "读法", "Reading"),
    ("lens", "视角", "Lens"), ("insight", "题面启发", "Insight"),
    ("role", "谁在行动", "Role"), ("occasion", "场合", "Occasion"),
    ("freq", "频率", "Frequency"), ("current", "当前行为", "Current behaviour"),
    ("relationship", "涉及的人", "Relationship"), ("sub", "现有替代", "Substitute"),
    ("gap", "空位", "Decision-changing gap"), ("promise", "价值承诺", "Promise"),
    ("action", "设计动作", "Design action"), ("mechanism", "机制", "Mechanism"),
    ("how", "使用过程", "Interaction"), ("tradeoff", "代价", "Tradeoff"),
    ("claim", "待证主张", "Claim"), ("evidence", "证据等级", "Evidence"),
    ("evidenceNotes", "依据与局限", "Evidence notes"), ("links", "相邻方向", "Related cards"),
)
OPTIONAL = {"reading", "lens", "insight", "links"}
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")
RESERVED_ID = re.compile(r"CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9]", re.I)


def check_result(envelope):
    if not isinstance(envelope, dict):
        raise ValueError("result must be a JSON object")
    required_text(envelope, "scan", "result")
    manifest = envelope.get("manifest")
    validate(manifest)
    seen = set()
    for key, card in manifest["cards"].items():
        if (not SAFE_ID.fullmatch(key) or RESERVED_ID.fullmatch(key)
                or key.casefold() in seen):
            raise ValueError(f"unsafe or colliding card file ID: {key!r}")
        seen.add(key.casefold())
        for field, _, _ in FIELDS:
            if field not in OPTIONAL:
                required_text(card, field, key)
        for field in ("proof", "kill"):
            required_text(card, field, key)
        if "readings" in manifest:
            required_text(card, "insight", key)
        if card["evidence"] not in {"green", "yellow", "grey"}:
            raise ValueError(f"{key}.evidence must be green, yellow or grey")
        if card["status"] in {"variant", "duplicate"}:
            if isinstance(card.get("links"), list):
                if not card["links"]:
                    raise ValueError(f"{key}.links must identify the related card")
            else:
                required_text(card, "links", key)
        if card.get("short") is not None:
            if card["status"] not in {"live", "needs-evidence"}:
                raise ValueError(f"{key}: cannot recommend a {card['status']} card")
            for field in ("why", "risk", "test"):
                required_text(card["short"], field, f"{key}.short")
            if "rank" not in card["short"]:
                raise ValueError(f"{key}.short needs a rank")
    return manifest


def inline(value):
    """Model-written text in a heading, paragraph or GFM table cell."""
    escaped = html.escape(" ".join(str(value).splitlines()), quote=False)
    return re.sub(r"([\\`*_\[\]|~])", r"\\\1", escaped)


def card_table(card, zh):
    head = inline(card["id"] + " · " + card["title"])
    rows = [f"## {head}", "", "| 项 | 内容 |" if zh else "| Field | Record |", "|---|---|"]
    for key, chinese, english in FIELDS:
        if card.get(key):
            value = card[key]
            if key == "links" and isinstance(value, list):
                value = " · ".join(value)
            rows.append(f"| {chinese if zh else english} | {inline(value)} |")
    rows.extend(("", f"- **Proof** · {inline(card['proof'])}",
                 f"- **Kill** · {inline(card['kill'])}"))
    return "\n".join(rows)


def write_documents(stage, manifest, scan, brief):
    cards = manifest["cards"]
    language = manifest.get("language")
    zh = (language.lower().split("-")[0] == "zh" if language
          else bool(re.search(r"[\u3400-\u9fff]", manifest["project"]["title"] + brief)))

    def label(chinese, english):
        return chinese if zh else english

    def write(name, title, body):
        (stage / name).write_text(f"# {title}\n\n{body.rstrip()}\n", encoding="utf-8")

    def card_link(key):
        return f"[{inline(key + ' · ' + cards[key]['title'])}](cards/{key}.md)"

    def part(card, key):
        return inline(card[key])

    reading_first = "readings" in manifest
    group = "reading" if reading_first else "lens"
    branches = manifest["readings" if reading_first else "lenses"]
    branch_docs, map_docs = [], []
    tables = []
    for key, branch in branches.items():
        name = inline(branch["name"])
        branch_docs.append(f"## {inline(key)} · {name}" if reading_first else f"## {name}")
        branch_docs.append(inline(branch["q"]))
        if reading_first:
            for field, cn, en in (("premise", "前提", "Premise"), ("audience", "决策者", "Audience"),
                                  ("check", "核查", "Check")):
                branch_docs.append(f"**{label(cn, en)}** · {inline(branch[field])}")
        members = [cid for cid, card in cards.items() if card[group] == key]
        lines = [f"- {card_link(cid)} · {part(cards[cid], 'action')}" for cid in members]
        map_docs.append(f"## {name} ({len(members)})\n\n{inline(branch['q'])}\n\n" +
                        ("\n".join(lines) if lines else label("待核查。", "Open question.")))

    # Preserve the literal request, including Markdown or HTML supplied by the user.
    quoted = "\n".join("    " + line for line in brief.splitlines())
    write("00_BRIEF.md", inline(manifest["project"]["title"]), "\n\n".join([quoted] + branch_docs))
    write("01_SCAN.md", label("调查记录", "Scan"), scan)
    write("03_MAP.md", label("分支地图", "Branch map"), "\n\n".join(map_docs))
    (stage / "cards").mkdir()
    for cid, card in cards.items():
        table = card_table(card, zh)
        (stage / "cards" / (cid + ".md")).write_text(table[1:] + "\n", encoding="utf-8")
        tables.append(table)
    write("08_IDEA_TABLES.md", label("逐卡定位表", "Positioning tables"), "\n\n".join(tables))
    families = {card["family"] for card in cards.values()}
    count = (f"{len(cards)} 张方向卡，{len(families)} 个家族。" if zh
             else f"{len(cards)} cards across {len(families)} families.")
    index = [f"- {card_link(cid)} · {part(card, 'status')} · {part(card, 'family')}"
             for cid, card in cards.items()]
    write("02_CANDIDATES.md", label("候选方向", "Candidate directions"), count + "\n\n" + "\n".join(index))

    shortlist = []
    recommended = sorted((c for c in cards.values() if c.get("short")),
                         key=lambda c: c["short"]["rank"])
    for card in recommended:
        short = card["short"]
        shortlist.append(f"## {short['rank']} · {card_link(card['id'])}\n\n" +
                         "\n".join(f"- **{label(cn, en)}** · {inline(short[k])}"
                                   for k, cn, en in (("why", "保留理由", "Rationale"),
                                                     ("risk", "风险", "Risk"), ("test", "下一步", "Next test"))))
    empty = label("暂无推荐。", "No directions recommended.")
    write("04_SHORTLIST.md", label("推荐方向 · 待人选择", "Recommendations · pending human selection"),
          "\n\n".join(shortlist) or empty)
    handoff = [card_table(cards[cid], zh) for cid in manifest.get("handoff", [])]
    write("05_HANDOFF.md", label("交接草稿", "Draft handoff"),
          "\n\n".join(handoff) or label("尚无交接方向。", "No draft finalists."))
    reviews = []
    for cid, record in manifest.get("grill", {}).items():
        rows = [f"## {card_link(cid)}", part(cards[cid], "claim")]
        for i, entry in enumerate(record["rounds"], 1):
            rows.append(f"### {i} · {inline(entry['q'])}")
            rows.extend((f"**{label('权衡', 'Considered')}** · {inline(entry['consider'])}",
                         f"**{label('判断', 'Judgement')}** · {inline(entry['decision'])}"))
        rows.append(inline(record["verdict"]) + " · " + inline(record.get("note") or ""))
        reviews.append("\n\n".join(rows))
    if reviews:
        write("07_GRILL_CASES.md", label("质询记录", "Grill records"), "\n\n".join(reviews))


def write_atlas(run_dir, envelope, brief):
    """Build in a private staging directory and publish into a fresh runner-owned directory."""
    run_dir = Path(run_dir)
    if run_dir.is_symlink() or not run_dir.is_dir():
        raise ValueError("atlas requires its allocated run directory")
    manifest = check_result(envelope)
    with tempfile.TemporaryDirectory(prefix=".atlas-", dir=run_dir) as tmp:
        stage = Path(tmp)
        visual = stage / "visual"
        visual.mkdir()
        manifest_path = visual / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                                 encoding="utf-8")
        render(manifest_path, visual / "atlas.html")
        write_documents(stage, manifest, envelope["scan"], brief)
        artifacts = list(stage.iterdir())
        for item in artifacts:
            if os.path.lexists(run_dir / item.name):
                raise ValueError(f"run already contains {item.name}")
        published = []
        try:
            for item in artifacts:
                item.rename(run_dir / item.name)
                published.append(item)
        except OSError:
            for item in reversed(published):
                (run_dir / item.name).rename(item)
            raise
