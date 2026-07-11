# Author Lab 完整目录、文件与工作方式说明

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本文是 `author-lab-sample` 当前“真实实跑前完整仓库”的权威逐路径说明。它回答四个问题：

1. 每个目录和文件负责什么；
2. 谁可以读写；
3. 上游输入与下游输出是什么；
4. 什么内容不得跨层回流。

当前仓库已经完成结构、机器合同、脚手架、验证、实验接口和出版事务的实跑前整备；Sample Source Author、Sample B/C、runtime 配置和实验结果仍是示例，不代表真实研究或实验已经完成。

---

# 一、系统对象与单向数据流

仓库管理以下对象：

```text
真实源作者资料
→ 版本化规范化文本与 segment map
→ 有证据的源作者研究 claim
→ 带 provenance 的 source-author model
→ 独立 derived-author lineage / derivation / model
→ writing work item
→ factual / persona-style / editorial gates
→ approved publication
```

实验是横跨 work item 与 evaluation 的比较对象：

```text
hypothesis
+ controlled inputs
+ controlled execution
+ multiple conditions
+ immutable run records
+ blinded evaluation
+ failure cases
→ aggregate analysis
→ experiment conclusion
```

禁止：

- derived-author 生成物成为源作者证据；
- publication 自动写回 research 或 model；
- B 的 memory 自动进入 C；
- runtime adapter 偷带作者人格；
- writer 读取真实 held-out evaluation material；
- 网站目录反过来决定研究与出版结构。

---

# 二、根目录：项目控制平面

| 路径 | 职责 |
|---|---|
| `README.md` | 人类入口；准确说明 reference architecture、executable core、真实内容和实验状态。 |
| `AGENTS.md` | 根级 agent 操作边界、source-of-truth hierarchy、加载与修改规则、policy IDs 和完成前验证。 |
| `author-lab-project-manifest.json` | 机器入口；声明 repository mode、readiness、各对象目录及所有 register。 |
| `repository-component-status-register.json` | 区分 Core / Optional / Example、实现状态、验证状态、基础设施 readiness、真实内容状态和实验验证状态。 |
| `repository-placeholder-register.json` | 管理 reference-sample 与 active-author-lab 两种 marker 语义。 |
| `source-material-storage-and-ingestion-register.jsonl` | 全仓库资料存储与摄取状态索引；记录 URI、rights、checksum、normalization、segmentation 和 research readiness。 |
| `RIGHTS-AND-LICENSING-POLICY.md` | 原始材料、代码、模型、图片、音频和出版物的权利与再分发政策。 |
| `ETHICS-AND-DERIVATION-DISCLOSURE-POLICY.md` | 派生关系、非冒充、私人经历、署名和披露边界。 |
| `CHANGELOG.md` | 按日期与里程碑记录仓库升级；不建立并存的仓库版本体系。 |
| `CONTRIBUTING.md` | 贡献、证据、PR、schema/test 同步和 review 要求。 |
| `SECURITY.md` | 密钥、私人资料、受限原始材料、个人信息和事故处理。 |
| `.gitignore` | 排除缓存、环境、secrets、构建产物和 primary-source binaries；保留资料目录 README。 |
| `.gitattributes` | 统一换行和二进制文件处理。 |
| `.editorconfig` | 统一 UTF-8、LF、缩进与文件末尾。 |
| `pyproject.toml` | Python 工具包、`jsonschema`、pytest、ruff 和测试配置。 |
| `.pre-commit-config.yaml` | 提交前文本、JSON/YAML 与 Python 基础检查。 |

`repository_mode`：

- `reference-sample`：所有受管文本文件保留 sample marker；
- `active-author-lab`：只有 placeholder register 登记的未完成文件可以保留 marker。

---

# 三、`documentation/`：长期方法与仓库说明

| 路径 | 职责 |
|---|---|
| `documentation/README.md` | 文档导航与权威状态来源索引。 |
| `documentation/complete-repository-file-and-directory-reference.md` | 本文；逐路径职责的权威说明。 |
| `documentation/pre-real-run-complete-repository-design.md` | 真实实跑前完整仓库的目标、边界、完成标准和不做事项。 |
| `documentation/repository-architecture-and-data-flow.md` | 数据流、control plane、contracts、scaffolding、experiments 与 publication transaction。 |
| `documentation/source-author-research-methodology.md` | rights/storage、edition、segmentation、claim、counterexample、confidence 与 provenance 方法。 |
| `documentation/derived-author-creation-methodology.md` | inherited、transformed、rejected、original、rationale 与独立作者形成方法。 |
| `documentation/provenance-and-evidence-policy.md` | 证据等级、claim 可追溯性与禁止生成物回流。 |
| `documentation/publication-and-editorial-approval-policy.md` | factual/style/editorial gates 与正式出版责任。 |
| `documentation/naming-versioning-and-file-conventions.md` | 长描述性名称、标准入口文件、对象 ID 和模型版本约定。 |
| `documentation/runtime-adapter-contract.md` | runtime 只能描述执行环境，不能承载作者身份。 |
| `documentation/writing-work-item-state-machine.md` | lifecycle、stage execution、quality gates、不可覆盖原则和 publication transaction。 |
| `documentation/glossary-of-author-lab-terms.md` | 统一 source author、model、persona、runbook、runtime、work item、evaluation、experiment 等术语。 |

## `documentation/implementation-plans/`

| 文件 | 职责 |
|---|---|
| `2026-07-11-complete-author-lab-sample-repository-scaffold.md` | 最初完整 reference scaffold 的实施记录。 |
| `2026-07-11-complete-repository-file-and-directory-guide.md` | 第一份逐文件说明建立计划。 |
| `2026-07-11-pre-real-run-complete-repository-upgrade.md` | 本次实跑前完整升级的任务、文件与验证清单。 |

Implementation plan 记录“怎样改仓库”，不取代长期规范，也不构成实验结果。

---

# 四、`source-authors/`：真实源作者、权利与资料

## 顶层

| 路径 | 职责 |
|---|---|
| `source-authors/README.md` | 一个真实源作者一个目录的总规则。 |
| `source-authors/source-author-sample/AGENTS.md` | 源材料局部规则：原件不可覆盖、不得加载派生文章作为证据。 |
| `source-author-profile.json` | source author ID、语言、corpus、rights、research 与 compiled model 路径。 |
| `source-bibliography.md` | 人类可读版本、译本、期刊与出版书目。 |
| `source-rights-register.jsonl` | 每个 source ID 的 rights、redistribution、storage URI 和 repository copy 权限。 |

## `source-corpus/`

| 路径 | 职责 |
|---|---|
| `source-corpus-manifest.jsonl` | source ID、type、edition、external storage URI、normalized text、segment map、checksum 与 segmentation version。 |

### `primary-source-materials/`

这些目录只保留 README；版权二进制默认位于仓库外。

- `README.md` — 原作材料总规则。
- `books/README.md` — 书籍、EPUB、版本和章节映射。
- `essays-and-articles/README.md` — 散文、评论、报刊和网页文章。
- `interviews-and-conversations/README.md` — 说话人、转录、翻译与编辑删节。
- `letters-and-correspondence/README.md` — 授权、收件人、公开状态和隐私。
- `diaries-and-notebooks/README.md` — 时间、编辑介入与私人材料边界。
- `speeches-and-lectures/README.md` — 场合、听众、准备稿与口述版本。
- `social-media-and-short-form-writing/README.md` — 时间戳、上下文、线程和平台状态。

### `secondary-source-materials/`

- `README.md` — 二手材料不得冒充源作者原话。
- `biographies-and-historical-context/README.md` — 传记、背景、争议与来源立场。
- `criticism-and-scholarship/README.md` — 评论、研究、书评和解释传统。

### `normalized-source-materials/`

- `README.md` — 可重建层与 source-location 映射总则。
- `plain-text/README.md` — 纯文本格式。
- `plain-text/SOURCE-BOOK-0001.md` — 版本化 sample normalized text。
- `structured-metadata/README.md` — edition、章节、页码、说话人和位置结构。
- `structured-metadata/SOURCE-BOOK-0001-segment-location-map.jsonl` — segment ID、ordinal、full SHA-256 与 character count。
- `segmented-passages/README.md` — 检索分段与上下文保留规则。

Segment ID 绑定 source、edition、segmentation version、ordinal 与 hash prefix；重新分段必须提升 segmentation version。

---

# 五、`source-author-research/`：证据化研究

| 路径 | 职责 |
|---|---|
| `source-author-research/README.md` | 研究层与 corpus/model/persona 的边界。 |
| `source-author-sample-research/AGENTS.md` | claim 必须引用 segment、记录反例与 confidence；禁止生成物回流。 |

## `persona-and-intellectual-structure/`

- `recurring-concerns-and-attention-patterns.md` — 长期关注与触发物。
- `worldview-values-and-central-tensions.md` — 价值、世界观和张力。
- `epistemology-and-standards-of-evidence.md` — 知识、证言、推断与不确定。
- `knowledge-structure-and-domain-boundaries.md` — 知识领域、薄弱区域和明确未知。
- `reasoning-patterns-and-problem-framing.md` — 发现、框架、语境、尺度与判断。
- `emotional-register-and-public-position.md` — 情绪范围、公共距离和论证关系。
- `contradictions-blind-spots-and-uncertainties.md` — 矛盾、盲点、材料空缺和开放解释。

## `writing-style-fingerprint/`

- `vocabulary-and-diction-patterns.md`
- `sentence-syntax-and-rhythm-patterns.md`
- `paragraph-architecture-and-transition-patterns.md`
- `rhetorical-moves-and-argument-structures.md`
- `openings-endings-and-narrative-distance.md`
- `genre-specific-and-period-specific-variations.md`
- `anti-patterns-counterexamples-and-overfitting-risks.md`

这些文件研究关系、分布与变化，不建立可复制短语库。

## `topics-and-periodization/`

- `recurring-topics-and-issue-relationships.md` — 议题图谱。
- `topic-chronology-and-periodization.md` — 依据材料划分时期。

## `evidence-and-confidence/`

- `research-claim-evidence-register.jsonl` — claim ID、claim、confidence、status、supporting/counterexample segment IDs。
- `research-confidence-rating-guide.md` — high/medium/provisional/open 与 model 准入门槛。

## `comprehensive-research-reports/`

- `comprehensive-source-author-research-report.md` — 综合研究报告。
- `source-author-research-limitations.md` — corpus、版本、翻译和解释限制。

---

# 六、`source-author-models/`：从研究编译的可加载模型

| 路径 | 职责 |
|---|---|
| `source-author-models/README.md` | 模型是研究编译物，不是源作者本人。 |
| `source-author-sample-model/AGENTS.md` | 只有 accepted claim 可进入模型，生成文本不得写回。 |
| `VERSION` | source model 语义版本；真实实验需要精确记录。 |
| `source-author-model-manifest.json` | model ID、source author ID、version、core/modes/overlays/load map/provenance。 |
| `source-author-model-limitations.md` | 不完整性和不适用范围。 |
| `author-model-loading-map.json` | default core 与 genre modes 的加载组合。 |
| `source-author-model-provenance-register.jsonl` | model rule → research claim IDs → model file。 |

## `core-author-model/`

- `source-author-identity.md`
- `recurring-concerns.md`
- `worldview-and-central-tensions.md`
- `epistemology-and-uncertainty-practice.md`
- `knowledge-map-and-domain-boundaries.md`
- `reasoning-patterns.md`
- `emotional-register.md`
- `voice-and-register.md`
- `writing-style-fingerprint.md`
- `authorial-boundaries.md`
- `model-uncertainties.md`

## `genre-specific-author-modes/`

- `essay-writing-mode.md`
- `column-writing-mode.md`
- `criticism-writing-mode.md`
- `diary-writing-mode.md`
- `letter-writing-mode.md`
- `short-post-writing-mode.md`

## `period-specific-author-overlays/`

- `early-period-author-overlay.md`
- `middle-period-author-overlay.md`
- `late-period-author-overlay.md`

## Calibration

- `calibration-examples/README.md` — 少量授权例子和用途限制。
- `negative-calibration-examples/README.md` — 反例、近似文本和过拟合风险。

---

# 七、`derived-author-personas/`：独立派生作者

`derived-author-personas/README.md` 规定一个子目录代表一个长期维护的独立化名作者。

Sample B 与 C 都必须拥有以下结构；内容不得互相共用。

## Persona 根文件

| 文件 | 职责 |
|---|---|
| `README.md` | 人类可读定位与非冒充说明。 |
| `AGENTS.md` | 本 persona 的加载、写入和隔离规则。 |
| `derived-author-persona-manifest.json` | persona 机器入口与各子目录。 |
| `derived-author-lineage.json` | 上游 source model、版本、角色、设计权重和冒充禁令。 |

## `derivation-profile/`

- `inherited-source-author-traits.md`
- `transformed-source-author-traits.md`
- `rejected-source-author-traits.md`
- `original-derived-author-traits.md`
- `derivation-rationale-and-design-decisions.md`

五个文件共同回答“受到了什么影响，又怎样成为另一个作者”。

## `derived-author-model/`

- `VERSION` — derived model 版本。
- `derived-author-model-manifest.json` — model ID、persona ID、version、core、genre 与 load map。
- `derived-author-model-loading-map.json` — default core 与 genre overlay。

### `core-derived-author-model/`

- `derived-author-identity-and-public-role.md`
- `recurring-concerns-and-topic-boundaries.md`
- `worldview-values-and-central-tensions.md`
- `knowledge-boundaries-and-research-obligations.md`
- `reasoning-patterns-and-problem-framing.md`
- `emotional-register-and-narrative-distance.md`
- `voice-and-writing-style-fingerprint.md`
- `authorial-and-ethical-boundaries.md`
- `model-uncertainties-and-open-questions.md`

### `genre-specific-writing-modes/`

共同文件：

- `README.md` — genre overlay 索引与加载规则。
- `diary-and-life-writing-mode.md` — 生活材料授权与非虚构边界。

Sample B：

- `essay-writing-mode.md`
- `short-commentary-writing-mode.md`

Sample C：

- `cultural-essay-writing-mode.md`
- `short-cultural-commentary-writing-mode.md`

## 其他 persona 子目录

| 路径 | 职责 |
|---|---|
| `author-specific-writing-harness/derived-author-writing-overlays.md` | 只增加 persona 加载和差异化约束，不复制 shared harness。 |
| `derived-author-memory/author-writing-memory.md` | 已批准写作历史和有意发展。 |
| `derived-author-memory/editorial-review-memory.md` | 重复编辑问题和接受的修正。 |
| `derived-author-memory/knowledge-growth-log.md` | 审核后的知识增长，不自动改变人格。 |
| `derived-author-memory/publication-history.jsonl` | publication history 机器记录。 |
| `derived-author-writing-work-items/README.md` | 说明该目录只是生成视图。 |
| `derived-author-writing-work-items/derived-author-work-item-index.jsonl` | 从根级 canonical work items 重建的索引。 |
| `derived-author-evaluations/README.md` | persona-specific evaluation 范围。 |
| `derived-author-publications/README.md` | 说明该目录只是生成视图。 |
| `derived-author-publications/derived-author-publication-index.jsonl` | 从根级 canonical publications 重建的索引。 |

完整新 persona 由 `shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json` 和 `create_new_derived_author_persona.py` 生成。

---

# 八、`shared-writing-harness/`：共享执行控制

| 路径 | 职责 |
|---|---|
| `README.md` | contracts、runbooks、prompts、policies 与 templates 总览。 |
| `AGENTS.md` | harness 的 canonical responsibilities、controlled repetition 与 contract-change 规则。 |

## `machine-readable-contracts/`

`README.md` 解释 schema 是稳定接口。`document-schema-registry.json` 将生产型 machine documents 映射到 schema；未注册文件会失败。

### Project / repository

- `author-lab-project-manifest.schema.json`
- `repository-component-status-register.schema.json`
- `repository-placeholder-register.schema.json`
- `publication-site-configuration.schema.json`

### Source evidence / research / model

- `source-author-profile.schema.json`
- `source-rights-record.schema.json`
- `source-material-storage-record.schema.json`
- `source-corpus-record.schema.json`
- `source-segment-location-record.schema.json`
- `research-claim-evidence-record.schema.json`
- `source-author-model-manifest.schema.json`
- `source-author-model-provenance-record.schema.json`
- `author-model-loading-map.schema.json`

### Derived authors

- `derived-author-persona-manifest.schema.json`
- `derived-author-lineage.schema.json`
- `derived-author-model-manifest.schema.json`
- `derived-author-persona-template-manifest.schema.json`
- `derived-author-publication-history-record.schema.json`
- `derived-author-work-item-index-record.schema.json`
- `derived-author-publication-index-record.schema.json`

### Work items / runtime / review

- `writing-runbook-manifest.schema.json`
- `writing-work-item-state.schema.json`
- `writing-run-manifest.schema.json`
- `work-item-source-record.schema.json`
- `factual-review-result.schema.json`
- `style-review-result.schema.json`
- `runtime-adapter-configuration.schema.json`

### Evaluation / experiment / publication

- `evaluation-result.schema.json`
- `author-model-experiment-manifest.schema.json`
- `experiment-runtime-run-record.schema.json`
- `experiment-evaluation-result.schema.json`
- `experiment-aggregate-analysis.schema.json`
- `publication-record.schema.json`
- `policy-rule-record.schema.json`

## `task-prompts/`

- `README.md` — prompt 只定义阶段输出，作者身份来自 persona。
- `source-research-stage-prompt.md`
- `structured-planning-stage-prompt.md`
- `complete-drafting-stage-prompt.md`
- `factual-review-stage-prompt.md`
- `style-review-stage-prompt.md`
- `editorial-revision-stage-prompt.md`
- `publication-preparation-stage-prompt.md`

关键 prompt 引用 canonical policy IDs，不重新定义政策。

## `writing-runbooks/`

- `README.md` — runbook 不选择作者或实际模型。
- `standard-researched-essay/README.md` + `writing-runbook-manifest.json`
- `deep-research-article/README.md` + `writing-runbook-manifest.json`
- `short-public-commentary/README.md` + `writing-runbook-manifest.json`
- `authorized-life-writing/README.md` + `writing-runbook-manifest.json`
- `style-preserving-rewrite/README.md` + `writing-runbook-manifest.json`

每个 manifest 是 stages、required artifacts、artifact templates 与 policy IDs 的唯一权威来源。

## `harness-policies/`

- `factuality-and-claim-classification-policy.md`
- `citation-and-source-quality-policy.md`
- `derived-author-boundaries-and-source-leakage-policy.md`
- `originality-and-non-copying-policy.md`
- `editorial-review-and-publication-gates-policy.md`
- `policy-rule-register.jsonl` — canonical policy IDs、规范文件、摘要和 enforcement scope。

## `artifact-templates/`

- `writing-brief-template.md`
- `research-pack-template.md`
- `article-plan-template.md`
- `editor-review-template.md`
- `final-publication-metadata-template.json`
- `article-draft-template.md`
- `final-approved-article-template.md`
- `factual-review-result-template.json`
- `style-review-result-template.json`
- `work-item-source-register-template.jsonl`
- `authorized-scene-details-template.md`
- `authorized-source-text-template.md`
- `semantic-review-result-template.md`

Templates 可以包含未解析变量，因此在 schema registry 中显式分类为 artifact templates；生成后的 runtime 文件必须通过对应 schema。

## `scaffold-templates/`

- `derived-author-persona-template/template-manifest.json` — 完整 persona 必需目录、路径、Markdown 文件和默认 genre modes。

---

# 九、`agent-skills/`：轻量角色入口

| 文件 | 职责 |
|---|---|
| `README.md` | skills 只负责加载和执行，不复制研究或 harness。 |
| `source-author-researcher/SKILL.md` | 读取版本化证据并写 research claims；引用 `POLICY-PROVENANCE-001`。 |
| `derived-author-writer/SKILL.md` | 按 work item 加载一个 persona/mode/runbook；禁止 held-out 和跨 persona memory。 |
| `factual-claim-reviewer/SKILL.md` | 独立 claim 分类与事实支持审核。 |
| `derived-author-style-reviewer/SKILL.md` | persona consistency、leakage、originality 与 distinction 审核。 |
| `approved-publication-preparer/SKILL.md` | 只能通过 transactional publication command 发布。 |

---

# 十、`runtime-adapters/`：执行环境

`runtime-adapters/README.md` 规定 adapter 不携带作者知识。

每个目录包含 `README.md` 和 `runtime-adapter-configuration.json`：

- `chatgpt-runtime-adapter/`
- `openclaw-runtime-adapter/`
- `codex-runtime-adapter/`
- `claude-code-runtime-adapter/`
- `local-command-line-runtime-adapter/`

Configuration 记录 runtime ID/type/version、default model、context window、tool capabilities 和环境变量。当前这些 adapter 是示例或 scaffold；没有一个被虚假标记为已完成跨 runtime 实验验证。

---

# 十一、`author-model-evaluations/`：测量方法

| 路径 | 职责 |
|---|---|
| `README.md` | 六类核心指标与 held-out 隔离。 |

## `evaluation-rubrics/`

- `source-trait-fidelity-rubric.md`
- `independent-persona-consistency-rubric.md`
- `source-author-leakage-rubric.md`
- `originality-and-non-copying-rubric.md`
- `cross-persona-distinction-rubric.md`
- `factuality-and-scene-authorization-rubric.md`

## Evaluation case directories

- `calibration-evaluation-cases/README.md` — 开发期可见题。
- `held-out-evaluation-cases/README.md` — 只说明接口；真实 held-out 内容不在 writer repo。
- `adversarial-evaluation-cases/README.md` — 冒充、泄漏、伪造与 gate bypass 压力测试。
- `runtime-comparison-reports/README.md` — 同条件比较 runtime。

---

# 十二、`author-model-experiments/`：正式实验对象

| 路径 | 职责 |
|---|---|
| `README.md` | 区分 experiment、work item 与 evaluation。 |
| `AGENTS.md` | blind evaluation、held-out 隔离、失败记录保留。 |

## `experiment-scaffold-template/`

- `experiment-manifest.json` — hypothesis 路径、controlled execution、四个 conditions、held-out URI、run/result/conclusion 路径。
- `hypothesis.md` — 第一轮 B/C distinction 假设模板。
- `controlled-inputs/README.md` — common brief、research pack 和 task set；不放 held-out。
- `runtime-run-records/README.md` — 每 condition/repetition 的 immutable run record 要求。
- `failure-cases/README.md` — leakage、fabrication、persona collapse、evaluator disagreement 与 exclusions。
- `raw-evaluation-results.jsonl` — blind code、evaluator、scores 与 notes；sample 状态为 not-run。
- `aggregate-analysis.json` — condition summary、agreement、excluded/failure counts 与 conclusion support。
- `experiment-conclusion.md` — 只有 raw results 与 aggregate analysis 存在后才能写。

标准四条件：

- generic runtime baseline；
- source-model-direct baseline；
- Derived Author B；
- Derived Author C。

共享 controlled execution 记录 runtime/runbook 版本、model parameters、context budget、tool permissions、repetition count 与 randomness control。

---

# 十三、`derived-author-comparisons/`：受控比较报告

- `README.md` — 比较报告是 evaluation asset，不是写作 prompt。
- `source-author-model-versus-derived-author-sample-b/README.md`
- `source-author-model-versus-derived-author-sample-c/README.md`
- `derived-author-sample-b-versus-derived-author-sample-c/README.md`

---

# 十四、`writing-work-items/`：具体生产中心

| 路径 | 职责 |
|---|---|
| `README.md` | 一个 work item 一个完整目录。 |
| `AGENTS.md` | 先读 state、草稿不可覆盖、gate 不可跳过、run 必须记录。 |
| `2026-writing-work-items/` | 年度归档容器，不改变状态机。 |

## `2026-001-sample-article/`

- `work-item-state.json` — lifecycle、stage executions、quality gates、persona/model/runbook/runtime 版本与 publication。
- `writing-brief.md` — 任务、受众、目的、材料、禁区和出版目标。
- `writing-run-manifest.json` — sample 明确为 not-run；真实 run 必须记录 commit、版本、参数、context、工具、loaded file hashes、outputs 和 exit status。
- `research-pack.md` — 当前文章事实与分析材料。
- `work-item-source-register.jsonl` — 当前文章使用来源。
- `article-plan.md` — 判断、证据顺序、段落功能、风险和结尾。
- `draft-01.md` — 第一版不可覆盖草稿。
- `draft-02-after-review.md` — 审核后新版本。
- `factual-review-result.json` — 结构化事实审核。
- `style-review-result.json` — persona/style/leakage/originality/distinction 审核。
- `editor-review.md` — 人类编辑决定。
- `final-approved-article.md` — 只有 state/gates 批准后才具有 approved 意义。

---

# 十五、`approved-publications/`：canonical 出版物

| 路径 | 职责 |
|---|---|
| `README.md` | 只有 gate 通过内容可以进入。 |
| `AGENTS.md` | 强制 transactional publication。 |
| `approved-publication-manifest.jsonl` | canonical publication 索引；当前只有 withdrawn sample placeholder。 |
| `researched-essays/README.md` | 研究型散文分类。 |
| `short-public-commentaries/README.md` | 短公共评论分类。 |
| `authorized-life-writing/README.md` | 场景授权生活写作。 |
| `book-length-projects/README.md` | canonical manuscript 与版本元数据。 |
| `editorial-collections/README.md` | 专题集、选集与编排关系。 |

正式发布只能通过 `publish_approved_writing_work_item.py`。`build_approved_publication_manifest.py` 也会重新执行 publication gate，而不只是汇总 metadata。

---

# 十六、`publication-site/`：可选展示层

- `README.md` — 网站只读取 approved publications，不控制研究结构。
- `publication-site-configuration.json` — site ID、generator、canonical directory、output 与允许状态。

当前为 Optional / Example，不属于第一场作者模型实验的必要核心。

---

# 十七、`repository-automation-scripts/`：执行与验证工具

| 文件 | 职责 |
|---|---|
| `README.md` | 脚本总览与使用边界。 |
| `validate_author_lab_repository_structure.py` | 按 project manifest 与 persona template 验证必需路径。 |
| `validate_json_and_jsonl_documents.py` | 基础 JSON/JSONL 语法。 |
| `validate_machine_readable_contracts.py` | registry-driven JSON Schema；拒绝未注册 machine documents。 |
| `validate_repository_cross_references.py` | source、model、persona、runbook、runtime、work item、experiment、publication 的 ID/version/path/artifact 关系。 |
| `validate_source_research_and_model_provenance.py` | segment → research claim → source-model rule/model file。 |
| `validate_policy_rule_references.py` | 扫描未知 policy IDs。 |
| `validate_writing_work_item_state.py` | lifecycle、stage 与 gate 关系。 |
| `validate_writing_run_reproducibility.py` | completed run 的版本、loaded file hash 与 output artifact。 |
| `validate_sample_comment_markers.py` | reference-sample / active-author-lab 双模式 placeholder。 |
| `create_new_derived_author_persona.py` | 从 complete persona template 生成完整 persona。 |
| `create_new_writing_work_item.py` | 从 runbook、persona model 和 runtime 生成完整 work item。 |
| `create_new_author_model_experiment.py` | 建立四条件 controlled experiment scaffold。 |
| `rebuild_derived_author_indexes.py` | 从 canonical work/publication 重建 persona indexes。 |
| `normalize_authorized_plain_text_source.py` | 生成 versioned segments 与 location map。 |
| `publication_gate_support.py` | publication 共享验证、manifest serialization 与 gate helpers。 |
| `publish_approved_writing_work_item.py` | staging、canonical copy、metadata、manifest/state 更新和 rollback。 |
| `build_approved_publication_manifest.py` | 验证 metadata 与 gates 后重建 manifest。 |

---

# 十八、`repository-validation-tests/`：行为回归测试

- `README.md` — 测试范围说明。
- `test_repository_structure_validation.py`
- `test_json_and_jsonl_document_validation.py`
- `test_machine_readable_contract_validation.py`
- `test_pre_real_run_contracts.py`
- `test_sample_comment_marker_validation.py`
- `test_writing_work_item_state_machine.py`
- `test_authorized_plain_text_normalization.py`
- `test_author_model_experiment_scaffolding.py`
- `test_transactional_publication_gate.py`
- `test_derived_author_index_rebuilding.py`
- `test_policy_rule_references.py`
- `test_runbook_driven_work_item_scaffolding.py`
- `test_complete_derived_author_persona_scaffolding.py`
- `test_source_research_and_model_provenance_validation.py`
- `test_writing_run_reproducibility_validation.py`

这些测试覆盖“合同是否真的影响行为”，而不只检查文件存在。

---

# 十九、`.github/`：协作与 CI

| 路径 | 职责 |
|---|---|
| `.github/workflows/validate-author-lab-repository.yml` | 依次运行结构、语法、schema、cross-reference、provenance、policy、state、run reproducibility、placeholder 和 pytest。 |
| `.github/CODEOWNERS` | 关键目录责任人。 |
| `.github/PULL_REQUEST_TEMPLATE.md` | 变更层次、证据、schema/test 和验证确认。 |
| `.github/ISSUE_TEMPLATE/source-author-research-claim.yml` | 提出或修订 research claim。 |
| `.github/ISSUE_TEMPLATE/derived-author-model-change.yml` | persona/lineage/model/boundary 变更。 |
| `.github/ISSUE_TEMPLATE/repository-validation-problem.yml` | schema、validator、state 与 CI 问题。 |

---

# 二十、角色读取路径

## Corpus curator

`RIGHTS-AND-LICENSING-POLICY.md` → root/source AGENTS → profile → corpus/rights/storage registers → material-type README → normalization script。

## Source-author researcher

Profile → corpus manifest → versioned segment maps → research methodology → evidence register。输出 claim、counterexample、confidence；不得读取 derived output 作为证据。

## Source-model curator

Accepted claims → comprehensive report/limitations → provenance register → source model core/modes/load map。

## Derived-author designer

Source model → derivation methodology → complete persona template → lineage/derivation/core/modes/boundaries。

## Writer

Work-item state → selected persona manifest/lineage/derivation → load map core + one genre → runbook → brief/research/source register。禁止 held-out 与其他 persona memory。

## Factual reviewer

Draft → research pack/source register → factuality policy/schema；不加载不必要的 style prompt。

## Style reviewer

Draft → selected persona/derivation/model → rubrics；不修改事实，不读取 held-out 作为写作提示。

## Editor

完整 work item、两类 review、必要 persona/model；写 editor review 并决定 gate。

## Publisher

只调用 transactional publication command；不手工复制正文。

## Evaluator

读取 blind pack、rubrics、outputs；真实 held-out 位于 evaluator-only storage。

## Runtime maintainer

修改 adapters、execution records、tools、CI；不得修改作者身份以适配 runtime。

---

# 二十一、四类新增工作的标准顺序

## 新增真实源作者

1. 创建 source-author 目录、profile、bibliography、rights 和 corpus manifest；
2. 把原始材料登记到 external storage；
3. 记录 checksum、rights 与 ingestion；
4. 生成 versioned normalized text 与 segment map；
5. 建立 research directory 和 claim register；
6. claim 通过后建立 source model 与 provenance；
7. 更新 project manifest/component status；
8. 运行完整 CI。

## 新增派生作者

1. 调用 persona generator；
2. 完成 lineage 与五类 derivation 文件；
3. 完成 core、genre、boundaries、uncertainties；
4. 保持独立 memory/indexes；
5. 完成 calibration/adversarial evaluation 后再进入真实生产。

## 新增 work item

1. 选择 persona、runbook、runtime；
2. 调用 runbook-driven scaffolder；
3. 完成 brief/research/source register/plan；
4. 每次模型运行写 reproducible run manifest；
5. 生成不可覆盖 draft；
6. 依次通过 factual、persona/style、editor gates；
7. approved 后才进入 publication preparation。

## 新增 experiment

1. 调用 experiment generator；
2. 锁定 shared controlled inputs 与 controlled execution；
3. 把真实 held-out pack 放到 evaluator-only storage；
4. 按 condition × repetition 写 immutable run records；
5. 盲评并保留失败、排除和 disagreement；
6. 生成 aggregate analysis；
7. 最后写 conclusion，并根据失败修改架构。

---

# 二十二、最终判定

这套仓库已经不是只有目录的“实验室宪法”：schema、cross-reference、provenance、state、scaffolding、run reproducibility、experiment controls 与 publication transaction 已进入执行链。

它仍不是一次已经完成的真实实验。当前正确状态是：

```text
Reference architecture: complete
Executable pre-real-run core: complete
Real source content: not started
Real A→B/C controlled experiment: not run
Experimental validation: false
Production publications: none
```

下一阶段不应继续横向扩目录，而应选择一个有限真实 corpus、一个主要 runtime 和一组固定任务，运行第一场受控实验。
