# Repository Architecture and Data Flow

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本仓库把真实证据、研究解释、可执行模型、派生作者、具体任务、实验、审核和出版分成不同的权威层。分层的目的不是增加文件数量，而是让每条结论、每次生成和每个出版决定都能追溯。

## 一、主数据流

```text
source-author materials
  → normalized text + versioned segment map
  → evidence-backed research claims
  → source-author model + provenance register
  → derived-author lineage and derivation profile
  → derived-author executable model
  → work item + selected runbook + selected runtime
  → factual gate + persona/style gate + editor approval
  → transactional approved publication
```

任何下游工件都不得静默修改上游层：

- 生成文章不能证明源作者具备某种特征；
- publication 不能自动写回 source-author research 或 source-author model；
- 一个派生作者的 memory 不能自动进入另一个派生作者；
- runtime adapter 不能决定作者身份、议题或文风；
- presentation site 不能反过来决定研究和出版目录。

核心边界由 `POLICY-PROVENANCE-001`、`POLICY-DERIVATION-001`、`POLICY-FACTUALITY-001`、`POLICY-ORIGINALITY-001` 和 `POLICY-PUBLICATION-001` 统一编号。

## 二、控制平面

根级 `author-lab-project-manifest.json` 是仓库机器入口。它声明：

- repository mode 与 readiness status；
- source author、source model、persona 目录；
- harness、runtime、work item、evaluation、experiment 与 publication 目录；
- component、placeholder、storage、schema、persona template 和 policy register。

验证器从 manifest 发现对象，不再硬编码 Sample A/B/C 名称。

`repository-component-status-register.json` 区分：

```text
component_class:
  core | optional | example

implementation_status:
  placeholder | scaffolded | partially-implemented
  | implemented | experimentally-validated | example | deprecated
```

所以目录存在只代表架构位置存在，不代表真实内容、runtime 或实验已经完成。

## 三、资料与规范化层

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

规范化文本不再使用声称跨编辑稳定的简单段落序号。每个 segment 绑定：

```text
source_id
edition_id
segmentation_version
segment_ordinal
content_sha256
```

重新分段必须提升 segmentation version；即使正文未变，新的分段命名空间也与旧版本分开。

## 四、机器合同执行

`document-schema-registry.json` 将 path pattern 映射到 schema。执行顺序为：

```text
JSON/JSONL syntax
  → registered JSON Schema validation
  → semantic and cross-reference validation
```

生产型机器文档如果没有 schema registration，也没有明确分类为 schema definition 或 artifact template，CI 会失败。

跨引用验证进一步检查：

- source、rights、storage、normalized text 与 segment map；
- research claim segment ID 与 source-model provenance；
- source model、persona、derived model 的 ID 和版本；
- runbook stages、artifact templates 和 policy IDs；
- work item 的 persona/model/runbook/runtime；
- experiment 的四个条件与 held-out URI；
- publication 的 work item、persona/model、canonical file 与状态。

## 五、脚手架权威关系

新 work item：

```text
runbook manifest
  → stages
  → required artifacts
  → artifact templates
  → create_new_writing_work_item.py
```

新 persona：

```text
complete persona template manifest
  → required directories and paths
  → generic Markdown and JSON structures
  → create_new_derived_author_persona.py
```

Sample B/C、generator 和 structure validator 必须共享这两个权威来源，不再分别手写目录事实。

Persona 内部的 work/publication 目录只保存自动生成索引，canonical work item 与 publication 始终位于根级目录。

## 六、实验层

Work item、evaluation 与 experiment 是三个不同对象：

- work item：生成一次具体写作；
- evaluation：定义如何评分一个输出；
- experiment：管理假设、条件、控制变量、重复运行、盲评、失败案例、聚合分析和结论。

第一类标准 experiment 至少包含：

```text
generic-runtime-baseline
source-model-direct-baseline
derived-author-b
derived-author-c
```

四个条件应共享 brief、research pack、runbook、runtime、模型参数、context budget 和工具权限。

真实 held-out 内容必须使用 `evaluator-storage://`，并位于 writer runtime 无法读取的独立存储或 workspace。仓库中的 experiment template 只定义接口，不包含真实 held-out 题目或虚假结果。

## 七、出版层

`approved-publications/` 不接受手工复制的普通草稿。正式内容必须经过 publication transaction：

```text
approved work item
  → gate and version validation
  → staging copy
  → canonical article + metadata
  → manifest rebuild
  → work-item state update
```

任何失败都应回滚，避免 canonical 文件、manifest 和 work-item state 不一致。

## 八、当前边界

本仓库已经是“真实实跑前完整”参考实现，含可执行验证、脚手架、实验接口和 publication gate；但 sample source research、B/C 内容和 runtime 配置仍是示例，第一场真实实验尚未运行。
