# Documentation Directory

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本目录保存 Author Lab 的权威架构、逐文件职责、研究方法、运行合同、政策解释、术语和实施记录。仓库操作边界以根级与局部 `AGENTS.md` 为准；机器接口以 `shared-writing-harness/machine-readable-contracts/` 及其 registry 为准。

## 首先阅读

1. [`complete-repository-file-and-directory-reference.md`](complete-repository-file-and-directory-reference.md) — 当前完整目录、文件职责与实际工作方式的权威说明。
2. [`pre-real-run-remediation-design.md`](pre-real-run-remediation-design.md) — 外部审查后对 active mode、原子脚手架、provenance、实验、运行历史和出版事务的修复设计。
3. [`repository-architecture-and-data-flow.md`](repository-architecture-and-data-flow.md) — 单向数据流、控制平面、机器合同、不可变运行、实验和可恢复出版。
4. [`pre-real-run-complete-repository-design.md`](pre-real-run-complete-repository-design.md) — 最初“真实实跑前完整仓库”的目标、边界和完成标准。
5. [`glossary-of-author-lab-terms.md`](glossary-of-author-lab-terms.md) — 核心术语。

## 当前状态来源

- 根 `README.md` — 面向读者的总体状态与完整验证命令。
- `repository-component-status-register.json` — Core / Optional / Example、实现状态、真实内容状态与实验验证状态。
- `CHANGELOG.md` — 按日期与里程碑记录结构变化，不使用并存的仓库版本体系。
- `author-lab-project-manifest.json` — repository mode、readiness 与所有机器入口。
- `.github/workflows/validate-author-lab-repository.yml` — 实际 CI 顺序。

## 研究与模型方法

- [`source-author-research-methodology.md`](source-author-research-methodology.md) — rights、storage、edition、segmentation、author-scoped research claim 与 accepted-claim provenance gate。
- [`derived-author-creation-methodology.md`](derived-author-creation-methodology.md) — inherited、transformed、rejected、original 与独立派生作者设计。
- [`provenance-and-evidence-policy.md`](provenance-and-evidence-policy.md) — 证据等级与禁止生成物回流。

## 运行、状态、实验与出版

- [`runtime-adapter-contract.md`](runtime-adapter-contract.md) — runtime adapter 的职责边界。
- [`writing-work-item-state-machine.md`](writing-work-item-state-machine.md) — lifecycle、stage execution、quality gates、immutable runs 与 recoverable publication transaction。
- [`publication-and-editorial-approval-policy.md`](publication-and-editorial-approval-policy.md) — 编辑批准与出版门。
- [`naming-versioning-and-file-conventions.md`](naming-versioning-and-file-conventions.md) — 命名、模型版本和文件约定。

实验的 exact model pinning、controlled execution、held-out 边界和结果文件由 `author-model-experiments/README.md`、remediation design 与完整说明书共同解释。

## 实施记录

`implementation-plans/` 保存已执行或正在执行的仓库变更计划。当前修复计划为：

- `2026-07-11-complete-pre-real-run-remediation.md`

计划说明一次变更怎样完成，不取代长期规范，也不代表真实实验结果。
