# Writing Work-Item State Machine

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

写作工作项必须把总体生命周期、runbook 阶段、质量判断、不可变运行历史和出版状态分开记录。任何一个字段都不能替代其他维度。

## 一、Lifecycle status

```text
intake
  → in-progress
  → under-review
  → approved
  → published
```

不成功或停止的分支：

```text
rejected | cancelled | abandoned | superseded
```

任何终态都可以在记录原因后进入：

```text
archived
```

含义：

- `intake`：任务刚建立，brief 和执行边界尚未完成。
- `in-progress`：research、planning、drafting 或 revision 正在进行。
- `under-review`：事实与 persona/style gate 已通过，编辑审核或编辑退回正在处理。
- `approved`：三个质量 gate 均通过，可进入出版准备。
- `published`：recoverable publication transaction 已成功提交 canonical article、metadata、manifest、state 和 persona indexes。
- `rejected`：编辑明确拒绝，不要求伪造已通过的 gate。
- `cancelled`：因外部决策停止。
- `abandoned`：工作长期停止且不再继续。
- `superseded`：被另一个 work item 取代。
- `archived`：不再活动；必须有非空 `archive_reason`，但不要求此前成功通过 gate。

只有 `approved` 和 `published` 强制 factual、persona/style 与 editorial 三个 gate 全部成功。失败、取消和替代状态必须保留原始工件与失败证据。

## 二、Stage executions

`stage_executions` 由选定的 `writing-runbook-manifest.json` 生成。不同 runbook 可以包含：

- `research-review`
- `scene-authorization`
- `source-text-analysis`
- `semantic-review`
- `second-factual-review`
- `editorial-revision`
- `publication-preparation`

状态：

```text
not-started | in-progress | completed | failed | skipped
```

推荐记录：

```json
{
  "status": "completed",
  "started_at": "2026-07-11T10:00:00+09:00",
  "completed_at": "2026-07-11T10:12:00+09:00",
  "run_id": "run-2026-001-fact-01"
}
```

Required stage 在相关 gate 通过前必须完成；optional stage 可以 `skipped`。脚手架读取 runbook 自动创建阶段，不允许在脚本中维护第二套阶段清单。

## 三、Quality gates

```text
factual_accuracy
persona_and_style
editorial_approval
```

取值：

- `factual_accuracy`：`not-evaluated | pending | passed | failed`
- `persona_and_style`：`not-evaluated | pending | passed | failed`
- `editorial_approval`：`not-evaluated | pending | approved | changes-requested | rejected`

必要关系：

- factual gate 通过要求 `factual-review=completed`；
- persona/style gate 通过要求 `style-review=completed`；
- editor approval 通过要求 `editor-review=completed`；
- `approved` 与 `published` 要求三项 gate 全部通过；
- `published` 还要求完整、typed publication metadata。

## 四、Runbook 与工件

```text
writing-runbook-manifest.json
  → required_stages / optional_stages
  → required_artifacts / artifact_templates
  → create_new_writing_work_item.py
  → staged work-item tree
  → atomic promotion to canonical path
```

脚手架在临时 sibling 目录中生成全部工件；任一模板缺失或渲染失败时，不得留下半成品目录。

Validator 检查：

- state 是否包含所有 required/optional stages；
- required artifacts 是否存在；
- 每个 artifact 是否有真实模板；
- persona/model/runbook/runtime ID 与版本是否解析；
- policy IDs 是否属于 canonical register；
- `writing-runs/` 是否存在。

## 五、不可变运行历史

旧的单一 `writing-run-manifest.json` 已删除。每次执行必须建立：

```text
writing-runs/run-*.json
writing-runs/<run-id>/...
```

每个运行记录固定：

- `repository_commit_sha`；
- derived model、runbook、runtime 的 ID 与版本；
- model identifier 与参数；
- context budget 与工具权限；
- loaded file path 与 SHA-256；
- timestamps、exit status 和 output paths。

验证器使用：

```text
git show <repository_commit_sha>:<loaded-path>
```

读取历史 commit 中的内容并校验 hash，而不是把旧 run 与当前 HEAD 比较。Run ID 必须唯一；输出必须位于 `writing-runs/<run-id>/`；path traversal、未知 commit 和覆盖旧 run 都是错误。

Reference sample 可以保留一个明确的 `run-sample-not-run.json`。Active author lab 不允许 fake not-run record。

## 六、Publication metadata

`publication` 只能是 `null` 或结构化对象：

```json
{
  "publication_id": "publication-2026-001-example",
  "publication_status": "published",
  "canonical_file": "approved-publications/researched-essays/publication-2026-001-example/article.md",
  "published_at": "2026-07-11T12:00:00+09:00"
}
```

`published` lifecycle 必须对应 `publication_status=published`。零出版物由空 `approved-publication-manifest.jsonl` 表示，不使用 Sample B 或其他假记录。

## 七、可恢复出版事务

正式发布只能通过：

```text
publish_approved_writing_work_item.py
```

事务流程：

1. 恢复任何未完成 journal；
2. 获取 repository publication lock；
3. 验证 gates、review stages、final article 与 persona/model version；
4. 在 staging 中准备 article 与 metadata；
5. 预计算新 manifest、work-item state 和 persona indexes；
6. 写 transaction journal 与旧内容 backups；
7. 原子移动 canonical publication；
8. 联合替换 manifest、state 与 indexes；
9. 删除 journal、staging 和 lock。

任何 Python 异常会回滚；进程中断后，下次调用会根据 journal 恢复。CI 还会独立运行 `validate_publication_integrity.py`，检查：

- 没有残留 journal、lock 或非空 staging；
- manifest 与 canonical metadata 完全一致；
- canonical article 与 work-item final 的 SHA-256 一致；
- state linkage 正确；
- persona work/publication indexes 可从 canonical 对象精确重建。

因此，手工复制文章或手改 manifest 不能绕过 publication gate。
