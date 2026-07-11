# Author Lab 完整目录、文件与工作方式说明

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本文是 `author-lab-sample` 当前仓库结构与执行方式的权威说明。仓库已完成真实 A→B/C 实验开始前的结构、合同、脚手架、验证和治理整备；真实源作者研究、真实模型内容、正式 runtime run、盲评结果与生产出版物仍未发生。

本文回答：

1. 每个层次保存什么；
2. 哪个文件是权威来源；
3. 数据怎样向下游移动；
4. 哪些内容禁止回流；
5. 怎样创建、运行、审核和发布真实对象。

---

# 一、权威链与禁止回流

```text
source evidence
→ normalized source + segment map
→ author-scoped research claims
→ source-author model provenance
→ derived-author lineage / model
→ writing work item
→ immutable writing runs
→ factual / persona-style / editorial gates
→ recoverable publication transaction
→ canonical publication
```

实验是独立的受控对象：

```text
hypothesis
+ controlled inputs
+ exact runtime/runbook versions
+ exact source/derived model IDs and versions
+ repeated immutable runs
+ evaluator-only held-out material
+ blinded evaluation
+ failure cases
→ aggregate analysis
→ conclusion
```

禁止：

- derived-author 生成物成为 source-author evidence；
- A 的 research claim 引用另一个 source author 的 segment；
- A 的 source model 引用另一个 source author 的 claim；
- publication 自动写回 research 或 model；
- B 的 memory 自动进入 C；
- runtime adapter 携带隐藏人格；
- writer 读取 held-out pack、blind labels 或 raw evaluation results；
- presentation site 反向决定研究或 canonical publication 结构。

---

# 二、根目录：控制平面

| 路径 | 职责 |
|---|---|
| `README.md` | 仓库定位、真实状态、核心路径与完整验证命令。 |
| `AGENTS.md` | agent 的 source-of-truth hierarchy、加载、修改、运行、发布和验证规则。 |
| `author-lab-project-manifest.json` | 机器入口；声明 repository mode、readiness、source author/model/persona 目录和所有 register。 |
| `repository-component-status-register.json` | 区分 core / optional / example，并分别记录实现、验证、真实内容和实验验证状态。 |
| `repository-placeholder-register.json` | 定义 reference-sample 与 active-author-lab 的 placeholder 规则。 |
| `source-material-storage-and-ingestion-register.jsonl` | source storage URI、rights、checksum、ingestion、normalization、segmentation 与 research readiness。 |
| `validation-constraints.txt` | 固定 CI 使用的 setuptools、jsonschema、pytest 与 Ruff 版本。 |
| `RIGHTS-AND-LICENSING-POLICY.md` | 原始资料、生成物和出版物的权利边界。 |
| `ETHICS-AND-DERIVATION-DISCLOSURE-POLICY.md` | 派生作者、非冒充、私人经历、署名与披露原则。 |
| `CHANGELOG.md` | 按日期记录结构里程碑，不建立并存的仓库版本。 |
| `CONTRIBUTING.md` | PR、测试、schema、证据和 review 要求。 |
| `SECURITY.md` | secrets、私人资料、受限材料和事故处理。 |
| `.gitignore` | 排除环境、缓存、secrets、输出和 primary-source binaries。 |
| `.gitattributes` | 换行与二进制处理。 |
| `.editorconfig` | UTF-8、LF、缩进和文件末尾。 |
| `pyproject.toml` | Python 包、依赖范围、pytest 和 Ruff 配置。 |
| `.pre-commit-config.yaml` | 提交前基础检查。 |

## Repository mode

### `reference-sample`

- 有内容的受管文本文件必须包含 sample marker；
- sample persona/model/experiment/run 可以使用明确的 sample 状态；
- canonical JSONL manifest 可以真正为空，不需要伪造 sentinel record。

### `active-author-lab`

- 只有 placeholder register 登记的未完成文件可以含 marker；
- 生成器不得写入 sample marker、sample status、fake checksum 或 `SAMPLE-*` ID；
- 新 persona、work item、experiment 和 publication 必须直接生成 production-shaped records。

---

# 三、`documentation/`

| 路径 | 职责 |
|---|---|
| `documentation/README.md` | 文档导航。 |
| `complete-repository-file-and-directory-reference.md` | 本文；当前路径与职责的权威说明。 |
| `pre-real-run-complete-repository-design.md` | 最初实跑前仓库目标。 |
| `pre-real-run-remediation-design.md` | 外部审查后修复 active mode、provenance、experiment、run 和 publication 的设计。 |
| `repository-architecture-and-data-flow.md` | control plane、数据流、机器合同与执行对象。 |
| `source-author-research-methodology.md` | source storage、segmentation、claim、confidence 和 provenance。 |
| `derived-author-creation-methodology.md` | inherited / transformed / rejected / original / rationale。 |
| `provenance-and-evidence-policy.md` | 证据等级与禁止生成物回流。 |
| `publication-and-editorial-approval-policy.md` | gates、批准与出版责任。 |
| `naming-versioning-and-file-conventions.md` | ID、路径、文件和模型版本约定。 |
| `runtime-adapter-contract.md` | runtime 只定义执行环境。 |
| `writing-work-item-state-machine.md` | lifecycle、stages、gates、immutable runs 与 publication transaction。 |
| `glossary-of-author-lab-terms.md` | 统一术语。 |
| `implementation-plans/` | 已执行或正在执行的实施计划；不取代长期规范。 |

---

# 四、`source-authors/`：真实材料、权利和定位

一个真实 source author 一个目录。

## Source-author 根文件

| 文件 | 职责 |
|---|---|
| `AGENTS.md` | 局部证据与材料操作规则。 |
| `source-author-profile.json` | source author ID、语言、corpus、rights、research 和 compiled model 路径。 |
| `source-bibliography.md` | 人类可读书目、版本、译本和出版信息。 |
| `source-rights-register.jsonl` | 每个 source ID 的 rights、storage URI 与 repository-copy 权限。 |

## `source-corpus/`

| 路径 | 职责 |
|---|---|
| `source-corpus-manifest.jsonl` | source ID、edition、external URI、checksum、normalized text、segment map 和 segmentation version。 |
| `primary-source-materials/**/README.md` | 说明各类原始材料规则；受限二进制默认不进入 Git。 |
| `secondary-source-materials/` | biographies、historical context、criticism 和 scholarship。 |
| `normalized-source-materials/plain-text/` | 可审查的版本化纯文本。 |
| `normalized-source-materials/structured-metadata/*-segment-location-map.jsonl` | segment ID、source、edition、segmentation version、ordinal、hash 和位置。 |
| `normalized-source-materials/segmented-passages/` | 检索分段与上下文规则。 |

原始材料默认使用：

```text
private-storage://<source-author-id>/<source-id>
```

只有 rights 明确允许时才能使用 repository storage。

Segment identity 绑定 source、edition、segmentation version、ordinal 与 content hash。重新分段必须提升 segmentation version，不能复用旧 ID。

---

# 五、`source-author-research/`：按作者隔离的证据化研究

每个 research directory 只能处理一个 `source_author_id`。

## 研究内容

- `persona-and-intellectual-structure/`：关注、世界观、知识边界、推理、情绪、矛盾和不确定性。
- `writing-style-fingerprint/`：词汇、句法、节奏、段落、修辞、开头结尾、文类与时期差异、反例和过拟合风险。
- `topics-and-periodization/`：议题关系与时期划分。
- `comprehensive-research-reports/`：综合报告和限制。

## 证据合同

`evidence-and-confidence/research-claim-evidence-register.jsonl` 每条记录必须包含：

- `source_author_id`；
- `research_claim_id`；
- claim；
- confidence；
- status；
- supporting segments；
- counterexample segments。

Status：

```text
proposed | accepted | rejected | superseded | sample-unreviewed
```

Claim 只能引用同一 source author 的 segment。跨作者 segment reference 会被 CI 拒绝。

---

# 六、`source-author-models/`：可加载的研究编译物

| 文件或目录 | 职责 |
|---|---|
| `AGENTS.md` | 只有 accepted claim 可以支持 approved model rule。 |
| `VERSION` | source model 语义版本。 |
| `source-author-model-manifest.json` | model ID、source author ID、version、core/modes/load map/provenance。 |
| `source-author-model-limitations.md` | 缺口和不适用范围。 |
| `author-model-loading-map.json` | 默认 core 与 genre overlays。 |
| `source-author-model-provenance-register.jsonl` | model rule → author-scoped research claims → model file。 |
| `core-author-model/` | identity、concerns、worldview、epistemology、knowledge、reasoning、emotion、voice、style、boundaries、uncertainties。 |
| `genre-specific-author-modes/` | essay、column、criticism、diary、letter、short post。 |
| `period-specific-author-overlays/` | early / middle / late。 |
| `calibration-examples/` | 少量授权校准材料。 |
| `negative-calibration-examples/` | 反例和过拟合风险。 |

Provenance record 必须声明：

- `source_author_id`；
- `source_author_model_id`；
- `model_rule_id`；
- `research_claim_ids`；
- `model_file`；
- status。

Approved model rule 只能引用同一作者的 accepted claims。

---

# 七、`derived-author-personas/`：独立派生作者

每个 persona 是独立长期作者，不是 source author 的别名。

## Persona 根文件

| 文件 | 职责 |
|---|---|
| `README.md` | 公共定位和非冒充说明。 |
| `AGENTS.md` | persona 加载、隔离、memory 和写作规则。 |
| `derived-author-persona-manifest.json` | persona ID、状态、语言和子目录。 |
| `derived-author-lineage.json` | exact source model ID/version、影响角色与冒充禁令。 |

## `derivation-profile/`

- `inherited-source-author-traits.md`
- `transformed-source-author-traits.md`
- `rejected-source-author-traits.md`
- `original-derived-author-traits.md`
- `derivation-rationale-and-design-decisions.md`

## `derived-author-model/`

- `VERSION`
- `derived-author-model-manifest.json`
- `derived-author-model-loading-map.json`
- `core-derived-author-model/`
- `genre-specific-writing-modes/`

## Memory 与生成视图

- `derived-author-memory/author-writing-memory.md`
- `derived-author-memory/editorial-review-memory.md`
- `derived-author-memory/knowledge-growth-log.md`
- `derived-author-memory/publication-history.jsonl`
- `derived-author-writing-work-items/derived-author-work-item-index.jsonl`
- `derived-author-publications/derived-author-publication-index.jsonl`
- `derived-author-evaluations/`

Work/publication 目录只是生成索引，不能存第二份正文。

## Persona 创建

`create_new_derived_author_persona.py`：

1. 从 project manifest 解析 source-model directory；
2. 验证 source model ID 与 exact version；
3. 在临时 sibling directory 完整渲染 persona template；
4. 验证 required paths；
5. 原子提升到 canonical persona path；
6. 更新 project manifest；
7. 更新 component status register；
8. 任一步失败则回滚，不留下半成品。

Reference mode 生成带 marker 的 sample scaffold；active mode 生成无 marker 的 `draft` / `unreviewed` production records。

---

# 八、`shared-writing-harness/`

## `machine-readable-contracts/`

`document-schema-registry.json` 将生产型 JSON/JSONL path pattern 映射到 Draft 2020-12 schema。未注册的 machine document 会失败。

合同覆盖：

- project、component、placeholder、site；
- source profile、rights、storage、corpus、segments；
- research claims、source model、provenance、loading map；
- persona、lineage、derived model、indexes；
- runbook、work-item state、immutable writing run、sources、reviews、runtime；
- experiment、experiment runs、evaluation、aggregate analysis；
- publication 与 policy rules。

`writing-run-manifest.schema.json` 仍是 schema 文件名，但它验证的是：

```text
writing-work-items/**/writing-runs/run-*.json
```

旧的单一 `writing-run-manifest.json` 不再允许。

## `writing-runbooks/`

每个 `writing-runbook-manifest.json` 是以下内容的唯一权威来源：

- required stages；
- optional stages；
- required artifacts；
- artifact templates；
- required policy rule IDs。

## `artifact-templates/`

保存 brief、research pack、plan、draft、review、final、source register、authorized scene/text 和 semantic review 模板。

## `scaffold-templates/`

`derived-author-persona-template/template-manifest.json` 定义完整 persona required directories、required paths、Markdown files 与 default genre modes。

## `harness-policies/`

`policy-rule-register.jsonl` 是 policy IDs 的唯一机器来源。AGENTS、skills、prompts 和 runbooks 只能引用 ID，不分别维护不同版本的同一政策。

---

# 九、`agent-skills/`

- `source-author-researcher/SKILL.md`
- `derived-author-writer/SKILL.md`
- `factual-claim-reviewer/SKILL.md`
- `derived-author-style-reviewer/SKILL.md`
- `approved-publication-preparer/SKILL.md`

Skill 负责加载与执行，不复制 research/model/policy。Publisher skill 只能调用正式 publication transaction。

---

# 十、`runtime-adapters/`

每个 adapter 目录包含：

- `README.md`
- `runtime-adapter-configuration.json`

当前示例包括 ChatGPT、OpenClaw、Codex、Claude Code 和 local command line。Adapter 记录 runtime ID/version、模型入口、context window、tools 和环境变量，但不得决定 persona。

这些 adapter 仍是 optional/example；没有被错误标为已经跨 runtime 实验验证。

---

# 十一、`writing-work-items/`

一个 work item 一个 canonical directory。

## 核心工件

- `work-item-state.json`
- `writing-brief.md`
- `research-pack.md`
- `work-item-source-register.jsonl`
- `article-plan.md`
- 不可覆盖 drafts
- factual review
- style review
- editor review
- `final-approved-article.md`

## State

`work-item-state.json` 分开记录：

- lifecycle status；
- stage executions；
- quality gates；
- exact persona/model/runbook/runtime versions；
- typed publication metadata；
- archive reason。

Lifecycle：

```text
intake | in-progress | under-review | approved | published
rejected | cancelled | abandoned | superseded | archived
```

只有 approved/published 强制三个 gate 全部通过。Archived 必须有原因，但可以保存失败或取消的工作。

## Immutable writing runs

```text
writing-runs/README.md
writing-runs/run-*.json
writing-runs/<run-id>/...
```

每个 run 记录：

- repository commit SHA；
- exact model/runbook/runtime versions；
- model parameters；
- context budget；
- tool permissions；
- loaded file hashes；
- timestamps；
- exit status；
- run-scoped output paths。

Validator 使用 `git show <sha>:<path>` 检查历史输入，不与当前 HEAD 比较。Run ID 重复、未知 commit、path traversal、输出不在 run-specific directory 都会失败。

Reference sample 可以保留 `run-sample-not-run.json`；active mode 不创建 fake run record。

## Work-item 创建

`create_new_writing_work_item.py` 从 project-declared persona、selected runbook 和 runtime 解析 exact versions，在 staging 中生成全部 artifacts 与 state，完成后原子提升。渲染失败不得留下半目录。

---

# 十二、`author-model-evaluations/`

- fidelity rubric；
- independent persona consistency；
- source leakage；
- originality；
- B/C distinction；
- factuality / scene authorization；
- calibration cases；
- held-out interface；
- adversarial cases；
- runtime comparison reports。

真实 held-out 内容不在 writer-readable repository。

---

# 十三、`author-model-experiments/`

## Experiment 文件

- `experiment-manifest.json`
- `hypothesis.md`
- `controlled-inputs/`
- `runtime-run-records/`
- `raw-evaluation-results.jsonl`
- `aggregate-analysis.json`
- `failure-cases/`
- `experiment-conclusion.md`

## 标准四条件

1. generic runtime baseline；
2. source-model-direct baseline；
3. Derived Author B；
4. Derived Author C。

每个 condition 固定：

- condition ID 与 role；
- persona ID；
- author model ID/version；
- source-author model ID/version。

Generic baseline 的全部 author fields 必须为空。Source-direct condition 必须锁定 exact source model。B/C 必须是不同 persona，并分别锁定 exact derived model 和 upstream source model。

共享 controlled execution 固定 runtime/runbook versions、parameters、context budget、tools、repetition count 和 randomness control。

Active experiment 的 raw results 起始为真正空 JSONL，不生成 `SAMPLE-NOT-RUN`。

---

# 十四、`derived-author-comparisons/`

保存 source model vs B、source model vs C、B vs C 的受控比较报告。比较报告是 evaluation asset，不得成为写作 prompt。

---

# 十五、`approved-publications/`

| 路径 | 职责 |
|---|---|
| `approved-publication-manifest.jsonl` | canonical publication index；零出版物时是空文件。 |
| `researched-essays/` | 研究型散文。 |
| `short-public-commentaries/` | 短评论。 |
| `authorized-life-writing/` | 授权生活写作。 |
| `book-length-projects/` | 长篇 canonical manuscript。 |
| `editorial-collections/` | 专题集与选集。 |

禁止手工复制 draft 或编辑 manifest。

## Recoverable publication transaction

`publish_approved_writing_work_item.py`：

1. 恢复残留 journal；
2. 获取 publication lock；
3. 验证 gates、review stages、final article 和 persona/model version；
4. staging article 与 metadata；
5. 预计算 manifest、state 和 persona indexes；
6. 写 journal 与 backups；
7. 原子提升 canonical publication；
8. 联合替换所有生成记录；
9. 清理 journal、staging 和 lock。

`validate_publication_integrity.py` 在 CI 中独立检查：

- 无残留 transaction artifacts；
- metadata 与 manifest 一致；
- canonical article hash 与 final-approved article 一致；
- state linkage 正确；
- persona work/publication indexes 可精确重建。

因此手工绕过 publisher 也不能通过 CI。

---

# 十六、`publication-site/`

可选展示层，只读取 approved publications；不控制 research、work item 或 canonical publication 结构。

---

# 十七、`repository-automation-scripts/`

## 共享基础

| 文件 | 职责 |
|---|---|
| `repository_mode_support.py` | mode-aware marker、status、template rendering 与 active sentinel 规则。 |
| `atomic_repository_update.py` | staged sibling、atomic promotion、多文件替换与 rollback。 |
| `publication_gate_support.py` | publication gate、canonical hash 和 manifest helpers。 |

## 创建与转换

| 文件 | 职责 |
|---|---|
| `create_new_derived_author_persona.py` | 原子生成并注册完整 persona。 |
| `create_new_writing_work_item.py` | 按 runbook 原子生成 work item 与 writing-runs directory。 |
| `create_new_author_model_experiment.py` | 原子生成 exact-version-pinned 四条件实验。 |
| `normalize_authorized_plain_text_source.py` | 生成 versioned normalized source 与 segment map。 |
| `rebuild_derived_author_indexes.py` | 从 canonical objects 确定性重建 persona indexes。 |

## Publication

| 文件 | 职责 |
|---|---|
| `publish_approved_writing_work_item.py` | lock/journal/staging/recovery publication transaction。 |
| `build_approved_publication_manifest.py` | 验证 metadata 后联合重建 manifest 和 persona indexes。 |
| `validate_publication_integrity.py` | 独立检查 transaction residue、manifest、hash、state 与 indexes。 |

## Validators

- `validate_author_lab_repository_structure.py`
- `validate_json_and_jsonl_documents.py`
- `validate_machine_readable_contracts.py`
- `validate_repository_cross_references.py`
- `validate_source_research_and_model_provenance.py`
- `validate_policy_rule_references.py`
- `validate_writing_work_item_state.py`
- `validate_writing_run_reproducibility.py`
- `validate_sample_comment_markers.py`

---

# 十八、`repository-validation-tests/`

测试不只检查文件存在，还覆盖：

- active/reference mode generation；
- persona source-model resolution、registration 与 atomic failure cleanup；
- runbook-driven work items；
- author-scoped provenance；
- accepted claim gate；
- experiment condition version pinning 与 B/C distinction；
- immutable multi-run history与 historical commit hashes；
- unsuccessful lifecycle 与 archive reason；
- publication staging cleanup、journal recovery、empty manifest、manual bypass 和 stale indexes；
- schemas、cross references、policies、normalization 和 placeholder modes。

---

# 十九、`.github/`

| 路径 | 职责 |
|---|---|
| `.github/workflows/validate-author-lab-repository.yml` | 完整 CI。GitHub Actions 固定到 commit SHA，checkout fetch-depth 为 0。 |
| `.github/CODEOWNERS` | 关键目录责任人。 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 证据、schema/test 和验证清单。 |
| `.github/ISSUE_TEMPLATE/` | research claim、persona/model change 与 validation problem。 |

CI 顺序：

1. structure；
2. JSON/JSONL syntax；
3. schema registry；
4. cross references 与 generated indexes；
5. author-scoped provenance；
6. policy references；
7. work-item states；
8. immutable run reproducibility；
9. publication integrity；
10. repository-mode placeholders；
11. Ruff；
12. pytest。

失败时上传 placeholder、Ruff 和 pytest diagnostics。

---

# 二十、角色读取路径

- Corpus curator：rights policy → source profile → corpus/rights/storage → normalization。
- Source researcher：profile → versioned segments → methodology → claim register。
- Source-model curator：accepted claims → reports/limitations → provenance → model files。
- Persona designer：exact source model → derivation methodology → persona generator → reviewed persona model。
- Writer：state → selected persona/model/mode → runbook → brief/research/source register。
- Factual reviewer：draft → research pack/source register → factual policy。
- Style reviewer：draft → persona/derivation/model → style/leakage/originality rubrics。
- Editor：完整 work item 与 reviews → editorial gate。
- Publisher：只调用 recoverable publication command。
- Evaluator：blind pack、rubrics 和 outputs；held-out 位于 evaluator-only storage。
- Runtime maintainer：adapter、tool、run records 和 CI；不得改变 persona 以适配 runtime。

---

# 二十一、标准操作

## 新增真实 source author

1. 建立 profile、bibliography、rights 和 corpus manifest；
2. 登记 external storage 与 checksum；
3. 生成 normalized text 和 segment map；
4. 建立 author-scoped research claim register；
5. claims accepted 后建立 source model provenance；
6. 更新 project/component registers；
7. 运行完整 CI。

## 新增 derived author

1. 调用 persona generator 并提供 exact source model ID/version；
2. generator 自动 staging、验证、注册和原子提交；
3. 完成 derivation、core、genres、boundaries 和 uncertainties；
4. review 后改变 persona/model status；
5. 通过 calibration/adversarial checks 后进入真实生产。

## 新增 work item

1. 选择 persona、runbook、runtime；
2. 调用 work-item generator；
3. 完成 brief、research、sources 和 plan；
4. 每次模型执行创建新的 `writing-runs/run-*.json` 与 run-specific outputs；
5. 保留 drafts 和 reviews；
6. 通过 factual、persona/style、editor gates；
7. approved 后调用 publication transaction。

## 新增 experiment

1. 调用 experiment generator；
2. 锁定 exact source/derived model versions；
3. 固定 common inputs 与 execution controls；
4. 把 held-out pack 放在 evaluator-only storage；
5. 记录 condition × repetition runs；
6. 盲评并保留 failures/exclusions/disagreement；
7. 生成 aggregate analysis；
8. 最后写 conclusion。

---

# 二十二、当前最终状态

```text
Reference architecture: complete
Executable pre-real-run core: complete
Active-mode generation: validated
Author-scoped provenance: validated
Exact experiment model pinning: validated
Immutable multi-run history: validated
Recoverable publication transaction: validated
Independent publication integrity gate: validated
Real source content: not started
Real A→B/C controlled experiment: not run
Experimental validation: false
Production publications: none
```

下一阶段不再扩建架构，而是选择有限真实 corpus、一个主要 runtime、真实 source model、B/C 两个派生作者和固定测试任务，运行第一场受控实验。
