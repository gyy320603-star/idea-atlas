# Perturbation Campaign

Use when the user wants to repeat the old skill ten times **without changing the product category or the core user**. The point is controlled variation, not ten different topics.

## Core idea

Fix a base frame. Change **one variable per run**. Let the old skill diverge inside that frame.

The old skill's strength is a stable frame plus 5–8 mechanisms. Changing the entire frame every run destroys that strength.

## Base frame

| Field | Fixed content |
|---|---|
| Category | the same product/service category |
| Who | the same core user, defined by behaviour |
| Occasion | the same primary occasion |
| Job | the same job-to-be-done |
| Substitute | the same cheapest alternative |
| Value | the same primary value (time, dignity, safety, predictability, cost) |
| Constraints | regulation, infrastructure, budget, body, environment |

Write it in `00_BASE_FRAME.md` before run 1.

## Ten runs

Run 1 is the control. Runs 2–10 each change exactly one variable.

For a passenger eVTOL example:

| Run | Changed variable | Frame |
|---|---|---|
| 01 | control | business traveller, airport–city, on-time |
| 02 | Who | first-time passenger, anxiety |
| 03 | Who | wheelchair user, transfer/dignity |
| 04 | Who | older adult + companion, assistance |
| 05 | Who | family with child, luggage/safety |
| 06 | Occasion | island/coastal passenger, ferry disruption |
| 07 | Occasion | night tourism, experience/noise |
| 08 | Job | luggage/transfer, door-to-door |
| 09 | Job | motion sickness/comfort, ride quality |
| 10 | Value | weather/predictability, not speed |

Do not turn operator, regulator, community, or insurer into separate runs. They are **context lenses**: put them into constraints, evidence, and kill criteria.

## Per-run protocol

Each run uses the old skill:

1. Gate 0 Frame — restate the base frame and the one changed variable.
2. Gate 1 Scan — shared evidence base, plus sources specific to the changed variable.
3. Gate 2 Diverge — 5–8 directions inside this frame.
4. Gate 3 Score / Kill — six dimensions; pre-register kill criteria.
5. Gate 4 Evidence — public evidence only; label it.
6. Gate 5 Position — five-field Who, four-field What.
7. Gate 6 Prove — three alternatives + SWOT.
8. Gate 7 Package — **1-page decision brief only**; no 8-page outline for every run.
9. Gate 8 Grill — three rounds; delete or rewrite at least one sentence.
10. Gate 9 Decide — continue / narrow / pivot / kill.

Only the top 3 runs get an 8-page Markdown outline. The other 7 stop at the one-page brief. Packaging is not the test.

## Ledger

Every run appends to `RUN_LEDGER.md`:

| Run | Changed variable | Frame | Selected | Family | Who | Gap | Mechanism | Promise | Verdict |
|---|---|---|---|---|---|---|---|---|---|

Rules:

- A new selected position must differ from prior selected positions on at least **2 dimensions**: Who / gap / mechanism / promise.
- Same family: max 2 selected positions; a third is `variant` or `killed`.
- If all 5–8 directions in a run fall back to an existing family, mark that variable **exhausted**.
- If 8/10 selected positions land in the same family, report convergence and stop. Do not add runs 11–20 to manufacture novelty.
- Do not require ten runs. Five clean variables beat ten paraphrases.

## Output

```
campaign/
  00_BASE_FRAME.md
  01_SCAN.md
  RUN_LEDGER.md
  run01/
    00_BRIEF.md
    02_CONCEPTS.md
    03_SCORECARD.md
    04_DECISION_BRIEF.md
    05_GRILL_LOG.md
  ...
  run03/01_DECK_OUTLINE.md   # only top 3
  PORTFOLIO.md
```

Keep individual runs and the ledger in Markdown. When sharing the resulting atlas, build the default HTML canvas from the portfolio cards and their recorded verdicts.

## Portfolio summary

`PORTFOLIO.md` reports:

- base frame;
- ten frames and the one variable each changed;
- selected position per run;
- independent family count;
- overlap matrix;
- verdict distribution;
- which variables were exhausted;
- top 3 that deserve an 8-page outline.

## Pitfalls

- Changing the whole frame every run is not a campaign; it is ten different prompts.
- Repeating a prompt unchanged uses the independent run entry point. Compare the resulting families after generation if the user requests it.
- Turning stakeholders into runs pulls the work away from the core user.
- Producing ten 8-page outlines is packaging, not quality.
- Counting ten selected positions as ten opportunities when they share one family is fake diversity.
