# Positioning Table

Use one positioning table per idea in the standard atlas. Open the same table from either a canvas node or its direction-index entry.

## Why this table

A card is good for divergence; a table is better for reading a single positioning. The six rows force the reader to see the same structure for every idea:

1. **Who** — role + occasion + frequency, behaviour-defined.
2. **行为** — what they do now, including the workaround.
3. **现有替代** — cheapest substitute, with cost/effort.
4. **空位** — the decision-changing gap, not a feature gap.
5. **What** — one concise promise. For Chinese, aim for 15 characters or fewer.
6. **How** — the mechanism that delivers the promise.

Below the table:

- **Proof** — metric + threshold.
- **Kill** — testable kill condition.

## Output contract

For a standard or reframed atlas with candidate cards, write `08_IDEA_TABLES.md`:

- one table per idea, in card order;
- header line with status, family and the originating branch. Include a lens, score and recommendation rank when recorded. For a reframed card, include the insight that connects the brief to this decision;
- same six rows in the same order for every idea;
- Proof and Kill directly below each table;
- no ellipsis, no merged cells, no giant wide table.

Use `templates/positioning-table.md`.

## HTML reading view

The default `visual/atlas.html` opens on the tree. Its index lists the current directions; selecting an idea in either view opens the positioning table, followed by the card’s recorded tests and judgements. The manifest must preserve the actual scene, behaviour, substitute, gap, promise and mechanism for every card. For any completed grill, include its question, the evidence or counterexample weighed, and its decision.

## Relation to other tables

- `templates/direction-table.md` is a finalist evaluation table with evidence, strongest challenge, and next test. Use it when the user asks for a full evaluation.
- `templates/positioning-table.md` is a reading table for one idea. Use it when the user asks "what is this idea's positioning?"
- The interactive HTML drawer should show the same six rows, then the grill rounds, so the table and the visual do not diverge.
