# Changelog

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

## 2026-07-11 — 真实实跑前完整仓库

本次不是建立并存的新版本，而是把原有 sample scaffold 直接升级为真实实验开始前的完整参考实现。

### Repository control plane

- 根 manifest 增加 repository mode、readiness status、component、placeholder、storage、schema、persona template、policy 与 experiment 入口。
- 新增 Core / Optional / Example 组件分类。
- 组件状态区分 implementation、validation、infrastructure production readiness、real content status 与 experimental validation。
- structure validator 改为从 manifest 发现 source author、source model 与 persona，不再硬编码 Sample A/B/C。

### Machine-readable contracts

- 建立 path pattern → JSON Schema 的 executable document registry。
- 未注册的生产型 JSON/JSONL 会失败；schema definitions 与 artifact templates 必须显式分类。
- 为 rights、storage、corpus、segments、research claims、source-model provenance、derived models、loading maps、persona indexes、work sources、work state、run records、experiment、evaluation、publication 与 site config 建立 schema。
- 增加跨文件 ID、版本、路径和工件验证。

### Source evidence and research

- 原始版权材料默认使用 `private-storage://` 或明确授权的 `repository-storage://` URI。
- `.gitignore` 阻止 primary-source binaries 进入普通 Git history，同时保留目录 README。
- corpus、rights 和 storage register 必须对 source ID、URI、rights status 和 segmentation version 保持一致。
- 规范化文本使用 edition、segmentation version、ordinal 与 SHA-256 组成的 segment identity，并生成 location map。
- 增加 segment → research claim → source-model provenance chain validation。

### Derived authors and scaffolding

- 建立 complete derived-author persona template manifest。
- persona generator 从模板一次生成 lineage、derivation、core model、genre modes、memory、harness overlay 和生成式 indexes。
- Sample B/C 与 generator、structure validator 共享同一结构合同。
- persona 内部 work/publication 目录改为 canonical root records 的生成索引，不再允许第二套正文。

### Work items and runs

- `lifecycle_status`、`stage_executions` 与 `quality_gates` 分开。
- runbook manifest 成为 stages、required artifacts、artifact templates 与 policy rules 的唯一权威来源。
- work-item scaffolder 解析 persona model、runbook 和 runtime 的 ID 与版本，并按 runbook 创建工件。
- writing run manifest 记录 commit SHA、model/runbook/runtime 版本、参数、context budget、工具权限、加载文件 hash、输出工件与 exit status。
- 增加 completed run 的版本、hash 和输出可复现性验证。

### Policy and agent behavior

- 建立 canonical policy-rule register。
- AGENTS、skills、prompts 与 runbooks 引用 policy IDs，而不是分别维护不同版本的同一规则。
- CI 扫描所有 policy references，未知规则 ID 会失败。
- repository placeholder validation 区分 reference-sample 与 active-author-lab；真实项目可以逐文件完成而不必先关闭 CI。

### Experiments

- `author-model-experiments/` 成为一等对象。
- 标准 scaffold 包含 generic baseline、source-model-direct baseline、Derived Author B 与 C 四个条件。
- runtime/runbook 版本、模型参数、context budget、工具权限、重复次数和 randomness control 成为共享 controlled execution contract。
- real held-out material 必须使用 `evaluator-storage://`，不能进入 writer-readable repository。
- experiment runtime runs、raw evaluation results、aggregate analysis、failure cases 与 conclusion 均有正式接口，但 sample 不制造真实结果。

### Publication

- 新增 transactional publication command。
- 事实、persona/style、编辑、final file、persona/model 版本与 metadata 全部通过后，才会写入 canonical publication。
- publication 在 staging 中准备；失败会回滚 canonical directory、manifest 与 work-item state。
- publication manifest builder 现在执行 gate validation，而不只是汇总 JSON。

### Continuous integration

CI 依次执行：

1. manifest-driven structure validation；
2. JSON/JSONL syntax；
3. registered JSON Schema contracts；
4. repository cross references；
5. source research/model provenance；
6. policy rule references；
7. work-item state；
8. writing run reproducibility；
9. repository-mode-aware placeholders；
10. pytest。

## 2026-07-11 — Initial reference scaffold

- 建立 source-author research、source models、derived authors、shared harness、runtime adapters、evaluations、work items 与 publications 的完整参考目录。
