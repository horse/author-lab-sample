# Writing Work-Item State Machine

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

写作工作项不再用一个 `status` 字段同时表达“整体生命周期”“runbook 阶段”和“质量审核”。这三个维度必须分开记录。

## 一、Lifecycle status

`lifecycle_status` 表示工作项在整个生产过程中的总体位置：

```text
intake
  → in-progress
  → under-review
  → approved
  → published
  → archived
```

- `intake`：任务已创建，brief 尚未完成。
- `in-progress`：research、planning、drafting 或 revision 正在进行。
- `under-review`：事实与 persona/style gate 已通过，编辑审核正在进行；或者编辑已经要求修改。
- `approved`：事实、persona/style 和编辑三个 gate 均通过，最终稿可进入出版准备。
- `published`：publication transaction 已成功写入 canonical publication、metadata、manifest 和 state。
- `archived`：任务不再活动，但所有历史工件、审核和运行记录继续保留。

编辑退回不需要恢复旧式 `planned` 或 `drafted` lifecycle。具体回退目标由 `stage_executions` 表示，例如把 `research`、`planning`、`drafting` 或 `editorial-revision` 重新标记为 `in-progress`，并在编辑审核文件中记录理由。

## 二、Stage executions

`stage_executions` 来自选定的 `writing-runbook-manifest.json`。每个 runbook 可以拥有不同阶段，例如：

- `research-review`
- `scene-authorization`
- `source-text-analysis`
- `semantic-review`
- `second-factual-review`
- `editorial-revision`

每个 stage 使用：

```text
not-started
in-progress
completed
failed
skipped
```

可选 stage 可以是 `skipped`，但 required stage 在进入相关 gate 前必须 `completed`。新 work item 由脚手架读取 runbook 的 `required_stages` 与 `optional_stages` 自动建立 stage 记录，不允许手工维护另一套阶段清单。

推荐的 stage record：

```json
{
  "status": "completed",
  "started_at": "2026-07-11T10:00:00+09:00",
  "completed_at": "2026-07-11T10:12:00+09:00",
  "run_id": "RUN-2026-001-FACT-01"
}
```

真实运行时应记录 `run_id`；sample 可以省略时间和 run ID。

## 三、Quality gates

`quality_gates` 只有三项：

```text
factual_accuracy
persona_and_style
editorial_approval
```

它们不是“某一步运行过”，而是独立判断：

- `factual_accuracy`：`not-evaluated | pending | passed | failed`
- `persona_and_style`：`not-evaluated | pending | passed | failed`
- `editorial_approval`：`not-evaluated | pending | approved | changes-requested | rejected`

必要关系：

- `factual_accuracy=passed` 要求 `factual-review` stage 为 `completed`；
- `persona_and_style=passed` 要求 `style-review` stage 为 `completed`；
- `editorial_approval=approved` 要求 `editor-review` stage 为 `completed`；
- `under-review` 及以后要求 factual 和 persona/style 已通过；
- `approved` 及以后要求 editor 已批准；
- `published` 要求 publication metadata 已写入 state。

## 四、Runbook 与工件

Runbook 是 stages 和 required artifacts 的唯一权威来源：

```text
writing-runbook-manifest.json
  → required_stages / optional_stages
  → required_artifacts / artifact_templates
  → create_new_writing_work_item.py
  → work-item-state.json + 完整工件目录
```

validator 会检查：

- state 中是否包含 runbook 的所有 required/optional stages；
- work-item 目录是否包含所有 required artifacts；
- runbook 中每个 required artifact 是否有 template；
- template 路径是否真实存在；
- policy rule ID 是否在 canonical policy register 中存在。

## 五、不可覆盖原则

- `draft-01.md` 完成后不得覆盖；后续版本使用 `draft-02-after-review.md` 等新文件。
- `writing-run-manifest.json` 应记录每次实际运行；多次运行时不得用最后一次结果覆盖早期失败记录。
- factual/style/editor review 的新一轮结果应保留历史或使用明确的新文件名。
- 失败、回退和排除必须记录，不能通过删除工件伪造顺利流程。

## 六、出版事务

`approved` 只是允许进入出版准备，不等于已经出版。

正式发布必须通过：

```text
publish_approved_writing_work_item.py
```

事务将验证：

1. factual gate 通过；
2. persona/style gate 通过；
3. editor approval 为 approved；
4. 三个审核 stage 已完成；
5. `final-approved-article.md` 存在且非空；
6. work item 使用的 persona/model ID 与版本仍然匹配；
7. publication category、ID、status 和 metadata 合法；
8. canonical 文件写入成功；
9. publication manifest 重建成功；
10. work-item state 更新成功。

中间失败时应回滚 canonical 目录、manifest 和 state，避免半发布状态。
