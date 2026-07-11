# Author Lab 真实实跑前完整仓库设计

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

## 目标

把当前 reference scaffold 直接升级为“真实实验开始前的完整仓库”：目录边界不推翻，机器合同真正执行，脚手架与规范共用同一权威来源，资料存储安全，工作项状态可复现，发布成为端到端事务，并为第一场 A→B/C 受控实验准备正式接口。

本次不运行真实实验，不生成虚假的实验结果，不继续增加更多 runtime、文类或出版类型，也不采用并存的旧版/新版目录。

## 完成标准

完成后仓库必须做到：

1. JSON/JSONL 不只可解析，还会按路径匹配对应 JSON Schema。
2. 项目 manifest、source author、source model、derived author、runbook、runtime、work item 和 publication 的跨文件引用会被验证。
3. `lifecycle_status`、`stage_executions`、`quality_gates` 三种状态分开记录。
4. work-item scaffolder 从 runbook manifest 建立工件，不再硬编码另一套文件名。
5. persona scaffolder 从正式 persona template 建立完整结构，validator 也读取同一模板。
6. structure validator 从 project manifest 发现对象，不硬编码 Sample A/B/C。
7. 原始版权材料默认使用仓库外 storage URI，Git 忽略实际 primary-source-materials 二进制内容。
8. source segment ID 明确带 edition 与 segmentation version，不再声称顺序号跨分段稳定。
9. placeholder 规则由 repository mode 与 registry 控制，sample 和 active lab 使用不同语义。
10. publication 操作验证 work item、三项 gate、final 文件、metadata、persona 和 model version 后才写入 canonical publication。
11. 组件明确标记 Core、Optional、Example 与实现状态，目录存在不再等同于已经可运行。
12. `author-model-experiments/` 成为一等对象，但 held-out 真实材料只允许使用 evaluator-only 外部 URI。

## 权威关系

```text
project manifest
  → 发现 source authors、source models、personas、harness、runtime、work items、experiments、publications

schema registry
  → 决定每类机器文档使用哪个 schema

persona template manifest
  → 决定新 persona 的完整必需结构

runbook manifest
  → 决定新 work item 的 stages 与 required artifacts

work-item state
  → 分开记录 lifecycle、stage execution、quality gates

publication transaction
  → 只从 approved work item 产生 canonical publication
```

## 组件范围

### Core

- source materials、rights 与 storage register
- source-author research 与 provenance
- source-author model
- derived-author persona 与完整模板
- shared harness、schema registry、runbooks、policies
- one-way work-item lifecycle
- evaluations 与 experiment contract
- publication gate
- repository validation、tests、CI

### Optional

- additional runtime adapters
- publication site
- persona-specific generated views
- book-length publication categories

### Example

- Sample Source Author
- Sample B 与 Sample C
- sample work item
- sample withdrawn publication record
- experiment scaffold template

## 不做的事情

- 不引入多个并存 schema 版本或迁移目录。
- 不创建真实作者研究结论。
- 不创建看似真实的 B/C 实验得分。
- 不把五个 runtime 都伪装成已实现。
- 不把 held-out 题目放进 writer 可读仓库。
- 不建立网站实现。
