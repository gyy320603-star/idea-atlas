# 由现有 agent 运行图谱

在支持 skill 的 agent 中直接给出课题。设计、质询与筛选使用该 agent 已有的模型。下面的命令由 agent 执行。Hermes 使用已配置的 CLI 启动生成任务。分享时通常只需要发送 `visual/atlas.html`。

## 准备题面

把用户给出的设计要求逐字保存为 UTF-8 文本。保留明确给出的约束、数量和语言要求。用户指定的材料按顺序各存一份。原样复跑时复用这些文件，附带的旧稿仅在用户明确选择作续作材料时才带入。

## Hermes 的新图谱与同题重跑

在用户项目目录保存 `brief.txt` 并运行以下命令，`atlas-runs/` 将生成在项目内。把以下命令中的 `SKILL_DIR` 换为含有本 skill 的 `SKILL.md` 的实际绝对目录。Windows 可用 `py -3` 代替 `python3`。

```sh
python3 "SKILL_DIR/scripts/hermes_run.py" --brief brief.txt --runs atlas-runs
```

若 GUI 环境的 PATH 找不到 Hermes，可用 `--hermes "Hermes 启动文件的绝对路径"` 指定同一套已配置的 CLI。

用户指定了材料时追加一个或多个 `--material 文件`。每次执行都新建工作目录，派发相同的固定启动提示，运行 `hermes -z` 并保留宿主的规则加载设置，将 worker 的原始 JSON 交给本地渲染器。聊天里“再跑一次”也执行这个入口。下游选择和合并属于另一次操作。若 worker 异常退出、没有交回合格数据或无法启动，报告失败阶段和运行路径；该轮不生成替代画布。

如用户明确要求 Hermes 忽略其自动加载的规则文件，并且该 CLI 支持此选项，可在启动器命令中追加 `--ignore-rules`。独立运行使用新的进程和工作目录，默认无需该选项。

每次可核对 `worker.json` 中的启动参数、进程记录和原稿摘要，`worker-result.json` 与 `generation.json` 应逐字节相同。相同题面的两轮可以有相同点子。独立进程和独立工作目录能从记录核对，宿主 profile、工具权限以及提供方收到的完整上下文仍由远端 Hermes 控制。

## 其他宿主的手动派发

在用户项目目录运行。将 `SKILL_DIR` 替换为本 skill 的实际绝对目录。脚本会打印这一次的运行目录。

```sh
python3 "SKILL_DIR/scripts/agent_run.py" prepare --brief brief.txt --runs atlas-runs
```

资料用可重复的 `--material source.txt` 传入。每一轮都单独执行 prepare。`task.txt` 包含固定的设计与输出规则、当前题面及指定材料，不含运行编号、历史卡片或工作目录。此前出过一个相同的方向，也照常保留并评价。

## 选择生成上下文

- **宿主支持无历史子任务。** 每轮新建一个子任务，显式关闭父聊天继承。在提供这个选项的 Codex 中，调用 `spawn_agent` 并明确指定 `fork_turns="none"`。保持宿主模型设置一致，将 `task.txt` 全文原样作为任务正文，或作为唯一的任务附件。让子任务直接交回完整 JSON，一轮结束后用新子任务开始下一轮。
- **只能通过文件交接长文本。** 可以限定子任务只打开指定的 `task.txt`，只将最终 JSON 写到指定的新文件，不列目录、不读取其他文件。传输用路径独立于题面。能限制工具或文件访问时，在宿主中设置该限制。记录发生了文件交接；若看到子任务访问了旧稿，丢弃这份生成并从原始题面重新派发。
- **宿主没有独立子任务。** 普通出图可由当前 agent 按任务正文直接执行。用户明确要求独立重跑、当前聊天已有旧答案时，将 `task.txt` 交给用户，在一个新的非分叉聊天中以它作为设计任务。新聊天如可配置，使用空工作目录、关闭可能带入旧稿的记忆，再交回结果。

需要复核的实验可在每个结果目录单独记下宿主给出的子任务 ID、历史继承设置，以及可见的文件访问记录。这里记录实际采取的运行方式。无历史子任务解决父聊天的继承，宿主仍可能提供系统指令、共享工作区、文件工具或长期记忆。使用者可以核对本轮交给 agent 的正文；工具权限与模型实际接收的完整上下文由宿主决定。

## 交回图谱

将 agent 原样交回的 JSON 放到独立的临时文件，例如 `result.json`。以下命令的 `RUN_DIR` 使用 prepare 打印的目录。文件整理与渲染均在本地完成。

```sh
python3 "SKILL_DIR/scripts/agent_run.py" finish --run RUN_DIR --result result.json --mode fresh-worker
```

将生成者返回的原始 JSON 直接交给 finish。界面文字由画布模板提供，一份项目原稿即可出图。

`fresh-worker` 表示由未继承历史的新子任务生成，`fresh-chat` 表示在新聊天中生成，`current-chat` 表示使用当前聊天。模式由派发方填写。缺字段或 JSON 被截断时，把具体错误交回本轮生成者修复，避免整理者根据其他轮的卡片补全。把 `visual/atlas.html` 链接交给用户。

运行目录保留 `task.txt`、生成结果和 `receipt.json`。两轮的任务正文摘要相同，说明交接的设计输入相同。若用户明确要对照，在原稿封存后使用 [比较流程](reading-comparison.md)。
