# Idea Atlas for ChatGPT

Idea Atlas turns a design brief into directions, positioning cards, recorded challenges and an interactive offline HTML map. This directory packages the existing skill for the ChatGPT and Codex Plugins Directory.

## Availability

The plugin is being prepared for public submission. A private development copy has been created, but it is not a public installation link or an approved directory listing. The original skill remains available from this repository through the installation methods in the [main README](../../README.md).

The package uses the same Idea Atlas 1.0.0 runtime files as the standalone skill. Content follows the user's request language; the map's English / 中文 control changes interface labels only.

## What is included

- A portable root `plugin.json` with the English listing, Chinese listing translation, starter prompts and review prompts.
- The complete runtime under `skills/idea-atlas/`, including references, templates, rendering scripts and the bundled example.
- The existing map icon and MIT license.

No publisher-operated server, MCP connection or separate Idea Atlas account is required. The host must provide access to the packaged resources, a writable task directory, Python 3.8 or newer, and a way to return generated files. The renderer uses Python's standard library.

## Build

From the repository root:

```sh
python3 tools/package_chatgpt.py
```

The archive, checksum and verification report are written to `dist/chatgpt/`. The builder checks package paths and metadata, confirms that the skill runtime matches the source, and renders the existing English and Chinese examples using the extracted package. These checks establish package consistency; they do not establish host compatibility or public review approval.

## Validation and publication

See the [validation and submission record](submission.md) for the current state. A Codex test with a new brief completed the generation-to-HTML workflow. Execution and file delivery inside ChatGPT Work still need to be tested before claiming Work compatibility.

The [listing](listing.md) documents the intended audience, prompts and historical example provenance. The examples were generated with Hermes and DeepSeek, as credited in the main README. They are not ChatGPT Work test results.

The [privacy notice](privacy.md) describes the packaged workflow and offline viewer. The software is distributed under the repository's [MIT License](../../LICENSE). The AI host's own terms and policies apply separately.

Public submission follows the [OpenAI plugin submission workflow](https://developers.openai.com/plugins/deploy/submission). Upload, review submission and publication are separate steps. The portal's verified developer identity determines the displayed publisher.

yuyang gong（龚雨旸）
