# Decision Flow

Use the grill record format below for the interactive card drawer. The fixed-page layout is a separate print option. Its numbers and statuses illustrate one run; use actual records for the current brief.

A decision flow is not a prettier funnel. It shows **idea-level paths** through the same gate and grill. The atlas/process sheet answers "what did we find?"; the decision flow answers "why did this idea live, narrow, or die?"

If the user asks for a traditional line-connected mind-map, clean vector lines, or says the swimlanes read as a tidy dashboard, use `references/interactive-tree-flow.md` instead. Do not force three swimlanes.

The 18-card print layout below is a standard-run example. Use the actual branch labels, card IDs and counts for a reframed run.

## Preconditions

- For a grill-based kill, record the actual three rounds (claim, evidence, decision) in `07_GRILL_CASES.md`. A hard-gate failure can also kill a card. Show that gate and its reason without inventing grill rounds.
- If no card is killed, show `0 killed` and use a `narrow` lane. Do not invent a kill for visual balance.
- If a card is killed, update its status, the manifest, and every count on every sheet. A stale `0 killed` is a data bug.
- A killed card stays visible and keeps its reason. "Killed as standalone, kept as counterfactual" is a legitimate verdict: it removes the product claim but preserves the learning.

## Layout (2400×1450, landscape)

1. **Header**: title, one-sentence frame, counts (`18 ideas / 7 live / 10 needs / 1 killed / 6 shortlist / 3 handoff`), and the note that the shortlist is an agent recommendation.
2. **Macro flow**: six nodes across the page — Prompt → Interpretations or frame → Generate → Screen → Shortlist → Handoff. Put one count and one reason under each node.
3. **Idea swimlanes** for recorded cases; possible outcomes include:
   - continue (green);
   - narrow (amber);
   - kill (red).
   Each lane is a horizontal sequence:
   `idea → gate → R1 claim → R2 evidence → R3 decision → verdict`.
4. **Card index**: Include every idea with its ID, title, status and any recommendation rank.
5. **Bottom**: three short reason panels — why the kill is unreasonable, why the narrow is not a product, why the continue survives — plus a small grill-rules strip (`R1 claim / R2 evidence / R3 decision`).
6. **Footer**: source of truth (`cards/*.md`, `07_GRILL_CASES.md`, shortlist, handoff) and "a flow is not a decision."

## Grill card content

Each round is one card, not a paragraph. Every round must record three fields:

- **question**: what was actually asked. One sentence, in the critic's voice.
- **considered**: the substitute, constraint, evidence, or counterexample that was weighed; this is the reasoning, not the conclusion.
- **decision**: continue / narrow / pivot / kill, plus why.

Round labels:

- **R1 / CLAIM**: the strongest critic question. "Is this just a feature?"
- **R2 / EVIDENCE**: the one constraint or missing proof that could kill it.
- **R3 / DECISION**: what was actually decided, plus the next test.

A one-line critic is not a grill; it is a verdict with no reasoning. If the drawer or sheet cannot show `question → considered → decision`, the grill is incomplete.

A verdict card carries: `continue / narrow / pivot / kill`, the one-line reason, and where the idea goes next (old skill, another card, counterfactual, or nothing).

## Visual grammar

- Green = continue; amber = narrow; red = kill; grey = needs evidence.
- Arrows carry a label: `pass`, `grill`, `verdict`. An unlabelled arrow is decoration.
- Keep killed cards visible. A kill wall with one named card and a reason is stronger than a clean wall with no judgement.
- Do not draw 18 lines across the page. Use three exemplar lanes plus the all-18 index; 18 lines become spaghetti.
- For an interactive map, use the bundled brief → reading or lens → idea canvas. Gate, shortlist and grill outcomes stay attached to their corresponding ideas.

## Layout pitfalls

- **Tall empty nodes**: do not stretch three nodes to fill the page. Use compact lanes (≈160–190px) and fill the remaining height with the all-18 index and reason panels.
- **Tiny type**: 7–9px captions are unreadable in print. Keep node body ≥9px, verdict ≥11px, and inspect at 2×.
- **Three lanes, no all-18**: the exemplars become the whole story. Keep the complete index visible.
- **Fake decisiveness**: a kill drawn without a grill record is a lie. Either grill a real counterfactual or keep zero killed.
- **Stale counts**: after a status change, regenerate the manifest and every sheet; header, gate, and bottom notes must agree.

## Build

For a dynamic/zoomable deliverable, build the interactive tree flow and do not screenshot: `references/interactive-tree-flow.md`.

For a print-only decision flow:

1. Build `manifest.json` from the actual branches, cards and recorded decisions.
2. Render `decision_flow.html` at fixed `2400×1450`; CSS grid for macro, lanes, all-18 index, and reasons.
3. Screenshot with Chrome headless:

```bash
"C:/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=2400,1450 \
  --virtual-time-budget=4000 \
  --screenshot="visual/decision_flow.png" \
  "file:///.../visual/decision_flow.html"
```

4. For 2× use `--force-device-scale-factor=2`; resize a 1600px preview with PIL for chat.

## Validation

- Each lane corresponds to an actual recorded case.
- Each lane shows the recorded rounds and their outcome.
- Every verdict has a one-line reason and a next destination.
- The index contains every actual card; killed card is visible and red.
- Counts match `manifest.json`; killed count is derived, not typed.
- Screenshot inspected for clipped text, empty panels, and unreadable type.
