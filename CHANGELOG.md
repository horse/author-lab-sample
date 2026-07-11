# Changelog

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

## 2026-07-11 — Canonical template freeze and new-project bootstrap

本次明确 `author-lab-sample` 的长期身份：它是 Author Lab 的 canonical reference template，不承载任何真实作者资料、研究、派生作者、运行结果、评测结果或生产出版物。

### Template governance

- 新增 `documentation/template-repository-governance-and-backup.md`。
- 规定真实项目必须通过 GitHub `Use this template` 创建独立 repository，然后在新仓库转换为 `active-author-lab`。
- 规定 sample 本身长期保持 `reference-sample`。
- 说明 `main` Ruleset、冻结标签、外部 Git mirror 和 GitHub 平台设置备份。
- 明确当前 canonical template 不应 archive；需要只读档案时应创建独立 archive repository。

### Owner-only settings

- 新增 `.github/OWNER-TEMPLATE-LOCK-CHECKLIST.md`。
- Template repository、branch/tag rulesets、snapshot tag 与 mirror backup 只有在 GitHub UI 或受信任电脑实际执行并核验后才能勾选。
- 文档描述目标设置不等于设置已经生效，agent 不得误报。

### New-project bootstrap

- 新增 `documentation/new-author-lab-project-bootstrap-prompt.md`。
- 提供可直接复制到新 ChatGPT 对话的完整 prompt。
- Prompt 要求 sample 只读、target repository 独立、active mode 转换、sample 数据清理、真实 source-author 骨架、仓库外材料存储、branch/PR/CI、项目 handoff 和 owner settings checklist。
- 明确在真实材料不足时必须保留空 register 或 not-started 状态，不得编造 research、model、persona、run、evaluation 或 publication。

## 2026-07-11 — 外部审查阻塞项完整修复

本次直接修复“真实实跑前完整仓库”中仍未闭合的执行合同，不建立并存的新目录或兼容旧合同。

### Repository mode 与原子脚手架

- 新增共享 `repository_mode_support.py`，所有 generator 根据 `reference-sample` / `active-author-lab` 输出对应 marker、status 与空记录。
- Active mode 不再生成 sample marker、sample status、fake checksum 或 `SAMPLE-*` sentinel。
- 新增 `atomic_repository_update.py`；persona、work item 与 experiment 全部先在临时 sibling directory 完整生成，再原子进入 canonical path。
- Persona generator 验证 exact source-model ID/version，并自动更新 project manifest 与 component status register；失败时不留下半 persona。

### Author-scoped provenance

- Research claim 增加 `source_author_id`，source-model provenance 增加 `source_author_id` 与 `source_author_model_id`。
- Segment、claim 与 model rule 按 source author 建立独立 namespace。
- 跨作者 segment/claim reference 会失败。
- Approved model rule 只能引用 accepted research claim。

### Exact experiment conditions

- 每个 condition 固定 persona、author model 与 source-author model 的 exact ID/version。
- Generic baseline 禁止加载任何 author data。
- Source-direct baseline 必须锁定 exact source model。
- Derived Author B/C 必须是不同 persona，并分别锁定 exact derived model 与 upstream source model。
- Active experiment 的 raw evaluation result 起始为真正空 JSONL，不再生成 fake not-run record。

### Immutable writing-run history

- 删除旧单一 `writing-run-manifest.json`。
- 每次运行使用 `writing-runs/run-*.json`，输出位于 `writing-runs/<run-id>/`。
- Validator 通过 `git show <repository_commit_sha>:<path>` 验证历史输入 hash，而不是把旧 run 与当前 HEAD 比较。
- 增加 duplicate run ID、unknown commit、path traversal 与非 run-scoped output 检查。

### Lifecycle

- 增加 `rejected`、`cancelled`、`abandoned` 与 `superseded`。
- Archived work item 必须有 `archive_reason`，但不要求伪造已经通过的 gates。
- Publication linkage 改为 typed object。

### Recoverable publication transaction

- 零出版物由空 `approved-publication-manifest.jsonl` 表示；删除绑定 Sample B 的假 sentinel record。
- Publication command 增加 lock、transaction journal、staging、backup、recovery 与 rollback。
- Manifest、work-item state 与 persona indexes 在提交前统一预计算并联合替换。
- Canonical article 的 SHA-256 必须与 work-item final approved article 一致。
- 新增独立 `validate_publication_integrity.py`，手工复制文章或编辑 manifest/indexes 无法绕过 CI。

### CI 与依赖

- GitHub Actions 固定到 commit SHA。
- Checkout 使用 full history，以验证 commit-pinned run inputs。
- 新增 `validation-constraints.txt` 固定验证依赖版本。
- CI 增加 publication integrity 和 Ruff。
- 失败时上传 placeholder、Ruff 与 pytest diagnostics。
- README、AGENTS 与 CI 使用同一套完整验证顺序。

### Regression coverage

新增或扩展测试覆盖：

- active-mode persona/work-item/experiment/publication；
- persona source-model resolution、registration 与 atomic cleanup；
- author-scoped provenance 和 accepted-claim gate；
- exact experiment model pinning 与 B/C distinction；
- multiple immutable runs 与 historical Git hashes；
- unsuccessful lifecycle 与 archive reason；
- publication staging cleanup、journal recovery、empty manifest、manual bypass 与 stale indexes。

## 2026-07-11 — 真实实跑前完整仓库

本次不是建立并存的新版本，而是把原有 sample scaffold 直接升级为真实实验开始前的完整参考实现。

### Repository control plane

- 根 manifest 增加 repository mode、readiness status、component、placeholder、storage、schema、persona template、policy 与 experiment 入口。
- 新增 Core / Optional / Example 组件分类。
- 组件状态区分 implementation、validation、infrastructure production readiness、real content status 与 experimental validation。
- Structure validator 改为从 manifest 发现 source author、source model 与 persona，不再硬编码 Sample A/B/C。

### Machine-readable contracts

- 建立 path pattern → JSON Schema 的 executable document registry。
- 未注册的生产型 JSON/JSONL 会失败；schema definitions 与 artifact templates 必须显式分类。
- 为 rights、storage、corpus、segments、research claims、source-model provenance、derived models、loading maps、persona indexes、work sources、work state、run records、experiment、evaluation、publication 与 site config 建立 schema。
- 增加跨文件 ID、版本、路径和工件验证。

### Source evidence and research

- 原始版权材料默认使用 `private-storage://` 或明确授权的 `repository-storage://` URI。
- `.gitignore` 阻止 primary-source binaries 进入普通 Git history，同时保留目录 README。
- Corpus、rights 和 storage register 必须对 source ID、URI、rights status 和 segmentation version 保持一致。
- 规范化文本使用 edition、segmentation version、ordinal 与 SHA-256 组成的 segment identity，并生成 location map。
- 增加 segment → research claim → source-model provenance chain validation。

### Derived authors and scaffolding

- 建立 complete derived-author persona template manifest。
- Persona generator 从模板一次生成 lineage、derivation、core model、genre modes、memory、harness overlay 和生成式 indexes。
- Sample B/C 与 generator、structure validator 共享同一结构合同。
- Persona 内部 work/publication 目录改为 canonical root records 的生成索引，不再允许第二套正文。

### Work items and runs

- `lifecycle_status`、`stage_executions` 与 `quality_gates` 分开。
- Runbook manifest 成为 stages、required artifacts、artifact templates 与 policy rules 的唯一权威来源。
- Work-item scaffolder 解析 persona model、runbook 和 runtime 的 ID 与版本，并按 runbook 创建工件。
- Writing run 记录 commit SHA、model/runbook/runtime 版本、参数、context budget、工具权限、加载文件 hash、输出工件与 exit status。

### Policy and agent behavior

- 建立 canonical policy-rule register。
- AGENTS、skills、prompts 与 runbooks 引用 policy IDs，而不是分别维护不同版本的同一规则。
- CI 扫描所有 policy references，未知规则 ID 会失败。
- Repository placeholder validation 区分 reference-sample 与 active-author-lab。

### Experiments

- `author-model-experiments/` 成为一等对象。
- 标准 scaffold 包含 generic baseline、source-model-direct baseline、Derived Author B 与 C 四个条件。
- Runtime/runbook 版本、模型参数、context budget、工具权限、重复次数和 randomness control 成为共享 controlled execution contract。
- Real held-out material 必须使用 `evaluator-storage://`。

### Publication

- 新增 transactional publication command。
- 事实、persona/style、编辑、final file、persona/model 版本与 metadata 全部通过后，才会写入 canonical publication。

## 2026-07-11 — Initial reference scaffold

- 建立 source-author research、source models、derived authors、shared harness、runtime adapters、evaluations、work items 与 publications 的完整参考目录。
