# Interactive tree canvas

Every standard run includes `visual/atlas.html`. Use the bundled renderer and the input contract in `references/canvas-data.md`. The HTML, including its direction index, works from the local filesystem.

## Information hierarchy

1. The root shows the actual project brief. A conventional atlas branches by lens. A reframed atlas branches by the readings of the brief, displaying each reading’s question before any associated cards.
2. Each section shows its branch question followed by a grouped list of ideas. Keep readings whose next step is to investigate the need. Desktop uses quiet connectors between the brief and branches; the narrow layout uses stacked sections. Each row displays its title, design action and initial status and opens by its stable ID.
3. Selecting a lens shows its question and directions. Selecting a reading also exposes its premise, reachable decision owner and initial problem check. Selecting an idea highlights its root-to-branch path and opens its reader. Overview contains the action, use context, insight and full positioning statement. Validation contains the evidence and stopping criteria. Challenges appears when there is a recorded review. Switching the interface language preserves the selected card and tab and displays the same project wording, including each recorded question, decision and reason.
4. Use the direction index to compare scenes and design actions; reframed runs show the parent reading and any lens used. Both reading modes must resolve a card ID to the same detail view.
5. Keep gate status, recommendation, handoff and grill separate. A narrowed idea can have passed the original gate. A recommended idea may still need evidence. Show the reason whenever the run records a kill.

The default canvas supports unbounded panning, cursor-centred zoom and a full-map reset. The template adapts the branches to available screen width. Use the shipped geometry and controls when rendering a new run. Supply content through the manifest rather than editing nodes, counts or paths by hand.

## Content and verification

Populate the brief, lenses, cards, evidence, recommendations and handoff from the current Markdown records. Include a grill only for cards with completed rounds. For each round, preserve its question, what was weighed and its decision. Keep probe metrics distinguishable from measured results. If a card has no completed test or recorded grill, leave the corresponding record empty.

Before sending, verify that the HTML opens offline and that the index and canvas expose the same IDs. Trace a branch, open its positioning table, zoom, pan and return to the full map. Try the status and recommendation filters and inspect any existing kill reason or grill. New runs can have different lens questions, counts, outcomes and handoff IDs.
