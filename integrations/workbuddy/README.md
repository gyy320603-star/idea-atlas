# Idea Atlas for WorkBuddy

在 WorkBuddy 对话中发送：

> 从 https://github.com/gyy320603-star/idea-atlas 安装 Idea Atlas skill，然后用它帮我探索「我的课题」。

作者已实测 WorkBuddy 手机端的链接安装可用。生成使用 WorkBuddy 的模型和任务执行环境；技能本身免费开源，宿主模型用量与订阅按 WorkBuddy 的规则计算。地图内容沿用提问语言，English / 中文 只切换界面。

本目录提供 WorkBuddy 官方市场的提交材料。1.0.0 已于 2026-11-18 提交审核，平台提示预计 7 个工作日内出结果；当前尚未公开上架。提交编号、最终包校验值和后台字段见 [提交记录](submission.md)。

## 构建市场包

在仓库根目录运行：

```sh
python3 tools/package_workbuddy.py
```

Python 3.8+ 即可，无需第三方 Python 库。生成的 `dist/workbuddy/idea-atlas-workbuddy-1.0.0.zip` 只有一个 `idea-atlas/` 根目录，包含技能指令、脚本、参考资料、模板、示例和许可证。市场字段只加入 ZIP 内的 `SKILL.md`。

WorkBuddy 上传校验要求「根目录 / 二级目录 / 文件」，不接受更深的子目录。因此，市场包将自带示例改为 `idea-atlas/examples/sideboard-atlas-data.json`、`sideboard-atlas.html` 和 `sideboard-preview.png`，并只在包内的 `references/canvas-data.md` 更新对应示例链接和命令路径。仓库中的原始目录、技能正文、脚本、模板与示例数据保持不变。

构建会校验必填字段、ZIP 完整性、目录深度，以及仅上述路径适配发生变化；使用解压后的渲染器重建两个中文案例和包内扁平化后的示例，核对嵌入的原文数据。旁边的 `.verification.json` 和 `.sha256` 保存检查结果。该检查验证打包与渲染，不代表新的 WorkBuddy 模型生成测试或平台审核。

## 提交材料

- `skill-metadata.json`：市场中英名称、简介和使用示例。
- `listing.md`：中英详情、推荐用途、Demo 和案例来源说明。
- `assets/idea-atlas-icon-512.png`：沿用现有地图图标的 512 × 512 市场图标；同目录 SVG 是矢量源。
- `docs/media/cow-shoes-zh.png` 与 `docs/media/sideboard-zh.png`（仓库根目录下）：两张中文案例图。

在 [WorkBuddy 开放平台](https://open.workbuddy.cn/) 完成开发者入驻后，创建技能、上传市场 ZIP、完善展示信息并提交审核。以后台实际字段与提示为准。参见[技能包要求](https://open.workbuddy.cn/docs/skill)和[个人认证说明](https://open.workbuddy.cn/docs/onboarding)。

发布后应使用市场安装入口验证：输入课题 → 生成地图 → 点开卡片 → 切换界面语言 → 追溯质疑 → 下载并离线打开。案例图来自 README 标明的 Hermes 历史运行，不作为 WorkBuddy 生成效果证明。

反馈：[GitHub Issues](https://github.com/gyy320603-star/idea-atlas/issues)

yuyang gong（龚雨旸）
