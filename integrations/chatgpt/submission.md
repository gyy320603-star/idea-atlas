# ChatGPT plugin validation and submission record

Updated: 18 November 2026

## Current state

The source package and directory copy are prepared. A private development plugin has been created. No public draft upload, review submission or public publication is recorded.

Public submission still requires the intended verified publisher identity and the portal's checks and developer attestations. The author confirmed all available countries and regions on 18 November 2026; `publication.countries` is explicitly `[]`. All four listing URLs were verified publicly accessible with HTTP 200 and the expected page content on that date.

The author confirmed that the current account is intended, but its account-derived display name is not the requested public publisher credit. The intended credit is **yuyang gong（龚雨旸）**. Verify the publisher shown by the portal before public submission; keep the submission as a draft if that credit cannot be resolved. Do not treat the package's author field as proof that the portal will show it.

## Package checks

- Portable root manifest and conventional `skills/idea-atlas/` layout.
- All 35 runtime files match the standalone Idea Atlas 1.0.0 source byte for byte.
- No app bindings, hooks, MCP server, private credentials or host-specific absolute paths are added to the public upload.
- Icon references resolve to packaged files.
- English listing and starter prompts meet the documented length limits; category is `Creativity`.
- Four existing example editions render with the extracted package and retain their embedded records.

The build output includes an archive SHA-256 and a verification JSON. Consult the report beside the exact ZIP being uploaded. These are local checks, not a complete platform schema validation or a passed security review.

## New-brief pipeline test

Executed in Codex on 18 November 2026, with the generation mode accurately recorded as `current-chat` in a child task.

Brief: “Help visitors to a small library leave wet umbrellas and find their own when leaving. We cannot drill into the building.” The test explicitly requested exactly three directions.

Observed result:

- Three original English direction cards and two shortlist recommendations.
- Two recorded desk critiques; all untested evidence remains marked as assumptions.
- `agent_run.py prepare` followed by `finish` completed successfully.
- Raw model JSON was archived unchanged, and the HTML embedded the same card records.
- The brief's English wording and no-drilling constraint were preserved.
- Output HTML: 74,968 bytes; SHA-256 `38736694215c7a24738ef433ed7fcdd02abbbf22cc395b0199414f02413c9359`.

This test does not establish ChatGPT Work execution, browser interactions or download delivery. Those checks remain open. The canonical workflow permits current-chat execution when an independent worker is unavailable; it does not require the Hermes launcher.

## Work acceptance check

Using the saved plugin in ChatGPT Work, run the same brief and verify that the host can read the packaged skill resources, generate original records, execute the renderer and return a downloadable HTML map. Open the map, inspect a card and its challenges, switch interface language, and confirm that the original card text remains unchanged. Record the actual result and the saved release tested.

## Listing links

The website, support, privacy and software-license destinations are in `plugin.json`. All four returned HTTP 200 with expected content in an unauthenticated check on 18 November 2026. The privacy notice is published in this repository. The MIT License supplies the software license terms; it is not a separate publisher-operated service agreement. Confirm any additional policy requirements shown by the submission portal.

## Public review

Skills-only plugins do not require MCP test cases, a demo recording or reviewer credentials. The ZIP includes natural review prompts and initial release notes. Country targeting is explicitly set to all available countries and regions, as selected by the author. The base listing is English; a `zh-CN` translation is supplied for supported submission surfaces.

The developer must complete identity verification and the portal's legal/policy attestations. A saved private plugin does not establish public publishing permission or approval.

yuyang gong（龚雨旸）
