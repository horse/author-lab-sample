# Author Lab Sample

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

`author-lab-sample` 是一套面向真实作者研究、源作者模型编译、多个独立派生作者、受控写作、评测与编辑出版的参考仓库。

它已经完成“真实实跑前”的结构与执行整备，但尚未填入真实作者资料，也尚未运行第一场正式 A→B/C 对照实验。

## 当前状态

| 层次 | 状态 | 含义 |
|---|---|---|
| Reference architecture | 完整 | 核心、可选与示例组件的目录和责任边界已经建立 |
| Executable contracts | 完整 | JSON Schema、跨引用、状态机、脚手架和出版门进入 CI |
| Source-material safety | 完整 | 原始版权材料默认使用仓库外 URI，并受到 Git ignore 与 rights/storage register 约束 |
| Work-item execution core | 实跑前完整 | runbook 决定 stages 与工件；lifecycle、stage execution、quality gate 分开记录 |
| Persona scaffolding | 实跑前完整 | 新派生作者由一个完整模板生成，不再与 Sample B/C 分别演化 |
| Experiment interface | 实跑前完整 | 已有四条件实验对象和 evaluator-only held-out 边界，但没有真实结果 |
| Runtime adapters | 示例/可选 | 配置结构存在，但尚未声称五种 runtime 都已端到端实现 |
| Real author research | 未开始 | Sample 文件不构成真实研究结论 |
| Controlled A→B/C experiment | 未运行 | 仓库中没有虚构的 run、评分或结论 |
| Production publication | 未发生 | 当前 publication 记录是 withdrawn sample placeholder |

组件的机器状态以 `repository-component-status-register.json` 为准。目录存在不等于组件已经实验验证或可生产使用。

## 单向数据流

```text
source materials
  → source-author research
  → source-author model
  → derived-author design and model
  → writing work item
  → factual, style, and editorial gates
  → approved publication
```

生成文本不得反向成为源作者证据；一个派生作者的记忆不得自动进入另一个派生作者；runtime 配置不得决定作者人格。

## 核心目录

- `source-authors/` — 真实源作者资料、rights、storage 与规范化定位。
- `source-author-research/` — 有证据 ID、反例和置信度的源作者研究。
- `source-author-models/` — 从已接受研究编译的紧凑可加载模型。
- `derived-author-personas/` — 拥有独立 lineage、derivation、model、memory 和索引的化名作者。
- `shared-writing-harness/` — schema registry、runbook、policy、prompt、模板和 persona scaffold template。
- `runtime-adapters/` — 运行环境配置，不携带作者知识。
- `writing-work-items/` — 一次写作的 brief、research、plan、草稿、审核、状态与运行记录。
- `author-model-evaluations/` — 评测标准、校准题和 evaluator 边界。
- `author-model-experiments/` — 假设、控制条件、运行记录、盲评、失败案例和结论。
- `approved-publications/` — 只接受通过事务性 publication gate 的 canonical 内容。
- `repository-automation-scripts/` 与 `repository-validation-tests/` — 验证、脚手架、索引、规范化和发布工具。

完整逐文件说明见：

`documentation/complete-repository-file-and-directory-reference.md`

## 仓库模式

- `reference-sample`：所有受管文本文件都必须保留 sample marker，用于展示完整结构。
- `active-author-lab`：只有 `repository-placeholder-register.json` 登记的未完成文件可以保留 marker；已完成生产文件不得残留 marker。

这使 sample 可以逐文件转化为真实项目，而不需要先关闭 CI。

## 验证

```bash
python -m pip install -e '.[development]'
python repository-automation-scripts/validate_author_lab_repository_structure.py
python repository-automation-scripts/validate_json_and_jsonl_documents.py
python repository-automation-scripts/validate_machine_readable_contracts.py
python repository-automation-scripts/validate_repository_cross_references.py
python repository-automation-scripts/validate_writing_work_item_state.py
python repository-automation-scripts/validate_sample_comment_markers.py
pytest repository-validation-tests
```

任何 agent 修改仓库前都必须先读根级与所在目录的 `AGENTS.md`。
