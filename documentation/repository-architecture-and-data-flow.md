# Repository Architecture and Data Flow

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本仓库把真实证据、研究解释、可执行模型、派生作者、具体任务、不可变运行、实验、审核和出版分成不同的权威层。分层的目的不是增加文件数量，而是让每条结论、每次生成和每个出版决定都能追溯并独立验证。

## 一、主数据流

```text
source-author materials
  → normalized text + versioned segment map
  → author-scoped evidence-backed research claims
  → source-author model + author-scoped provenance
  → derived-author lineage and derivation profile
  → exact-version derived-author executable model
  → work item + selected runbook + selected runtime
  → immutable commit-pinned writing runs
  → factual gate + persona/style gate + editor approval
  → recoverable publication transaction
  → canonical publication
```

任何下游工件都不得静默修改上游层：

- 生成文章不能证明源作者具备某种特征；
- 一个 source author 的 claim/model 不能引用另一个 source author 的 segment/claim；
- publication 不能自动写回 source-author research 或 source-author model；
- 一个派生作者的 memory 不能自动进入另一个派生作者；
- runtime adapter 不能决定作者身份、议题或文风；
- presentation site 不能反过来决定研究和出版目录。

核心边界由 `POLICY-PROVENANCE-001`、`POLICY-DERIVATION-001`、`POLICY-FACTUALITY-001`、`POLICY-ORIGINALITY-001`、`POLICY-PUBLICATION-001` 和 `POLICY-HELDOUT-001` 统一编号。

## 二、控制平面

根级 `author-lab-project-manifest.json` 是仓库机器入口。它声明：

- repository mode 与 readiness status；
- source author、source model、persona 目录；
- harness、runtime、work item、evaluation、experiment 与 publication 目录；
- component、placeholder、storage、schema、persona template 和 policy register。

验证器从 manifest 发现对象，不硬编码 Sample A/B/C 名称。Persona generator 创建新 persona 时，必须同时更新：

```text
author-lab-project-manifest.json
repository-component-status-register.json
```

未注册 persona directory 与声明后缺失的 persona 都会失败。

`repository-component-status-register.json` 分开记录：

```text
component_class
implementation_status
validation_status
production_ready
real_content_status
experimentally_validated
```

所以基础设施可运行不代表真实内容或真实实验已经完成。

## 三、Repository mode

`repository_mode_support.py` 为所有 generator 提供同一模式合同。

### `reference-sample`

- 生成带 marker 的示例工件；
- 可以使用明确的 sample status；
- 可以保存 reference-only not-run 示例；
- 真正为空的 canonical JSONL 仍保持空文件。

### `active-author-lab`

- 生成无 marker 的 production-shaped records；
- 不允许 sample status、fake checksum、`SAMPLE-*` ID；
- 空 run/evaluation/publication 直接为空，不建立假对象；
- placeholder 只能存在于 register 明确登记的路径。

CI 会同时检查 marker 和更广义的 sample sentinel。

## 四、资料与规范化层

源资料首先进入：

```text
source-corpus-manifest.jsonl
source-rights-register.jsonl
source-material-storage-and-ingestion-register.jsonl
```

三者必须使用同一个 `source_id`，并对 storage URI、rights status、checksum 和 segmentation version 保持一致。

版权材料默认保存在：

```text
private-storage://source-author-id/source-id
```

仓库只保存登记、checksum、rights、规范化输出和定位关系。允许提交的公开材料可以使用 `repository-storage://`。

每个 segment 绑定：

```text
source_id
edition_id
segmentation_version
segment_ordinal
content_sha256
```

重新分段必须提升 segmentation version；新的分段命名空间与旧版本分开。

## 五、Author-scoped research 与 provenance

每条 research claim 必须声明 `source_author_id`。Validator 为每位 source author 分别建立：

```text
segment index
claim index
source-model provenance index
```

规则：

- claim 只能引用同一作者的 segment；
- model rule 只能引用同一作者的 claim；
- approved model rule 只能引用 accepted claim；
- provenance record 必须声明正确的 source author 和 source model ID。

因此“某个 ID 在仓库里存在”不再足以通过；其 ownership 和 status 也必须正确。

## 六、机器合同执行

`document-schema-registry.json` 将 path pattern 映射到 schema。执行顺序为：

```text
JSON/JSONL syntax
  → registered JSON Schema validation
  → semantic and cross-reference validation
  → specialized provenance/run/publication validation
```

生产型机器文档如果没有 schema registration，也没有明确分类为 schema definition 或 artifact template，CI 会失败。

跨引用验证进一步检查：

- source、rights、storage、normalized text 与 segment map；
- author-scoped research claims 与 source-model provenance；
- source model、persona、derived model 的 ID 和版本；
- runbook stages、artifact templates 和 policy IDs；
- work item 的 persona/model/runbook/runtime；
- exact-version experiment conditions；
- publication、canonical article、state 与 persona indexes。

## 七、原子脚手架

`atomic_repository_update.py` 提供：

```text
staged sibling directory
atomic directory promotion
multi-file replacement with rollback
```

### Work item

```text
runbook manifest
  → stages
  → required artifacts
  → artifact templates
  → staged work-item tree
  → atomic promotion
```

### Persona

```text
project-declared source model + exact version
  → complete persona template manifest
  → staged persona tree
  → required-path validation
  → atomic promotion
  → project/component registration
```

### Experiment

```text
runtime + runbook + source model + B/C personas
  → exact model/version conditions
  → staged experiment tree
  → atomic promotion
```

任一模板、引用或渲染失败都不得留下 canonical 半成品。

Persona 内部的 work/publication 目录只保存自动生成索引，canonical work item 与 publication 始终位于根级目录。

## 八、不可变写作运行

旧单一 `writing-run-manifest.json` 已删除。

```text
writing-runs/run-*.json
writing-runs/<run-id>/...
```

每个 run 固定 repository commit、model/runbook/runtime 版本、参数、tools、loaded-file hashes、timestamps、exit status 与 outputs。

验证器使用：

```text
git show <repository_commit_sha>:<loaded-path>
```

读取历史 commit 中的 blob，而不是拿历史 hash 与当前 HEAD 比较。Unknown commit、duplicate run ID、path traversal 和非 run-scoped outputs 都会失败。

## 九、实验层

Work item、evaluation 与 experiment 是三个不同对象：

- work item：生成一次具体写作；
- evaluation：定义如何评分输出；
- experiment：管理假设、条件、控制变量、重复运行、盲评、失败案例、聚合分析和结论。

标准 experiment 至少包含：

```text
generic-runtime-baseline
source-model-direct-baseline
derived-author-b
derived-author-c
```

每个 condition 固定 persona、author model 和 source-author model 的 exact ID/version。Role 与 condition ID 必须唯一；B 与 C 必须是不同 persona。

四个条件共享 brief、research pack、runbook、runtime、模型参数、context budget 和工具权限。

真实 held-out 内容必须使用 `evaluator-storage://`，并位于 writer runtime 无法读取的独立存储或 workspace。

## 十、Lifecycle 与 gates

总体状态与 runbook stage、quality gate 分开。

成功路径：

```text
intake → in-progress → under-review → approved → published
```

不成功路径：

```text
rejected | cancelled | abandoned | superseded
```

任何终态都可以在记录 `archive_reason` 后归档。只有 approved/published 要求三个 gate 全部通过；失败或取消不需要伪造成功审核。

## 十一、可恢复出版事务

`approved-publications/` 不接受手工复制的普通草稿。正式内容必须经过：

```text
approved work item
  → gate and version validation
  → publication lock
  → staging article + metadata
  → transaction journal + backups
  → canonical promotion
  → manifest + state + persona indexes replacement
  → cleanup
```

进程异常后，下次 invocation 根据 journal 恢复。

独立 `validate_publication_integrity.py` 检查：

- 无残留 lock、journal 或 staging；
- manifest 与 canonical metadata 完全相同；
- canonical article hash 与 final approved article 相同；
- work-item state linkage 正确；
- persona indexes 可从 canonical records 精确重建。

零 publication 由空 JSONL manifest 表示，不生成 Sample B 或其他 sentinel。

## 十二、CI

CI 固定 GitHub Actions commit SHA，并使用 full checkout history。顺序：

1. structure；
2. JSON/JSONL syntax；
3. schema registry；
4. cross references；
5. author-scoped provenance；
6. policy references；
7. work-item state；
8. immutable run history；
9. publication integrity；
10. repository-mode placeholders；
11. Ruff；
12. pytest。

Python 验证依赖由 `validation-constraints.txt` 固定。

## 十三、当前边界

本仓库已经完成真实实跑前的执行合同与回归测试；但 sample source research、Sample B/C 内容、runtime 配置、真实 run、真实盲评与 production publication 仍未发生。绿色 CI 证明内部合同一致，不证明作者模型实验已经成功。
