---
name: idea-atlas
description: "Idea Atlas (点子地图). Generate and screen design ideas for a brief or speculative prompt. Explore competing problem readings when the premise leaves the user or decision open. Deliver a reusable set of deep positioning cards, evidence and kill conditions, and an offline HTML map with English and Chinese interface controls for exploring the branches."
license: MIT
metadata:
  version: "1.0.0"
  author: yuyang gong（龚雨旸）
  hermes:
    tags:
      - design
      - ideation
      - positioning
      - divergence
      - atlas
    related_skills:
      - idea-to-positioning
---

# 点子地图 · Idea Atlas

Use for an open design brief, an abstract topic, or a request to explore competing directions before choosing one. The reader can compare, shortlist, or use the ideas to develop another direction. A topic alone is sufficient to begin. Keep run inputs and outputs in the user’s project. Preserve the original brief. Write the scan, ideas, evidence and reviews in the language the user requests. When no output language is specified, use the language the user used to ask for the atlas. Produce one set of project records. The reader can switch the interface between English and Simplified Chinese while reading those records in their original wording.

The standard run delivers an offline HTML canvas by default. Its Markdown cards and decision records remain the editable sources. The base workflow runs independently. For a final positioning defense, an eight-page proposal or a requested deep validation, the companion skill `idea-to-positioning` can take over.

## Dispatch a new brief or a repeat

**Hermes:** For a new atlas or a repeat, save only the literal user brief and explicitly selected materials and run `python3 "/absolute/path/to/idea-atlas/scripts/hermes_run.py" --brief brief.txt --runs atlas-runs` from the project directory, substituting the actual installed script path. Reuse the original brief file on “same prompt again”. The launcher uses the configured Hermes CLI to generate and publishes the worker's raw result. Return the resulting HTML. On failure, report the failed stage and run path. Do not generate replacement cards in the parent chat or substitute an existing result file. If a user explicitly asks to continue a previous card, use the continuation workflow.

**Other hosts:** Use the host agent's existing model access for ideation. The local scripts prepare input and render output. For each new atlas, including a repeat of the same prompt, follow [Agent-run handoff](references/independent-runs.md).

1. Freeze the user's literal design brief and expressly supplied materials with `scripts/agent_run.py prepare`. On “same prompt again”, reuse the original input. Keep the chat's summaries, earlier cards, feedback, run numbers and directions to avoid out of the design prompt.
2. When available, dispatch the prepared task to a **new** host worker with conversation inheritance disabled. In Codex use `spawn_agent` with `fork_turns="none"` when that option is available. Use a different worker on every run. Pass the task verbatim or as the sole task attachment. For long handoffs, use the restricted file transfer described in the reference. Keep previous outputs out of file access and memory where the host supports those controls. The worker interprets the brief and generates, screens and recommends all cards. Repeatedly invoking the skill in the same context does not reset it.
3. If the host lacks fresh-worker support, a new chat can run the prepared task directly. For ordinary ideation the current chat can also generate it; record the actual mode. If an independent repeat was requested and the available chat already holds old ideas, give the user the prepared task for a fresh chat. The capability belongs to the host, not the skill.
4. Preserve the worker's JSON as returned. Use `scripts/agent_run.py finish` to produce the Markdown and HTML. Describe the context actually used if independence matters. A matching task fingerprint checks the handoff text only. Shared workspace access and host-injected memory limit what the skill can establish.

An explicit request to develop a named card, combine runs or apply feedback is a continuation. Use only the named work and write the continuation separately from the original run. Compare frozen runs when requested.

## Choose the starting question

Give the map a specific project title and each direction a distinctive, concrete name as described in `references/generation-protocol.md`. Record the user's words and explicit constraints in `00_BRIEF.md` using `templates/brief.md`. Distinguish supplied facts from your assumptions before naming a product, target audience or venue.

- **Direct exploration.** When the intended problem, decision or commissioned setting is clear enough to start, frame an observable scene and use the six lenses to explore competing interventions. An unusual theme can still have a clear assignment.
- **Reading-first exploration.** When literal acceptance of an imaginative, contradictory or underspecified premise would require inventing the central user, job or reason for value, use `references/reframing.md` first. Keep competing problem readings in the brief. Carry each worthwhile reading into the scan as a separate branch. One world or audience chosen by the agent should not govern them all. Apply lenses selectively after identifying a consequential decision. Honour any scope the user explicitly fixed.

## Scan the relevant decisions

Write `01_SCAN.md` once for the atlas. Use only the source text included in the generation task. When the user asks for public research, collect it separately from the literal brief before freezing the input, or check evidence against the frozen cards afterward. For repeated samples with a shared evidence base, reuse its text unchanged. Tie reading-specific evidence and unknowns to their IDs. Look for existing rituals, cheapest substitutes and their cost or effort, complaints, negative cases and official constraints. Give sources IDs and dates when known. When research is unavailable, label the assumption and identify the evidence needed. Never manufacture interviews, observations, quotes, prices or sales.

## Generate directions

Use `references/lens-deck.md` for the six questions below. In direct exploration, formulate a brief-specific question for each lens and generate in separate batches. In reading-first exploration, start a batch from a reading's insight, reachable audience and decision. Use a lens only if its question helps develop that branch. An idea can follow directly from the reading. Keep the reading ID even when the candidate moves to a different setting.

| Lens | Question to explore |
|---|---|
| Body / embodiment | Which physical action changes? |
| Ritual / moment | When does the intervention happen, and which ritual does it replace? |
| Relationship / role | Who gains or gives up control, responsibility or information? |
| Material / structure | Which physical or interface property creates a different affordance? |
| Service / system | What changes in access, ownership, maintenance or economics? |
| Reverse / extreme | What follows if a defining feature disappears, a goal reverses or an extreme case becomes central? |

Direct exploration normally aims for 18–24 deep cards, typically three per lens. In reading-first exploration, 18 remains a useful overall target for a full atlas. Allocate it according to how many distinct, defensible opportunities each reading opens. Honour the user's requested batch size. Report a shortfall if more candidates would merely repeat earlier cards. A reading may remain visible with zero cards and an open question. Leave promising fragments in `seeds/` and record actual counts. Change the role, moment, object, relationship or constraint when the next idea repeats an earlier premise. If every serious contender is a category variant, record that result and identify a concrete change to the frame or scan, such as adjacent uses, a new material, a technical capability or a business model.

## Write and screen each card

Use `templates/card.md` and `references/quality-contract.md`. Assign a stable ID and a positioning family. The family captures the shared design logic. Compare Who, gap and mechanism to detect paraphrases across lenses. Allow up to two candidates per family. Link further variants and duplicates to the canonical card. Count independent families as well as deep cards.

For each card, keep the following fields usable on their own:

- **Who** includes role, occasion, frequency, current behaviour and relationship.
- **Substitute and gap** name the cheapest existing way to accomplish the job, its cost or effort, and the constraint that changes a real decision.
- **What** includes a single value promise, the mechanism, a proof metric with a threshold, and a tradeoff. Keep a Chinese promise to 15 characters where possible.
- **How** describes the sequence of actions or interactions. Write a short, concrete design action for the canvas node. Two neighbours that look alike should reveal their difference when the reader opens them.
- **Evidence** records what supports the importance of the decision to the user. Assess the evidence for the proposed mechanism separately. Identify source IDs, counterexamples and unknowns. A working mock-up establishes only the behaviour it measures. A documented problem still needs an effective intervention.
- **Reading and insight**, for a reading-first card, identify its reading ID and the tension the original prompt revealed. Trace it into the actual setting, the person who makes the decision, and what they stand to gain or lose. Name the cheapest observation that would show the problem matters or undermine its value. Keep any subsequent mechanism test distinct.
- **Kill** states what observable result would defeat the claim, with a test feasible within two weeks.

Screen for behaviour-defined Who, a named substitute, a decision-changing gap, falsifiability, labelled evidence, a testable kill and duplication. In evidence labels, `green` requires direct support for the exact claim, `yellow` denotes indirect or partial support, and `grey` denotes an assumption. Preserve the distinction between a planned threshold and an observed result.

Write one `cards/<ID>.md` per deep card and collect the index in `02_CANDIDATES.md`. Keep the initial gate status on the card:

- `live` meets the screening criteria.
- `needs-evidence` has adequate structure and a named proof gap.
- `killed` requires a documented hard-gate failure or a recorded grill verdict with its reason. Keep its ID and reason visible, including when it remains valuable as a counterexample.
- `duplicate` and `variant` preserve the canonical link. A raw `seed` remains outside the deep-card count.

Use `03_MAP.md` for the Markdown map or fallback (`references/visual-map.md`). Write `08_IDEA_TABLES.md` for the standard atlas using `templates/positioning-table.md`. Give each idea one complete reading table with Who, behaviour, substitute, gap, promise and mechanism, followed by Proof and Kill. The user may request a different format.

## Grill, shortlist and handoff

For recorded grills use `references/decision-flow.md`. Identify the proposer’s claim, the critic’s strongest objection and the evidence or counterexample considered. Record each round’s actual question, material weighed and judgement. End with continue, narrow, pivot or kill, the reason and the next test where applicable. Store completed rounds in `07_GRILL_CASES.md`. A card with only an initial gate has no completed grill. The number of grill records and verdict distribution follow the run.

Write `04_SHORTLIST.md` using `templates/shortlist.md`. The agent can normally recommend 5–8 directions, subject to the requested scale. For a direct run, look across three or more lenses unless the brief narrows. For a reading-first run, compare the value at stake, the insight carried from the prompt and what the next check can resolve. Record where a tempting prototype has weak evidence of need. Coverage by reading or lens never earns a place by itself. Recommend fewer or none when that is what the evidence supports. Include why each stays, what could kill it and which evidence is missing. A flagged `needs-evidence` card can be recommended with an explicit gap. Until the user chooses, identify recommendations as pending human selection. Display initial gate status, shortlist membership and subsequent grill verdict as distinct facts.

Use `templates/handoff.md` for the 1–3 directions going forward. Put source IDs, open assumptions, kill criteria and the cheapest next evidence step in `05_HANDOFF.md`. Keep the handoff a draft until confirmed. Deliver the complete atlas even if no user selection has arrived. Run the companion workflow for a requested deep validation and retain its verdict and any failed finalist in the atlas record.

## Build the deliverable

Use the packaged renderer for the default HTML. Read `references/canvas-data.md` for the input contract and `references/interactive-tree-flow.md` for the reading order. Copy the original project text into the manifest and preserve IDs, branch references, evidence levels, ranks, proposed thresholds and actual outcomes. Optionally record the language of that text in `manifest.language` when it is clear. The editable manifest contains the current brief, cards, recommendations, handoff and recorded grills. Direct runs group cards by lens. For reading-first runs, export the brief's `readings` keyed by stable ID with `name`, `q`, `premise`, `audience` and `check`. Set each card's `reading`, include its `insight`, and use `lens` when applicable. The resulting canvas groups cards by reading. Use actual project questions, IDs and actions. The included example shows format and behaviour only.

From the directory that contains this SKILL.md, run:

```sh
python3 scripts/render_canvas.py INPUT.json OUTPUT.html
```

Replace the two arguments with the project's manifest path and the desired HTML path. A prepared run writes `visual/atlas.html` inside its unique run directory. The renderer embeds the data in the shipped `templates/atlas-canvas.html`. Use this same template across topics and reruns so the reader can compare maps. When asked to restyle an existing run, render its original manifest into a new HTML file. The resulting HTML can be opened directly or sent by itself. Regenerate from the records after an edit.

Open the HTML in a browser when available. Check the brief, displayed branches and card counts against the records, open an idea via its branch and via the index, switch the interface language with the card open and verify its wording against the same record, check Overview and Validation, compare any Challenges to their source and test filters, zoom and full-map reset. Check a killed card when the run has one. Deliver the HTML link first, followed by brief context or record paths as needed. If the user explicitly requests Markdown only, deliver the records in that format.

```text
atlas/
  visual/
    atlas.html
    manifest.json
  00_BRIEF.md
  01_SCAN.md
  02_CANDIDATES.md
  03_MAP.md
  04_SHORTLIST.md
  05_HANDOFF.md
  08_IDEA_TABLES.md
  cards/
  seeds/                     # raw fragments, if any
  07_GRILL_CASES.md          # completed grill records, if any
```

## Additional modes

- **Compare generation methods.** On an explicit experiment request, use `references/reading-comparison.md` to compare direct-lens generation with reading-first generation at an equal card budget. Everyday runs do not initiate the experiment.
- **All-card validation.** When requested, follow `references/full-run.md` and `templates/dossier.md`. Produce one dossier per card using the shared scan. Record continue, narrow, pivot or kill, the surviving fraction, a sentence deleted or rewritten and the next cheapest test. Update the shortlist, handoff and canvas from the actual verdicts.
- **Detailed evaluation of finalists.** Use `templates/direction-table.md` for `06_DIRECTION_TABLES.md`, including the strongest challenge, missing proof and next test.
- **Single-variable campaign.** Use `references/perturbation-campaign.md`, `templates/base-frame.md` and `templates/run-ledger.md`. Establish a control, then vary one of Who, occasion, job or value per run. Compare against prior winners on Who, gap, mechanism and promise. Mark exhausted variables and stop when further runs repeat existing families. Use `references/constraint-campaign.md` for an explicitly open search across different constraint worlds.
- **Print.** Use `references/process-sheet.md`, `references/decision-flow.md` and `references/visual-map.md` for an explicitly requested static print view. For screen reading, the default canvas already includes the direction index and individual positioning tables (`references/positioning-table.md`).
