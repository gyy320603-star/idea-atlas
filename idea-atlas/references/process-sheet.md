# Process Sheet

Use for an explicitly requested print sheet of the divergence and convergence process. For normal screen reading deliver the interactive canvas. The counts below illustrate one run; use the actual card, shortlist, handoff and grill records for the current project.

The atlas sheet answers "what did we find?" The process sheet answers "how did 18 cards become 3, and what was decided at each step?"

Use `references/decision-flow.md` when the user asks why one idea is unreasonable or how it was grilled. The process sheet shows the whole search; the decision flow shows three idea-level paths and their verdicts.

If the user needs to read/zoom the process or says a bitmap is too large, use `references/interactive-tree-flow.md` instead of this fixed sheet.

## Artifacts

Use the current `visual/manifest.json` and Markdown records. The normal reading file is `visual/atlas.html`. Save additional print sheets under separate names such as `visual/process.html` and `visual/process.png`.

## Process sheet layout (A2, 2400×1697)

1. **Header**: title, one-sentence frame, counts: cards / live / needs evidence / shortlist / handoff / killed; a note that the shortlist is an agent recommendation pending human selection.
2. **Process ribbon**: Show how the brief was interpreted, which branches were explored, what the scan supported, and which candidates passed screening or moved forward. Label pending steps.
3. **Diverge matrix**: Use one row per reading in a reframed run or one row per lens in a standard run. Place each actual card in its own branch; row lengths may differ. Each card shows ID, status, title, promise, gap, role, kill, family, score. Do not use 6 tall columns: tall cards leave dead space and make the eye read down instead of across.
4. **Converge column**: Gate (7 checks; live / needs-evidence / killed / families), Shortlist (recommendations with why + kill), Handoff (confirmed IDs), Next (cheapest check per finalist), Sources (actual source IDs).
5. **Bottom strip**: brief notes explaining the observed candidate count, screening, recommendations and confirmed handoff.
6. **Footer**: source-of-truth files; "this is a process, not a decision."

## Data contract

Parse `cards/*.md` frontmatter and body:

- frontmatter: ID, family, originating branch, title, status, evidence and any recorded scores
- body: `Role`, `Promise`, `Decision-changing gap`, `Kill condition`
- `04_SHORTLIST.md`: rank, ID, why, kill
- `05_HANDOFF.md`: confirmed handoff IDs, possibly empty

Counts must be derived, not typed in twice. Every count (cards, live, needs evidence, killed, shortlist, handoff) must match the files; never copy a count from an earlier run.

## Build

1. Build the manifest from cards.
2. Render HTML at fixed `2400×1697`, `overflow:hidden`.
3. Screenshot with Chrome headless:

```bash
"C:/Program Files/Google/Chrome/Application/chrome.exe" \
  --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=2400,1697 \
  --virtual-time-budget=4000 \
  --screenshot="visual/process.png" \
  "file:///.../visual/process.html"
```

4. For 2× use `--force-device-scale-factor=2` and write `process@2x.png`.
5. For chat preview resize with PIL to `1600×1131`.

## Validation checklist

- All actual directions rendered and grouped by their recorded branch.
- Stages correspond to the actual run.
- Shortlist and handoff counts match their records.
- All cards visible; no card hidden because it is not shortlisted.
- Killed is shown as `0 killed` only if true; otherwise keep the kill wall and use the real count.
- Shortlist is labelled agent recommendation, pending human selection.
- Open gaps are named: primary research, prototype, old skill not run.
- Screenshot inspected for overflow, clipped titles, empty panels, and unreadable 7–9px text.

## Pitfalls

- **6 tall columns**: 18 cards become three lonely cards per column with large empty areas. Let the number of rows and cards follow the run.
- **Empty right column**: a shortlist + handoff stack leaves a large blank. Fill it with Gate, Next tests, Sources, and Reading; do not add decorative filler.
- **Decorative funnel**: a funnel without card IDs, counts, or kill reasons is not a process sheet.
- **Hidden killed cards**: the atlas contract says killed cards stay visible. If 0 killed, say so; do not imply needs-evidence cards are killed.
- **Typed counts drift**: derive every count from the manifest; a stale header number destroys trust in the whole sheet.
- **Tiny type**: at 2400px, 7–9px captions are nearly unreadable in print. Keep card body ≥10px, panel body ≥9px, and check at 2×.
- **Mermaid as final**: Mermaid is good for Markdown; it cannot carry card-level status, family, and shortlist rank. Use HTML/CSS for the sheet.
- **Static-only by default**: for 18+ cards or a user who needs to read/zoom, build the interactive tree flow first. Start static only when the target is print.
