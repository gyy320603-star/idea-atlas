# Constraint Campaign (legacy alternative)

> **Do not use this as the default.**  
> It changes whole constraint worlds, which can drift away from the core user.  
> For the current workflow, use `references/perturbation-campaign.md`: fixed base frame + one changed variable per run.  
> Keep this only for a genuinely open brief where maximal divergence is wanted.

Use when the user asks to repeat the positioning search many times without duplicates, or to compare a constrained search with the same prompt repeated.

The mechanism is **constraint worlds**, not temperature or "be more creative."

## Ten worlds

Each world removes or changes a different assumption. Five seeds per world.

| # | World | What it forces |
|---|---|---|
| 1 | No screen / no voice | ambient, tactile, or silent mechanisms |
| 2 | Two-person use | shared commitment, turn-taking, witness |
| 3 | Public / semi-public | social exposure, venue rules, glanceability |
| 4 | No power / low cost | mechanical, paper, passive mechanisms |
| 5 | No AI at all | removes the answer; tests whether the problem is AI or thinking |
| 6 | Elderly / child | explanation, teaching, family ritual |
| 7 | Institution / venue / school | loaner, policy, group ritual |
| 8 | Privacy extreme | deletion, local-only, anonymity, no record |
| 9 | Only 30 seconds | micro-intervention, delay, one-sentence commitment |
| 10 | Anti-product / refusal | refusal, one-use, deliberate emptiness |

## Protocol

1. Write `00_BRIEF.md` and one shared `01_SCAN.md`.
2. Create `RUN_LEDGER.md` with one row per seed.
3. For each world, generate **5 seeds** across different lenses.
4. Each seed must include: family, Who (role/occasion/frequency), current behaviour, substitute, gap, promise, mechanism, proof, kill.
5. After each world, dedupe against the ledger. Same family: max 2 candidates; the rest are `variant` or `killed`.
6. After ten worlds, write `FAMILIES.md`: family, card count, cards, shared logic.
7. Select **one finalist per family**; target 10 finalists from 12–15 families.
8. Run `references/full-run.md` only on the finalists, not all 50 seeds.
9. Write `DIRECTION_TABLES.md` if the user wants detail per direction.

## Counts

A healthy run looks like:

- 50 raw seeds;
- 12–15 families;
- 10 finalists;
- 20–30% direct-continue after the full run.

Do not report only the seed count. Report **raw seeds, independent families, finalists, and verdict distribution**.

## A/B comparison

- **A**: ten constraint worlds, 5 seeds each → dedupe → 10 finalists → full dossiers.
- **B**: same brief, no constraint world, 10 runs × 5 seeds → dedupe.

Compare:

- independent family count;
- semantic duplicate rate;
- direct-continue rate after the full run;
- whether B produces paraphrases of the same 4–6 families.

If A does not increase family count, the constraint worlds are decorative; fix the worlds before adding more seeds.

If B reselects the same 8/10 positions as the existing pool, that is **convergence, not a failure of effort**. Report the overlap, stop adding runs, and test the survivors. More runs do not manufacture new families; a new frame or constraint does.

## Pitfalls

- For repeated samples of the same prompt, run the independent entry point with identical inputs and keep each original output.
- A constraint world is not a theme. "No screen" must produce ambient, tactile, paper, and silent families, not five light-based cards.
- Do not send all 50 seeds to the full run. That dilutes evidence and turns the grill into ceremony.
- Do not count variants as independent opportunities. A family with five cards is one bet plus four variants.
- Do not truncate the ledger or the direction tables. If a field is too long, link the card.
- Do not produce decks or PDFs. Keep the campaign brief, scan, ledger, families, finalists, direction tables and dossiers in Markdown. Use the default canvas for the resulting atlas.
