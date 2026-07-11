# New Author Lab Project Bootstrap Prompt

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本文提供一个可以直接复制到新 ChatGPT 对话中的启动提示词，用于把 `horse/author-lab-sample` 创建成一个独立、真实、可持续维护的 Author Lab 项目。

## 使用前的唯一手工步骤

先在 GitHub 打开 canonical sample：

```text
https://github.com/horse/author-lab-sample
```

点击：

```text
Use this template
→ Create a new repository
```

不要选择 `Include all branches`。创建后，把新仓库 URL 填入下面提示词的 `TARGET_REPOSITORY`。

当前 GitHub agent connector 未必具备创建 repository 或开启 Ruleset 的权限，因此不要让新对话直接修改 sample，也不要假设它可以替你创建目标仓库。

## 需要替换的字段

```text
TARGET_REPOSITORY
PROJECT_ID
PROJECT_DISPLAY_NAME
SOURCE_AUTHOR_ID
SOURCE_AUTHOR_DISPLAY_NAME
PRIMARY_LANGUAGE
SOURCE_LANGUAGES
PROJECT_VISIBILITY
PRIVATE_STORAGE_NAMESPACE
```

推荐：

```text
PROJECT_ID = author-<descriptive-slug>-lab
SOURCE_AUTHOR_ID = source-author-<descriptive-slug>
PRIVATE_STORAGE_NAMESPACE = private-storage://<project-id>
```

## 完整启动提示词

复制下面全部内容到一个新对话，并替换方括号字段。

---

```text
/goal

你现在负责建立一个新的、真实的 Author Lab 项目仓库。请把这项工作作为一个连续的仓库建设任务推进，直到目标仓库在 main 上完成转换、文档齐全、完整 CI 通过，并留下足够的 agent handoff 信息。不要在后台承诺以后完成；在当前会话中逐步执行、验证并汇报。

CANONICAL_SAMPLE_REPOSITORY:
https://github.com/horse/author-lab-sample

TARGET_REPOSITORY:
[https://github.com/<owner>/<new-repository>]

PROJECT_ID:
[author-<project-slug>-lab]

PROJECT_DISPLAY_NAME:
[项目显示名称]

SOURCE_AUTHOR_ID:
[source-author-<author-slug>]

SOURCE_AUTHOR_DISPLAY_NAME:
[源作者正式名称]

PRIMARY_LANGUAGE:
[例如 zh-Hans / zh-Hant / en / ja]

SOURCE_LANGUAGES:
[例如 pl, en]

PROJECT_VISIBILITY:
[private / public]

PRIVATE_STORAGE_NAMESPACE:
[private-storage://<project-id>]

项目目标：
以 canonical sample 为规范架构，在 TARGET_REPOSITORY 中建立一个独立的 active Author Lab。源作者材料、研究、source model、派生作者、写作 work items、运行历史、实验和出版物都只属于 TARGET_REPOSITORY。CANONICAL_SAMPLE_REPOSITORY 只能读取，绝对不能修改。

一、不可违反的边界

1. 首先确认 TARGET_REPOSITORY 与 CANONICAL_SAMPLE_REPOSITORY 不是同一个仓库。若相同，停止写入并明确报告。
2. 不得向 canonical sample 创建 branch、commit、PR、issue、tag 或设置变更。
3. 不建立 v2、new、legacy、next 等并存目录；直接把目标仓库转换为当前真实项目结构。
4. 不得把模型生成内容当作 source-author evidence。
5. 不得编造 source materials、rights、checksum、research claims、source-model rules、derived-author traits、runtime runs、evaluation scores、held-out results 或 publications。
6. 材料不存在时使用真正的空 register、not-started 状态或明确登记的 placeholder，不创建看似真实的 sample record。
7. 受版权限制的 primary source 默认放在仓库外，只在 Git 中保存 private-storage URI、rights、checksum、edition、ingestion 与 segmentation metadata。
8. 不得把 secrets、API keys、private personal data、受限原始文件或 evaluator-only held-out pack 放进 Git。
9. Source Author A、Derived Author B、Derived Author C 必须是不同对象。B/C 不得声称 A 的身份、经历、关系、资格或背书。
10. 在 source research 和 source model 尚未完成前，不要编造 B/C 的人格和文风。可以保留尚未创建的状态，而不是生成空洞伪内容。

二、工作方式

1. 使用 GitHub 连接读取两个仓库：
   - canonical sample 的 README、AGENTS、author-lab-project-manifest、component register、placeholder register、完整目录说明、governance 文档、research methodology、state machine、schemas、validators 和 tests；
   - target repository 的当前 main、branches、PR、Actions 和完整文件状态。
2. 把 canonical sample 视为当前规范，但不要机械复制 sample 数据。
3. 在 TARGET_REPOSITORY 新建一个短期工作分支，例如：
   bootstrap/convert-template-to-active-project
4. 先写一份可执行 implementation plan 到：
   documentation/implementation-plans/<date>-bootstrap-active-author-lab-project.md
5. 在同一分支执行全部转换；不要直接写 main。
6. 每一阶段运行相关 validators/tests，最终运行与 CI 完全相同的完整验证序列。
7. 创建 PR，审查 diff、Actions、review threads 和最终 head SHA。
8. 只有 fresh PR-head 或 merge-ref CI 全绿后才 squash merge。
9. 合并后验证 main 文件树与 PR head 等价，删除工作分支。
10. 不要把“目录存在”描述为“真实研究完成”或“实验已验证”。

三、目标仓库转换任务

A. 项目身份与模式

1. 把 TARGET_REPOSITORY 的 project ID、显示名称、仓库描述和文档改为本项目。
2. 将 `author-lab-project-manifest.json` 的 `repository_mode` 改为 `active-author-lab`。
3. 更新 readiness/status 字段，使其准确表达：
   - repository infrastructure: ready；
   - real source corpus: not started 或按实际状态；
   - source-author research: not started；
   - source-author model: not started；
   - derived authors: not created；
   - controlled experiment: not run；
   - production publication: none。
4. 更新 `repository-placeholder-register.json`：只有真正未完成且必须保留的文件才能登记为 placeholder。
5. Active production files 中不得残留：
   - sample marker；
   - Sample A/B/C ID；
   - `sample-development`；
   - `sample-unreviewed`；
   - `sample-placeholder`；
   - `SAMPLE-NOT-RUN`；
   - `SAMPLE-NOT-PUBLISHED`；
   - `replace-with-real-checksum`。

B. 删除 sample 数据而保留架构

1. 删除或转换 sample source-author、sample research、sample source model、Sample B/C、sample work item、sample experiment 和 sample generated indexes。
2. 保留共享架构、schemas、validators、tests、runbooks、policies、skills、runtime adapter examples 和文档模板。
3. Canonical JSONL 在无记录时使用真正空文件，不写 fake sentinel record。
4. 更新 project manifest 的 source-author/model/persona directory lists，使其只声明实际存在对象。
5. 更新 component status register，明确区分 infrastructure readiness 与 real content status。

C. 建立真实 source-author 项目骨架

1. 使用 SOURCE_AUTHOR_ID 与 SOURCE_AUTHOR_DISPLAY_NAME 建立真实 source-author directory。
2. 创建真实 profile、bibliography、rights register、corpus manifest 和规范化目录结构。
3. 在尚无材料时：
   - rights register 可以为空；
   - corpus manifest 可以为空；
   - normalized text 与 segment map 不得伪造；
   - research claim register 可以为空；
   - source model 不得提前建立为 approved。
4. 把 PRIMARY_LANGUAGE 与 SOURCE_LANGUAGES 写入正确的 profile/project 字段。
5. 建立仓库外材料边界：
   PRIVATE_STORAGE_NAMESPACE/[source-id]
6. 为首次材料 ingestion 写清楚要求：
   - source ID；
   - edition ID；
   - storage URI；
   - rights status；
   - repository copy allowed；
   - SHA-256；
   - normalization status；
   - segmentation version；
   - research readiness。
7. 不上传真实受限二进制来测试目录。

D. 研究、模型与派生作者的准入门

1. Research claim 必须属于 SOURCE_AUTHOR_ID，并引用同一作者的 versioned segment IDs。
2. 只有 accepted claim 可以支持 approved source-model rule。
3. Source model 尚无证据时，保持未创建或 unreviewed，不生成完整人格结论。
4. Derived Author B/C 只能在 exact source model ID/version 存在后，通过 canonical persona generator 创建。
5. B/C 分别建立 independent lineage、derivation、model、memory、work-item index、publication index。
6. 不提前为 B/C 编造 inherited/transformed/rejected/original traits。
7. 在 B/C 尚未建立时，experiment manifest 不得伪造 condition model IDs。

E. 新项目文档与 agent handoff

创建或更新：

1. 根 README：项目定位、当前真实状态、数据流、材料边界、完整验证命令。
2. 根 AGENTS：sample 只读、target 权威层、加载规则、修改规则、运行与发布规则。
3. `documentation/project-bootstrap-record.md`：
   - template 来源；
   - bootstrap 日期；
   - sample commit/tag；
   - target initial commit；
   - 已转换对象；
   - 删除的 sample 对象；
   - 未完成事项。
4. `documentation/project-handoff-and-next-actions.md`：
   - 当前 branch/main/PR/CI 状态；
   - source materials 状态；
   - rights/storage 状态；
   - research/model/persona/experiment/publication 状态；
   - 下一批可执行任务；
   - 明确禁止的推断。
5. CHANGELOG：记录从 reference template 转换为 active project，不建立并存版本。
6. 必要时更新 documentation index 和 complete repository reference 中的项目专属内容，但不要破坏共享架构说明。

F. GitHub 治理

在工具权限允许时检查或设置：

1. default branch = main；
2. block force push；
3. restrict deletion；
4. require PR；
5. require `Validate Author Lab Repository`；
6. require conversation resolution；
7. squash merge；
8. secrets 与 Actions permissions 最小化。

若连接器不能修改设置：

- 不要声称已经完成；
- 创建 `.github/OWNER-ACTIVE-PROJECT-SETTINGS-CHECKLIST.md`；
- 写出 owner 需要执行的最少 UI 步骤。

四、必须通过的验证

最终在 TARGET_REPOSITORY 运行：

python -m pip install -c validation-constraints.txt -e '.[development]'
python repository-automation-scripts/validate_author_lab_repository_structure.py
python repository-automation-scripts/validate_json_and_jsonl_documents.py
python repository-automation-scripts/validate_machine_readable_contracts.py
python repository-automation-scripts/validate_repository_cross_references.py
python repository-automation-scripts/validate_source_research_and_model_provenance.py
python repository-automation-scripts/validate_policy_rule_references.py
python repository-automation-scripts/validate_writing_work_item_state.py
python repository-automation-scripts/validate_writing_run_reproducibility.py
python repository-automation-scripts/validate_publication_integrity.py
python repository-automation-scripts/validate_sample_comment_markers.py
ruff check repository-automation-scripts repository-validation-tests
pytest repository-validation-tests --tb=short

验证必须证明：

1. active production files 不含 sample marker 或 sentinel；
2. project manifest 只声明实际存在对象；
3. source author、research、source model 和 persona ownership 不串线；
4. 空 register 被正确接受；
5. 没有 fake run、evaluation 或 publication；
6. 生成索引能从 canonical objects 重建；
7. 所有 schema、cross references、provenance、state、run、publication 与 tests 通过。

五、完成定义

只有同时满足以下条件，才能宣告 bootstrap 完成：

- TARGET_REPOSITORY 与 sample 完全分离；
- `repository_mode=active-author-lab`；
- sample 数据和 sentinel 已清除；
- 真实 source-author project skeleton 已建立；
- rights/storage/ingestion 边界已写清楚；
- 未编造任何真实研究、模型、persona、run、evaluation 或 publication；
- 项目文档和 handoff 已完成；
- PR diff 已审查；
- fresh CI 全绿；
- 已 squash merge 到 main；
- main 已复核；
- 临时分支已删除；
- owner-only settings 未执行的部分被明确列出。

请先检查仓库和 canonical sample，然后给我一段简洁的执行摘要，接着直接创建分支、写 implementation plan 并推进全部工作。除非遇到权限或安全阻塞，不要停在泛泛规划或反复询问；根据以上明确字段作出保守、可逆、可验证的处理。
```

---

## 目标仓库尚未创建时的简化开头

```text
我要从 https://github.com/horse/author-lab-sample 建立一个新的真实 Author Lab 项目，但目标 GitHub repository 还没有创建。请先告诉我在 GitHub UI 中用 `Use this template` 创建独立 repository 的最少步骤。创建完成后，我会把新仓库 URL 发给你；在此之前不要修改 canonical sample。
```

## 使用提示

新对话开始后，最重要的是提供准确的 `TARGET_REPOSITORY`。源材料尚未整理完成并不妨碍建立项目基础设施；但 agent 必须保留空状态，而不能为了让目录看起来完整而编造研究和 persona 内容。
