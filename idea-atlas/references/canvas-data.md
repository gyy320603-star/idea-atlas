# 画布数据与生成

每次运行将本项目的 brief、实际采用的读法或视角、卡片、质询、推荐与交接记录汇入 `visual/manifest.json`。使用 UTF-8 JSON。同一张卡在 Markdown、画布、索引和交接记录中使用同一 ID。更新原稿后重新导出并渲染。每次运行都从当前项目取数。

在 skill 目录运行，两个参数依次指向项目的输入数据和 HTML 输出路径。

```sh
python3 scripts/render_canvas.py /path/to/project/visual/manifest.json /path/to/project/visual/atlas.html
```

打开生成的 HTML 即可查看画布和索引，也可以单独转发这个 HTML。

## 映射到界面

| JSON 字段 | 原稿与显示位置 |
|---|---|
| `project.title`、`project.subtitle` | 根节点显示课题标题。用户指定标题时沿用原文，其余情况可把开放的设计问题作为标题。副标题可补充场合或约束。 |
| `readings` | 拆题运行使用。以稳定的读法 ID 为键，至少一项。每项均有 `name`、`q`、`premise`、`audience`、`check` 五个非空字符串，分别为读法名称、值得追查的问题、保留或放开的前提、可接触的决策者及其场合、最低成本的需求核查。读法详情显示这些原始记录。 |
| `lenses` | 以视角名为键，每项含同名的 `name` 和实际提出的问题 `q`。常规运行至少声明一个视角；拆题运行可以省略整组或只提供实际用到的视角。 |
| `cards` | 以稳定卡号为键，卡内 `id` 与键一致。常规运行每张卡必须指定已声明的 `lens`。拆题运行每张卡必须用 `reading` 指向一个读法 ID；如实际用了某个视角，再用 `lens` 指向已声明的视角。 |
| `grill` | 以卡号为键，只收录已有逐轮记录。每项含 `rounds`、`verdict`、`note`，每轮含 `q`（问了什么）、`consider`（权衡了哪些依据）、`decision`（作何判断）。无逐轮记录时使用空对象。 |
| `handoff` | 按交接记录给出卡号数组，尚无记录时使用空数组。界面区分初筛状态、推荐、待交接与质询结论。 |

## 两种分支结构

常规运行省略 `readings`，沿用「课题 → 视角 → 方向」。拆题运行提供 `readings`，画布沿「课题 → 读法 → 方向」串联。可用短 ID（如 `R1`）标记读法。一条读法暂时没有方向时仍显示该分支；如果整轮只产生值得核查的问题，传入 `"cards": {}`，索引会说明目前尚无方向卡。

读法的 `check` 写明可以访问谁、观察哪个已有决定或对照什么记录来验证问题。卡片的 `proof` 与 `kill` 记录设计方案的验证和淘汰门槛。需要说明题目带来的新认识时，用可选的 `card.insight` 写一句话；画布在该卡的定位表中显示。

## 每张方向卡

- `title` 写成读者一眼能区分的短标题，点出这个方向特有的物件、动作或角色变化。用 `action` 再补一句实现细节。效果尚待检验时，标题只写提议的做法。保留完整 `mechanism` 供详情阅读。如有更完整的使用流程，用 `how` 字符串记录。
- 从卡片复制 `family`、`role`、`occasion`、`freq`、`current`、`relationship`、`sub`、`gap`。在 `sub` 中保留替代方案和已知成本，在 `gap` 中写清影响的实际决定。
- `promise`、`mechanism`、`proof`、`tradeoff` 对应价值承诺、实现方式、验证指标、代价。将完整主张放在 `claim`。在 `kill` 中写出会导致放弃或收窄的观察结果。
- `status` 沿用卡片状态。完整卡通常为 `live`、`needs-evidence` 或 `killed`。`duplicate`、`variant` 和 `seed` 使用原标记。用可选的 `statusReason` 记录初筛给出这一状态的实际理由。原始碎片保存在项目的 `seeds/` 中，深卡计数只包含达到深度门槛的方向。
- 有证据记录时，写入 `evidence`（如 `yellow`）和 `evidenceNotes`（字符串，包含来源 ID、依据和限制）。有邻近方向、归并或重复关系时，用 `links` 写明卡号和差别。可提供一段文字或多条非空文字的数组。
- 推荐记录写在卡片的 `short` 对象里，包含 `rank`、`why`、`risk`、`test`。未推荐时省略。只有实际评分时才传 `scores`（`specificity`、`evidence`、`difference`、`feasibility`、`brand`、`fit`，每项 1–5）和总分 `score`。
- 保留未知信息。没有来源或质询记录时，照实标出证据缺口。验证目标、拟开展的测试和实际观察结果应分别表述。

## 原稿与界面语言

项目只需一份正文。用户明确指定输出语言时遵从该要求，否则使用用户提出课题时的语言。源语言清晰时可在 `language` 中写入 BCP 47 标签（如 `fr`、`en-GB`、`zh-Hans`），无法确定时可省略。旧 manifest 如含 `translations`，渲染器使用主记录中的正文。

画布首次打开使用英文界面。点 **English / 中文** 会切换导航、筛选、状态标签和页签。两种界面展示同一份题目、卡片、验证记录及逐轮判断原文。浏览器允许本地存储时会记住界面语言选择。

## 随包示例

[餐边柜示例数据](../examples/sideboard/atlas-data.json) 包含 3 个读法、18 张方向卡和 3 份质疑记录。[离线地图](../examples/sideboard/atlas.html) 可直接打开。

```sh
python3 scripts/render_canvas.py examples/sideboard/atlas-data.json preview.html
```
