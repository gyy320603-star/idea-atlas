# Full-Run Batch

Use when the user asks to run `idea-to-positioning`'s full workflow on **every** atlas card.

The goal is a quality filter, not 18 decks.

## Scope

- One **one-page dossier** per card.
- Gate 0–9; Gate 7 is a one-page decision brief, not an 8-page deck.
- Write the dossiers in Markdown. Rebuild the shared HTML canvas from the updated records.
- Shared `01_SCAN.md`; do not re-research each card.
- Batch 4–6 cards per pass; write each dossier before the next batch.

## Dossier sections

1. Verdict and one-line reason.
2. Gate 0 — frame: category, scene, Who, constraints, confirmed, open.
3. Gate 1 — scan: shared source IDs only.
4. Gate 2 — diverge: the card's family, its sibling cards, and why this card is not a variant.
5. Gate 3 — score: the six scores and total.
5. Gate 4 — evidence: source labels, strongest counterexample, what the evidence cannot prove.
6. Gate 5 — position canvas: Who, substitute, gap, What, How, proof, kill, unknowns.
7. Gate 6 — alternatives: three cheaper alternatives or competitors; short SWOT.
8. Gate 7 — packaging: explicitly say it is replaced by this dossier.
9. Gate 8 — grill: claim, evidence, decision; at least one sentence deleted or rewritten.
10. Gate 9 — decision: continue / narrow / pivot / kill; next cheapest evidence; what would change it.

Use `templates/dossier.md`.

## Verdict rules

- **Continue**: the claim survives the grill and has a cheap next test.
- **Narrow**: the mechanism is real but the claim is too broad; rewrite it smaller.
- **Pivot**: the insight survives, the product form does not.
- **Kill**: a cheaper substitute wins, the behavior does not change, or the evidence does not support the claim.

Do not force a spread of verdicts. Do not rescue a card because its score is high or its rendering is attractive.

## Metrics

Report all four:

- **Continue**: n / total.
- **Narrow**: n / total.
- **Pivot**: n / total.
- **Kill**: n / total.

Then report:

- **Survival rate** = (continue + narrow + pivot) / total. 50–70% is healthy; a higher rate may mean the gates are soft.
- **Direct-continue rate** = continue / total. 20–30% is normal for a full atlas; it is a filter, not a failure.

## Detailed tables

When the user asks for a detailed table per direction, use `templates/direction-table.md`:

- one table per finalist;
- five-field Who and four-field What;
- evidence, kill, strongest challenge, deleted sentence, next test;
- no `…` truncation;
- the summary table is for scanning, not for evaluation.

## Pitfalls

- Do not turn the full run into 18 × 8 pages. That is 144 pages of packaging and no additional evidence.
- Do not keep the pre-run shortlist. Update `04_SHORTLIST.md` and `05_HANDOFF.md` after the verdicts.
- Do not let the atlas score decide the verdict. A high-score card can still die in the grill.
- Do not let a `needs-evidence` card pass as `continue`; it can be `narrow` or `continue with a test`, but the gap must be named.
- Do not write a dossier without a deletion, a decision, and a next test.
- Do not hide killed cards; the kill wall is the output.

## Summary format

`00_SUMMARY.md` should contain:

- verdict counts;
- survival and direct-continue rates;
- a table: ID, title, verdict, strongest challenge, deleted sentence, next test;
- the 1–3 cards that actually enter the next stage.
