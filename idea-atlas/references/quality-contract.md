# Quality Contract

This is the difference between an atlas and a wall of AI ideas.

## Two tiers

| Tier | What it is | What it can claim |
|---|---|---|
| Atlas card | a candidate bet with a claim, substitute, gap, mechanism, evidence status, and kill condition | "worth discussing" |
| Positioning dossier | a card that survived `idea-to-positioning` Gates 0–9 | "worth defending" |

Never promote a card to Tier 2 inside the atlas.

## Depth gate

A deep candidate describes a **multi-dimensional Who** and **What**. In reading-first exploration, add the reading ID and the insight connecting the prompt to a consequential decision for the named audience. Record the strength of evidence that the problem matters separately from the strength of evidence for the proposed mechanism. Identify what observation would make the problem worth pursuing or remove its justification. An unsupported reading can stay in the brief with its open question.

Who:

- Role — what the person is doing in the scene.
- Occasion — the specific moment and place.
- Frequency — how often; the last real occasion.
- Current behaviour — what they do now, including the workaround.
- Relationship — who else is involved and what they expect.

What:

- Promise — one concise statement of what changes for the user. For Chinese, aim for 15 characters or fewer.
- Mechanism — the physical/ritual/role action.
- Proof metric — what changes, measured how, threshold.
- Tradeoff — what gets worse or what the user gives up.

If any field is missing, the card stays in `seeds/` and cannot enter `02_CANDIDATES.md`. A one-line title is navigation, not positioning.

## Family gate

Every card gets a `family`: the shared positioning logic, not the surface theme.

- Max **2 candidates** per family.
- A third card in the same family is `variant` or `killed`.
- Report **independent family count** alongside card count.
- An 18-card atlas with 6 families is not 18 independent opportunities; it is 6 bets with variants.

## Seven checks

### Hard gates (fail = `killed`)

1. **Who is behaviour.**  
   Good: "people who ask a companion to repeat twice per meal."  
   Bad: "young professionals," "design students," "25–35."

2. **Named substitute + cost.**  
   Name the cheapest current behaviour or product, with time, money, or social cost.  
   Bad: "existing solutions are inconvenient."

3. **Decision-changing gap.**  
   The gap changes time, place, object, or behaviour.  
   Bad: "better experience," "more integrated," "more delightful."

4. **Testable kill condition.**  
   Must be executable within two weeks.  
   Bad: "users don't like it."  
   Good: "5 of 8 users refuse to wear it a second time."

### Soft gates (record the evidence gap or link the duplicate)

5. **Falsifiable claim with metric and threshold.**  
   "Reduce repeats from 5 to ≤2 per 10 minutes, while gaze-to-face time drops by ≤20%."

6. **Evidence status.**  
   `green` = a public source or observation directly supports the card's exact claim; `yellow` = a source supports the problem/mechanism, or there is one source/inference; `grey` = assumption.  
   A source that supports the problem space does not make a design concept green. Every card must state its status; no invented evidence.

7. **Non-duplicate.**  
   If a card shares Who + gap + mechanism with another, merge it.  
   More than 70% overlap = `duplicate`, not a new card.

## Status rules

| Status | Meaning | Can be shortlisted? |
|---|---|---|
| `live` | all seven pass | yes |
| `needs-evidence` | hard gates pass; soft gate missing | yes, with a flag |
| `duplicate` | merged into a canonical card | no; use the canonical ID |
| `killed` | hard gate fails | no; keep visible on the kill wall |
| `seed` | raw fragment; depth gate not passed | no; keep in `seeds/` |
| `variant` | same family and mechanism as a canonical card | no; use the canonical ID |

A shortlist without `live` cards is a warning, not a success.

## Shortlist rules

- A full run normally offers 5–8 recommendations for human selection. Use the actual number of worthwhile candidates, including a smaller or empty list.
- In direct exploration, consider breadth across three lenses unless the brief narrows. In reading-first exploration, compare competing readings on real-world stakes, distinct insight and a discriminating next check. Distribute recommendations according to merit.
- Every shortlisted card gets one line: why it stays; one line: what would kill it.
- The agent may cluster and recommend; it must not declare the winner.
- If the human has not selected yet, label the file "agent recommendation — pending human selection" and keep `05_HANDOFF.md` as a draft.

## Quality metrics

Report coverage, duplicate rate, kill specificity and evidence coverage with each atlas. Report full-run, promotion and blind-benchmark metrics when the corresponding evaluations have been performed:

- **Coverage**. In direct exploration, report counts by lens against the standard 18–24-card target. In reading-first exploration, report actual counts by reading, distinct families and unresolved readings against the requested total. A branch can have zero candidates. Evaluate diversity through distinct decisions and mechanisms.
- **Duplicate rate**: ≤20% after clustering. Report mechanical duplicates (merged cards) and semantic overlap separately; one linked duplicate does not prove diversity.
- **Kill specificity**: 100% of cards have a testable kill condition.
- **Evidence coverage**: ≥60% of cards have at least one public source or observed substitute; the rest are explicit `grey`.
- **Survival rate**: (continue + narrow + pivot) / all cards in the full run. 50–70% is healthy; a higher rate can mean the gates are soft.
- **Direct-continue rate**: continue / all cards. 20–30% is normal for a full atlas; do not rescue cards to raise it.
- **Promotion rate**: continue / cards sent to the full run. If the input is already shortlisted, target ≥50%; for a full 18-card run, 20–30% direct continue is acceptable if the kills are well argued.
- **Blind lift**: compared with direct chat, does the atlas improve at least two of: specificity, difference, feasibility, evidence, defensibility?

## Promotion rule

A card is promoted only when:

1. the human shortlists it;
2. `idea-to-positioning` runs its full frame, proof, grill, and decision;
3. the final dossier survives without the atlas rescuing it.

If it dies, log the death in `05_HANDOFF.md`. Do not revive it with a prettier card.

## Optional direct-chat benchmark

On an express comparison request, choose the test that answers the question. To test the effect of interpreting a premise before generating ideas, use [the reading comparison protocol](reading-comparison.md). The workflow below evaluates the whole atlas against direct chat.

Use the same model and the same brief.

- **A**: direct chat, ask for 10 ideas.
- **B**: atlas 18–24 deep cards + human shortlist + `idea-to-positioning` on 1–3.

Ask 5 design students or teachers to blind-rate:

- specificity of the scene;
- difference from substitutes;
- feasibility;
- evidence quality;
- would you defend it in a review?

For this optional benchmark, count a win if B improves at least two criteria. If B is a shortlist of 5–8, require a ≥50% promotion rate; if B is a full 18-card run, require a 20–30% direct-continue rate plus explicit kill reasons. Otherwise, cut the atlas or fix the card gate.

## One-line test

If a reader cannot point to a card and say "this is a bet I had not seen, and here is what would kill it," the atlas has failed.
