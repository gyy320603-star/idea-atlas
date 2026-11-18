# Idea Atlas — ChatGPT directory materials

Prepared on 2026-11-18. This file contains proposed listing copy and submission notes. It is not evidence of publication, review approval, or a completed ChatGPT Work test.

## Identity and display fields

| Field | Value |
| --- | --- |
| Plugin name | `idea-atlas` |
| Display name | Idea Atlas |
| Version | 1.0.0 |
| Author | yuyang gong（龚雨旸） |
| Category | Creativity |
| English subtitle | Explore and compare ideas |
| Chinese subtitle | 把课题展开成可探索的想法地图 |
| Source | https://github.com/gyy320603-star/idea-atlas |
| Website and interactive examples | https://idea-atlas-demo.sturdypalm7.chatgpt.site/ |
| Support | https://github.com/gyy320603-star/idea-atlas/issues |

Use the publisher identity selected and verified in the submission portal. The package author credit does not establish the portal's verified developer name.

## English directory description

Turn a design brief into an interactive map of possibilities you can inspect, compare and discuss.

Idea Atlas helps design students, educators and teams explore ideas before choosing what to prototype. Start with a topic, or add research notes, sketches and constraints. It examines different readings of an open brief and develops directions into cards: who might use the idea, what they do today, why they might switch, how the proposal works, and what tradeoffs it introduces.

Browse the branches, compare ideas in a list, or filter to a shortlist. Open a card to examine evidence, assumptions, a proposed test and a result that would rule it out. Cards that have been challenged also preserve the question, the material considered and the resulting decision.

You receive an HTML map that opens offline and can be shared as one file, plus editable Markdown records and JSON data. Ask to continue a card by its ID when you want to develop a direction further.

Use it for product and industrial design briefs, service and interaction concepts, speculative design exercises, or comparing ideas from a workshop. A topic alone is enough to start; ideas generated without research are hypotheses to investigate, and shortlist recommendations remain yours to judge.

Content follows the language of your request unless you specify another. The map interface starts in English and supports English / 中文 switching. This changes interface labels while preserving the original brief, cards and review records.

Created by yuyang gong（龚雨旸）.

## English starter prompts

1. Explore “running shoes for a cow.” Compare interpretations, challenge the ideas, and create an interactive map.
2. Explore moving breakfast prep from a small kitchen to a sideboard. Compare tradeoffs and propose tests.
3. Turn my uploaded workshop notes into an idea map. Group similar directions and show what to test before prototyping.

The third prompt requires the user to supply their notes. The first two can begin with the prompt alone.

## Chinese directory description

把一个设计课题展开成可点开、比较和讨论的想法地图。

Idea Atlas 面向设计学生、教师和设计团队，用于设计前期的发散、比较和筛选。只有一个题目也能开始；有调研笔记、草图和限制条件时，可以一起提供。它会探索开放命题的不同读法，将设计方向写成定位卡：谁会用、现在怎么做、为什么愿意换、方案如何起作用，以及要付出什么代价。

沿着地图看分支，切到清单比较方向，或筛选入围方案。点开卡片，可以查看已有依据、待验证的假设、下一步测试和放弃条件。完成过质疑的卡片还会保留问题、考虑过的依据和最后的判断。

交付物包括可离线打开、单文件分享的 HTML 地图，以及便于继续修改的 Markdown 记录和 JSON 数据。看中某个方向后，直接报出卡片编号，就能继续发展它。

适合产品与工业设计、服务与交互设计、开放命题与设计教学，也可以整理工作坊里的已有想法。仅凭题目生成的内容用于提出假设和安排验证，入围推荐由你判断和选择。

内容沿用提问语言，也可以主动指定。地图界面默认英文，支持 English / 中文 切换；切换只改变界面文字，保留课题、卡片和质疑记录的原文。

作者：yuyang gong（龚雨旸）。

## Chinese starter prompts

1. 探索「给牛穿的一双跑鞋」。比较题目的不同读法，质疑各个想法，生成可点开的想法地图。
2. 探索「小厨房家庭的早餐准备能否移到餐边柜」。比较不同方向的代价，并提出验证方法。
3. 把我上传的工作坊笔记整理成想法地图。归并相近方向，说明做原型前应该验证什么。

## Example gallery captions

**Running shoes for a cow.** Five readings, 18 ideas and seven shortlisted cards. Open C01 to follow the challenges to a hoof-print running shoe and the separate tests they prompted.

- [English edition](https://idea-atlas-demo.sturdypalm7.chatgpt.site/cow-shoes/en.html)
- [Chinese original](https://idea-atlas-demo.sturdypalm7.chatgpt.site/cow-shoes/zh.html)
- Image, relative to the repository root: `docs/media/cow-shoes-en.png`.

**A second prep station in the dining room.** Four readings, 18 ideas and six shortlisted cards. Open A01, “Breakfast Station,” and select Challenges. Crumbs, steam and who wipes the counter narrow the proposal to a 40 cm breakfast module with a washable tray.

- [English edition](https://idea-atlas-demo.sturdypalm7.chatgpt.site/sideboard/en.html)
- [Chinese original](https://idea-atlas-demo.sturdypalm7.chatgpt.site/sideboard/zh.html)
- Image, relative to the repository root: `docs/media/sideboard-en.png`.

**Provenance to retain beside these examples:** Both cases were generated in Chinese with Hermes and DeepSeek V4.1 Flash 1017, using Idea Atlas 0.14.1 for cow shoes and 0.13.0 for the sideboard. They use the 1.0.0 viewer; the English editions are separate translations. Tests in the cards are proposals. These examples show the workflow and interface; they are not ChatGPT Work test results.

## Release notes

Initial ChatGPT plugin package for Idea Atlas 1.0.0. Bundles the design exploration workflow, supporting references, templates and offline HTML renderer, with English and Chinese interface controls.

## Submission notes — not directory copy

- This is a skills-only package. It does not require a publisher-operated MCP service or a separate plugin account.
- Runtime: the host provides model access, file handling and Python 3.8 or newer. The renderer uses Python's standard library. A package render check alone does not establish ChatGPT Work compatibility.
- Existing Hermes examples must retain their provenance. Use actual ChatGPT Work output for any claim about Work performance.
- The proposed privacy text is in `privacy.md`. A local file is not a published policy URL. Publish and verify the final privacy and terms pages before marking submission materials complete.
- The public listing must not claim official endorsement or include price promotions. An official directory listing, if approved, does not imply a recommended placement.
- The portal's country targeting and verified publisher identity must match the developer's chosen settings; this draft does not invent those declarations.

yuyang gong（龚雨旸）
