# Idea Atlas privacy notice

Last updated: 18 November 2026

Publisher: **yuyang gong（龚雨旸）**

This notice describes the Idea Atlas skills-only plugin and its generated offline HTML maps. It explains the plugin's own data handling separately from the AI service in which you use it.

## What the plugin does with your material

Idea Atlas uses your design brief and any materials you choose to provide, such as project constraints and research notes, to generate design directions, comparison records, proposed tests and a map. These materials may contain personal information if you include it. The plugin does not require personal information to explore a design topic.

The workflow runs through your host AI service and its execution environment. In ChatGPT Work or Codex, OpenAI processes the conversation, uploaded material and generated files according to the terms, privacy information and account or workspace settings that apply to your use. See [OpenAI's privacy policy](https://openai.com/policies/privacy-policy/), including the regional version applicable to you. A school or employer may also control settings in a managed workspace.

The plugin consists of packaged instructions, references, templates and scripts. It has no publisher-operated processing server, account system or MCP connection. Its normal workflow does not send your briefs, uploaded materials or generated maps to the publisher. The rendering scripts and generated HTML viewer contain no publisher analytics or tracking requests.

## Files and browser storage

The workflow saves the supplied brief, selected material, model-generated records and output files in the host's task or project environment. This includes Markdown records, JSON data and the HTML map, as well as technical run receipts such as file hashes and the declared generation mode. These records support continuation and reproducible rendering; they are not sent to the publisher by the packaged scripts.

The generated HTML contains the map's brief and card records so it can open offline. Anyone you share that file with can read its embedded content. The plugin does not publish your map automatically.

The viewer stores your English / 中文 interface preference in the browser's local storage under `idea-atlas.language`, when the browser allows it. That setting contains only the selected interface language. It is kept in that browser and is not an analytics identifier. You can remove it using the browser's site-data controls; availability and behavior can differ when opening local files.

## Retention and deletion

Idea Atlas does not maintain a publisher-side database of your projects. The packaged workflow does not set a retention period for your project files: they remain in the task or project environment until removed by you or that environment's retention process. Host-service conversations, files, logs and backups follow the host's retention rules and your applicable account or workspace settings.

Use the host's available controls to manage conversations and hosted files, and delete downloaded maps or records from your own storage when you no longer need them. Clearing the browser's local storage removes its saved interface preference. Deleting a file or conversation in one place does not remove copies you have downloaded or shared elsewhere.

## Support and public feedback

Support is available through [Idea Atlas GitHub Issues](https://github.com/gyy320603-star/idea-atlas/issues). Opening an issue is optional. If you post one, the publisher and other visitors can see your GitHub username, issue text and any attachments you choose to share. The publisher uses that material to understand feedback, answer questions and investigate problems.

Issues in this repository are public. Use a minimal example without private project material or personal information. GitHub hosts the issue and controls its storage and platform-level processing under [GitHub's privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). Closing an issue does not delete its content. Use the content-management options available to you on GitHub, or request help through the issue tracker without reposting sensitive information. Removal from the repository cannot guarantee removal of copies made by others.

## Other services and hosts

Opening the public example website, source repository or support page involves the hosting service for that page; this notice does not replace that service's privacy information. If you separately ask your AI host to browse, connect a service, upload or publish material, the host and the selected service handle those actions under their own settings and policies.

The source project also supports other AI hosts. An optional Hermes launcher is intended for a separately configured Hermes environment and is not required for the ChatGPT workflow. If you choose to use another host, its model provider and execution environment handle your input according to their own policies.

For questions about the plugin's data handling, use [Idea Atlas GitHub Issues](https://github.com/gyy320603-star/idea-atlas/issues). Do not include private data in a public issue.

yuyang gong（龚雨旸）
