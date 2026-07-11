# Author Lab 完整目录、文件与工作方式说明

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

本文是 `author-lab-sample` 的权威目录说明书。它解释这套仓库中的每一层为什么存在、由谁读写、接受什么输入、产生什么输出，以及哪些内容绝不能反向流动。

`holonpress/author-zhang` 证明了一个作者仓库需要人格、文风、方法、写作循环、审校和发布机制。本仓库不是对它的目录复制，而是把那类单作者工作空间推广为一套可研究真实源作者、编译源作者模型、建立多个派生作者、运行不同写作流程并保留完整证据链的系统。

---

## 一、仓库的基本对象

本仓库同时管理六种性质不同的对象。使用者必须始终区分它们。

1. **源作者**：真实存在、留下原始作品的作者。
2. **源作者研究**：研究人员根据原始材料形成的解释、判断与证据记录。
3. **源作者模型**：从已接受研究中编译出来、供机器加载的压缩模型。
4. **派生作者**：受到源作者模型影响，但具有独立身份、边界、议题与写作历史的化名作者。
5. **写作工作项**：一次具体写作从 brief、研究、计划、草稿、审核到最终稿的完整记录。
6. **正式出版物**：经过事实审核、文风审核和编辑批准的成品。

它们之间只能按照下面的方向流动：

```text
源作者材料
  → 源作者研究
  → 源作者模型
  → 派生作者设计与模型
  → 写作工作项
  → 评测与编辑审核
  → 正式出版物
```

禁止以下反向污染：

```text
派生作者文章 → 证明源作者具备某种特征
模型生成文本 → 作为源作者研究证据
正式出版物 → 自动写回源作者模型
一个派生作者的记忆 → 自动进入另一个派生作者
runtime 配置 → 决定作者人格或文风
网站目录结构 → 反过来支配研究与出版结构
```

---

## 二、权威层级与读写权限

发生冲突时，按以下顺序判断：

1. `source-authors/` 中的原始证据与权利记录；
2. `source-author-research/` 中有证据编号的研究结论；
3. `source-author-models/` 中已批准、带版本的源作者模型；
4. `derived-author-personas/` 中的谱系、派生设计与独立作者模型；
5. `shared-writing-harness/` 中的工作合同与质量门；
6. `writing-work-items/` 中当前任务的状态与材料；
7. `approved-publications/` 中的正式成品。

每一层都有自己的职责：

| 层级 | 主要写入者 | 主要读取者 | 不允许做什么 |
|---|---|---|---|
| 源材料 | corpus curator | 研究员、规范化脚本 | 覆盖原件、伪造来源 |
| 源作者研究 | author researcher | 模型整理者、审校者 | 使用生成文章作为证据 |
| 源作者模型 | model curator | 派生作者设计者 | 添加无研究依据的人格规则 |
| 派生作者 | persona designer、编辑 | writer、style reviewer | 冒充源作者、继承真实私生活 |
| Harness | 系统设计者 | writer、reviewer、runtime | 写入某个作者的具体人格 |
| Work item | writer、researcher、reviewer | 编辑、publisher | 覆盖已有草稿版本、跳过状态门 |
| Evaluations | evaluator | 模型整理者、编辑 | 直接被 writer 当作提示词 |
| Publications | publisher | 网站、读者、编辑 | 接收未批准草稿 |

---

# 三、仓库根目录

## `README.md`

人类进入仓库时的第一入口。它只负责介绍项目是什么、顶层目录怎样分工、如何执行验证，不承载完整作者模型或所有操作规则。新成员先读它，再进入本文与 `AGENTS.md`。

## `AGENTS.md`

所有 agent 的根级操作规则。它定义默认模式是“仓库维护”，而不是“扮演某个作者”；定义权威层级、加载规则、修改规则、命名规则和完成前验证。任何子目录中的 `AGENTS.md` 只能收紧或补充根规则，不能取消根级安全边界。

## `author-lab-project-manifest.json`

整个仓库的机器入口。记录项目 ID、项目类型、默认语言、源作者目录、源作者模型目录、派生作者目录、共享 harness、工作项、出版物以及权利政策的位置。程序需要发现仓库资产时先读取它，不应通过猜目录名工作。

## `RIGHTS-AND-LICENSING-POLICY.md`

规定 EPUB、PDF、图片、音频、私人信件、研究笔记、代码、模型和出版物的权利处理方式。它提醒维护者：材料被登记不等于获得再分发许可；私有研究材料与可公开代码可能需要不同许可。

## `ETHICS-AND-DERIVATION-DISCLOSURE-POLICY.md`

规定派生作者与源作者的伦理边界。派生作者不得声称源作者身份、私人经验、关系、创伤、资历或授权；高度可识别的原句必须引用而不能伪装为派生作者原创。

## `CHANGELOG.md`

记录仓库架构、schema、模型、runbook 和重要行为的版本变化。日常文章修改通常不必进入此文件；会影响其他 agent 或程序理解方式的变化必须记录。

## `CONTRIBUTING.md`

说明贡献方式、分支和 PR 习惯、研究证据要求、schema 与测试同步要求，以及何时必须更新派生谱系。它服务于人类贡献者和负责修改仓库的 agent。

## `SECURITY.md`

规定密钥、私人信件、未公开稿件、个人信息和受限制原始材料的安全处理方式。任何意外泄漏必须先移除、轮换密钥并通知仓库所有者，而不是仅追加一个删除提交。

## `.gitignore`

排除 Python 缓存、虚拟环境、环境变量文件、构建产物、本地原始材料、私密材料、runtime secrets 和网站生成结果。这里定义“哪些文件不应该进入 Git”，不是定义材料是否存在。

## `.gitattributes`

统一文本换行，并将 EPUB、PDF、图片、音频和视频视为二进制。真实项目如需要 Git LFS，可在此基础上增加 LFS 规则。

## `.editorconfig`

统一 UTF-8、LF、末尾换行、空格缩进和 Markdown 空格保留规则，减少不同编辑器造成的无意义差异。

## `pyproject.toml`

定义仓库验证工具的 Python 包信息、Python 最低版本、`jsonschema`、pytest 和 ruff 依赖，以及测试目录。它属于仓库工程层，不属于任何作者模型。

## `.pre-commit-config.yaml`

定义提交前自动检查：JSON、YAML、文件末尾、尾随空格和 Python 格式。实际使用前应在本地安装 `pre-commit`。

---

# 四、`documentation/`：项目方法与操作文档

这个目录解释系统本身。它不存储某个作者的人格结论，也不存储某篇文章的工作记录。

## `documentation/README.md`

文档索引。新成员应通过它找到本说明书、架构、研究方法、派生方法、证据政策、出版政策、runtime 合同、状态机和术语表。

## `documentation/complete-repository-file-and-directory-reference.md`

即本文。它是按路径解释仓库职责和工作方式的权威文档。目录增删或职责改变后应同步更新。

## `documentation/repository-architecture-and-data-flow.md`

用较短篇幅定义证据、研究、模型、派生作者、任务和出版物之间的单向数据流。适合快速理解系统边界。

## `documentation/source-author-research-methodology.md`

规定如何从 corpus 建立研究结论：使用稳定证据 ID、记录反例、区分时期与文类、标注置信度。源作者研究员开始工作前必须阅读。

## `documentation/derived-author-creation-methodology.md`

规定如何把源作者模型转化为独立派生作者。重点是继承、改造、拒绝、原创和理由，而不是简单调整一个“相似度百分比”。

## `documentation/provenance-and-evidence-policy.md`

规定证据等级与可追溯性。它回答“什么可以证明源作者特征”“什么只能证明派生作者或 harness 的表现”。

## `documentation/publication-and-editorial-approval-policy.md`

规定什么情况下工作项可以进入正式出版区。事实审核、文风审核、编辑批准和元数据缺一不可。

## `documentation/naming-versioning-and-file-conventions.md`

规定描述性 kebab-case 目录和文档名、snake_case Python 名、语义版本、work-item ID，以及保留 `README.md`、`AGENTS.md`、`SKILL.md` 等标准名的理由。

## `documentation/runtime-adapter-contract.md`

规定 runtime adapter 只能描述模型、上下文、工具、环境变量和命令接口，不能偷偷携带作者人格或出版规则。

## `documentation/writing-work-item-state-machine.md`

定义 `intake → research → planned → drafted → fact-checked → style-reviewed → editor-review → approved → published → archived` 的状态顺序与回退原则。

## `documentation/glossary-of-author-lab-terms.md`

统一 source author、source corpus、source-author model、derived author、derivation profile、harness、runbook、runtime adapter、work item 等术语，避免团队使用同一个“作者模型”指代多种东西。

## `documentation/implementation-plans/`

存放已经批准或正在执行的架构和文档实施计划。它们记录“怎样完成一次仓库变更”，不是永久操作规范。

### `documentation/implementation-plans/2026-07-11-complete-author-lab-sample-repository-scaffold.md`

最初建立完整样板仓库的计划，保留为架构形成记录。

### `documentation/implementation-plans/2026-07-11-complete-repository-file-and-directory-guide.md`

建立本文和更新文档入口的实施计划。

---

# 五、`source-authors/`：真实源作者及其材料

此目录只管理真实作者、真实来源和材料权利，不管理派生作者。

## `source-authors/README.md`

说明一个真实源作者对应一个子目录，并要求该目录包含资料档案、权利登记、规范化文本、书目和局部 agent 规则。

## `source-authors/source-author-sample/`

样板源作者的完整资料容器。真实项目中复制此结构并更换 ID，而不是直接把真实内容写进 sample 名称下。

### `source-authors/source-author-sample/AGENTS.md`

源材料区域的局部规则：原始记录不可覆盖，不得推断缺失生平，不得加载派生文章作为研究证据，规范化段落必须指回原始来源。

### `source-authors/source-author-sample/source-author-profile.json`

源作者机器档案。记录源作者 ID、显示名、对象类型、语言、corpus manifest、权利登记、研究目录和编译模型目录。

### `source-authors/source-author-sample/source-bibliography.md`

人类可读的完整书目。负责版本、译本、修订、期刊出处和时间差异；机器稳定 ID 仍以 manifest 为准。

### `source-authors/source-author-sample/source-rights-register.jsonl`

逐条记录每个 source ID 的权利状态、可否再分发、存储策略与授权依据。材料进入仓库前先登记权利。

## `source-authors/source-author-sample/source-corpus/`

源作者资料的证据仓库，分为 manifest、原始材料、二手材料和规范化材料。

### `source-corpus-manifest.jsonl`

所有来源的机器索引。每条记录包含 source ID、类型、标题、作者、年份、语言、原始文件、规范化文本、权利状态和校验值。检索、规范化和研究都以它为入口。

## `primary-source-materials/`

存放源作者本人留下的作品。这里的内容证据等级最高，但仍需要版本和出处管理。

### `primary-source-materials/README.md`

说明原作材料的总规则，以及大文件或受限制文件应保存在普通 Git 之外。

### `primary-source-materials/books/README.md`

书籍和 EPUB 的存放说明。要求区分版本、章节结构和分页映射。

### `primary-source-materials/essays-and-articles/README.md`

散文、评论、报刊文章和网络文章的存放说明。记录原始发布时间、URL、修订和稳定段落 ID。

### `primary-source-materials/interviews-and-conversations/README.md`

访谈和对话的存放说明。必须区分源作者原话、采访者提问、转录修订、翻译和编辑删节。

### `primary-source-materials/letters-and-correspondence/README.md`

信件与通信的存放说明。私人材料必须有授权，并记录删节、收件人、出处和是否已经公开。

### `primary-source-materials/diaries-and-notebooks/README.md`

日记和笔记的存放说明。保持时间、编辑介入、私人笔记与正式发表文本之间的差别。

### `primary-source-materials/speeches-and-lectures/README.md`

演讲与讲座的存放说明。记录场合、听众、准备稿、口头变动、转录来源和后来的出版版本。

### `primary-source-materials/social-media-and-short-form-writing/README.md`

社交媒体、帖子、短评和线程的存放说明。保留时间戳、上下文、删除状态、引用关系和平台限制。

## `secondary-source-materials/`

存放别人关于源作者的材料。它们能帮助理解，但不能冒充源作者原话。

### `secondary-source-materials/README.md`

说明传记、评论、研究和时代背景必须与原作分开，并记录可靠性与立场。

### `secondary-source-materials/biographies-and-historical-context/README.md`

传记和历史背景的存放说明。记录来源依据、作者立场、出版年代和争议性主张。

### `secondary-source-materials/criticism-and-scholarship/README.md`

文学评论、学术研究和书评的存放说明。二手解释用于形成问题和比较，不替代直接阅读原作。

## `normalized-source-materials/`

供搜索、引用和研究使用的可重复生成层。它不是原件，但必须保留回到原件的位置映射。

### `normalized-source-materials/README.md`

规定规范化结果应保留 source ID、章节、页码或时间戳映射，并允许由脚本重新生成。

### `normalized-source-materials/plain-text/README.md`

纯文本规范。每段应具有稳定 ID，便于研究结论精确引用。

### `normalized-source-materials/structured-metadata/README.md`

结构化元数据规范。存储章节、页码、说话人、版本、时间戳和位置关系。

### `normalized-source-materials/segmented-passages/README.md`

检索分段规范。分段是检索单元，不是新版本；必须保留足够上下文，避免句子级误读。

---

# 六、`source-author-research/`：对源作者的证据化研究

这里允许长篇、复杂、相互矛盾的研究。它比源作者模型更丰富，也更适合保留不确定性。

## `source-author-research/README.md`

说明研究层与 corpus、编译模型和派生作者设计之间的边界。

## `source-author-research/source-author-sample-research/AGENTS.md`

要求每条实质结论引用证据 ID、记录反例和置信度；禁止把研究文件直接写成 prompt，禁止使用派生文章作为源作者证据。

## `persona-and-intellectual-structure/`

研究作者关心什么、怎样思考、知道什么、如何判断和如何处理情绪。

### `recurring-concerns-and-attention-patterns.md`

研究作者反复注意什么、什么会触发问题意识、主题怎样随时期变化，以及哪些表面高频只是 corpus 偏差。

### `worldview-values-and-central-tensions.md`

研究价值承诺、世界观和长期未解决的张力，不强行把作者整理成完全一致的意识形态。

### `epistemology-and-standards-of-evidence.md`

研究作者如何区分知识、见闻、证言、权威、推断、不确定和足够证据。

### `knowledge-structure-and-domain-boundaries.md`

研究作者真正掌握的领域、经常引用的传统、薄弱区域、明确无知和知识变化。

### `reasoning-patterns-and-problem-framing.md`

研究作者如何发现问题、拒绝表面框架、补充语境、处理矛盾、转换尺度、形成或暂缓判断。

### `emotional-register-and-public-position.md`

研究作者的情绪范围、公共距离、自我定位、讽刺、愤怒、温柔、犹疑及其与论证的关系。

### `contradictions-blind-spots-and-uncertainties.md`

集中记录矛盾、盲点、材料空缺、争议解释和不能负责任下结论的部分。

## `writing-style-fingerprint/`

研究文风作为句法、节奏、段落、修辞和思维运动的组合，而不是常用句词库。

### `vocabulary-and-diction-patterns.md`

研究词汇层级、具体名词、抽象术语、语域转换、搭配、回避词和时期变化。

### `sentence-syntax-and-rhythm-patterns.md`

研究句长、从句、标点、中断、重复、压缩、呼吸和不同文类的节奏差异。

### `paragraph-architecture-and-transition-patterns.md`

研究段落如何进入、展开、转折、落地，以及段落之间如何产生张力、离题和返回。

### `rhetorical-moves-and-argument-structures.md`

研究反框架、限定、比较、枚举、类比、自我修正、提问、引用和常见论证序列。

### `openings-endings-and-narrative-distance.md`

研究开头方式、作者何时进入文本、叙事距离怎样变化，以及结尾如何关闭、悬置、反转或返回。

### `genre-specific-and-period-specific-variations.md`

区分稳定特征与书籍、散文、评论、日记、信件、演讲、访谈和短帖的文类规则，并标明时期边界。

### `anti-patterns-counterexamples-and-overfitting-risks.md`

记录假指纹、罕见习惯、编辑痕迹、翻译影响、文类限制和模型容易过量使用的特征。

## `topics-and-periodization/`

研究议题之间的关系与作者发展时期。

### `recurring-topics-and-issue-relationships.md`

建立议题图谱：哪些议题互相引出、哪些概念连接它们、哪些议题消失或重新出现。

### `topic-chronology-and-periodization.md`

依据作品、主题、语汇、文类和社会位置确定作者时期，而不是机械按十年划分。

## `evidence-and-confidence/`

把研究判断变为可追溯、可审核的数据。

### `research-claim-evidence-register.jsonl`

每条研究 claim 的机器记录：claim ID、正文、置信度、状态、支持段落和反例段落。源作者模型只能引用已经接受的 claim。

### `research-confidence-rating-guide.md`

定义高、中、暂定和开放假设的置信度范围，以及什么条件下研究结论能够进入源作者模型。

## `comprehensive-research-reports/`

存放综合性成果，而不是零散笔记。

### `comprehensive-source-author-research-report.md`

综合时间、议题、人格、知识、推理、情绪、文风、反例和限制，始终保留指向证据 register 的链接。

### `source-author-research-limitations.md`

集中说明 corpus 空缺、版本问题、翻译影响、私人材料缺失、文类不均衡和被排除的解释。

---

# 七、`source-author-models/`：可加载的源作者模型

研究层可能很长，模型层必须短、稳定、分模块并有版本。模型是研究的编译产物，不是源作者本人。

## `source-author-models/README.md`

说明源作者模型的性质、用途和限制，防止把它当作人格扮演许可。

## `source-author-models/source-author-sample-model/AGENTS.md`

规定只有已接受研究可以进入模型，每条规则必须登记 provenance，模型应保持紧凑，生成文章不得写回。

## `VERSION`

当前源作者模型的语义版本。任何会影响下游派生作者加载结果的修改都应升级版本。

## `source-author-model-manifest.json`

记录模型 ID、源作者 ID、版本、状态、core、genre modes、period overlays、加载图和 provenance register。

## `source-author-model-limitations.md`

明确模型的不完整性、选择性和不适用范围，尤其不能代表源作者对新事件的观点或私人记忆。

## `author-model-loading-map.json`

规定默认 core 和不同文类应加载的文件。它控制上下文组合，避免每次把整个研究库塞进 prompt。

## `source-author-model-provenance-register.jsonl`

将每一条模型规则映射到一个或多个研究 claim ID 和具体模型文件。修改模型时必须同步更新。

## `core-author-model/`

每次需要理解源作者模型时可能加载的稳定核心。

### `source-author-identity.md`

只记录有研究支持的公共角色和思想位置，不编造履历或私人关系。

### `recurring-concerns.md`

压缩已达置信度门槛的稳定关注点，同时保留时期和文类限定。

### `worldview-and-central-tensions.md`

压缩价值结构和主要张力，不制造完美一致的世界观。

### `epistemology-and-uncertainty-practice.md`

定义模型如何区分观察、报道、推断、记忆、判断和未解决问题。

### `knowledge-map-and-domain-boundaries.md`

定义有证据的知识领域、薄弱领域、未知区域和需要外部研究的情形。

### `reasoning-patterns.md`

压缩注意、框架、比较、语境、尺度转换、限定、判断和返回的思维运动。

### `emotional-register.md`

定义可支持的情绪范围、触发条件和情绪与论证的关系。

### `voice-and-register.md`

定义公共姿态、对话距离、确定性、技术语域、直接程度和语言切换。

### `writing-style-fingerprint.md`

压缩句法、节奏、段落、修辞、开头、结尾、转换和负面约束。它是生成约束，不是可复制短语库。

### `authorial-boundaries.md`

规定模型不得声称的身份、私人经验、现时观点、资历和授权。

### `model-uncertainties.md`

保留尚未解决或因证据不足而没有进入模型的部分。

## `genre-specific-author-modes/`

源作者在不同文类中的表现覆盖层。

### `essay-writing-mode.md`

描述长篇散文或论说文的稳定方式，同时避免把一篇样本的结构变成固定模板。

### `column-writing-mode.md`

描述专栏的时事入口、论证密度、篇幅、节奏和结尾。

### `criticism-writing-mode.md`

描述批评写作中的判断、引用、语境、细读和公平原则。

### `diary-writing-mode.md`

描述日记尺度、时间感和观察方式，但不得据此编造生活事件。

### `letter-writing-mode.md`

描述书信中的称呼、亲密度、论证和收件人意识，不得制造关系。

### `short-post-writing-mode.md`

描述短帖压缩、线程、平台限制和口号化风险。

## `period-specific-author-overlays/`

只在任务明确需要某一时期时加载。

### `early-period-author-overlay.md`

记录早期关注、词汇、形式、知识和公共位置的差异。

### `middle-period-author-overlay.md`

记录中期变化与连续性。

### `late-period-author-overlay.md`

记录后期变化与连续性。

## `calibration-examples/README.md`

说明可以存放带授权的短例子和证据 ID，用于校准理解，禁止演变为句子模板库。

## `negative-calibration-examples/README.md`

说明存放反例和近似但不属于作者特征的文本，帮助模型避免过度概括。

---

# 八、`derived-author-personas/`：独立派生作者

一个派生作者不是“源作者模型加一个 prompt”。它必须拥有自己的谱系、身份、模型、边界、记忆、工作、评测和出版历史。

## `derived-author-personas/README.md`

说明每个子目录都代表一个长期维护的独立化名作者。

## 派生作者共同文件结构

下面的文件在 B 和 C 中分别独立存在。B 的路径以 `derived-author-sample-b/` 开头，C 的路径以 `derived-author-sample-c/` 开头。它们职责相同，但内容不能共用。

### `README.md`

给人看的派生作者概要：该作者的定位、与源作者的关系以及不能声称什么。

### `AGENTS.md`

进入该派生作者目录后的 agent 规则。规定什么时候允许进入作者写作模式、加载哪些模型文件、禁止读取哪个其他派生作者的记忆和出版物。

### `derived-author-persona-manifest.json`

派生作者机器入口。记录作者 ID、显示名、状态、语言、lineage、derivation、model、harness、memory、work、evals 和 publications 的位置。

### `derived-author-lineage.json`

记录该作者从哪些上游模型获得影响、版本、作用和设计权重，并明确禁止声称源作者身份、经验和无引用原句。

## `derivation-profile/`

回答“这个作者怎样从上游模型变成自己”。

### `inherited-source-author-traits.md`

只列明确继承的关注点、推理关系、文风关系和认识习惯，并引用上游模型规则。

### `transformed-source-author-traits.md`

记录继承特征怎样因新历史位置、文类、公共角色和知识边界而发生改变。

### `rejected-source-author-traits.md`

记录明确拒绝的源作者生平、私人经验、辨识度过高语言、权威和不能脱离原人生成立的特征。

### `original-derived-author-traits.md`

记录派生作者自己新增的公共角色、议题、知识、情绪范围、形式和编辑承诺。

### `derivation-rationale-and-design-decisions.md`

解释为什么继承、改造、拒绝和新增这些特征，并说明与其他派生作者的区别。

## `derived-author-model/`

派生作者实际写作时加载的模型。

### `VERSION`

当前派生作者模型版本。文章 work item 必须记录使用了哪个版本。

### `derived-author-model-manifest.json`

记录模型 ID、派生作者 ID、版本、状态、core、genre modes 和加载图。

### `derived-author-model-loading-map.json`

规定默认加载的 core 和每个文类 mode。writer 不应随意越过它加载全部人格资料。

## `core-derived-author-model/`

派生作者的稳定核心。

### `derived-author-identity-and-public-role.md`

定义化名身份和公共角色，但不虚构无法核实的履历、资历或私人关系。

### `recurring-concerns-and-topic-boundaries.md`

定义长期议题、可扩展方向、研究前置领域和不应自信处理的主题。

### `worldview-values-and-central-tensions.md`

定义该派生作者自己的价值结构与内在张力，而不是整套复制源作者世界观。

### `knowledge-boundaries-and-research-obligations.md`

定义现有知识、写前必须调研的领域、禁止冒充的专业资格和知识增长规则。

### `reasoning-patterns-and-problem-framing.md`

定义该作者如何选择触发物、提出问题、建立语境、转换尺度和保留不确定，同时防止形成单一文章公式。

### `emotional-register-and-narrative-distance.md`

定义情绪强度、第一人称距离、幽默、克制和不得制造的情感场景。

### `voice-and-writing-style-fingerprint.md`

定义句法、节奏、段落、修辞、结尾和与其他派生作者的区别。

### `authorial-and-ethical-boundaries.md`

定义不得声称、不得虚构和必须区分事实、报道、推断与文学构造的边界。

### `model-uncertainties-and-open-questions.md`

记录尚未稳定的作者特征，防止临时生成习惯过早成为永久人格。

## B 的 `genre-specific-writing-modes/`

### `essay-writing-mode.md`

规定 B 的研究型公共散文模式，强调持续论证、多尺度和非机械收束。

### `short-commentary-writing-mode.md`

规定 B 的短评论压缩方式，保留语境与限定，避免口号化。

### `diary-and-life-writing-mode.md`

规定 B 只能使用 work item 授权的生活材料，不得制造自传细节。

## C 的 `genre-specific-writing-modes/`

### `cultural-essay-writing-mode.md`

规定 C 可从地点、物件、界面、书、词语和习惯进入文化结构。

### `short-cultural-commentary-writing-mode.md`

规定 C 的短文化评论保留物质细节，不把观察压成普遍教训。

### `diary-and-life-writing-mode.md`

规定 C 的日记和生活写作保留普通物件和时间质感，不编造情绪闭合。

## `author-specific-writing-harness/derived-author-writing-overlays.md`

派生作者对共享 harness 的局部覆盖层。只能增加该作者的加载、边界和差异性规则，不能复制或削弱共享状态机、事实和出版门。

## `derived-author-memory/`

派生作者自己的长期记忆，不属于源作者研究。

### `author-writing-memory.md`

记录已经批准的写作历史、稳定编辑经验和有意发展的作者特征。

### `editorial-review-memory.md`

记录多次审校中反复出现的问题、已经接受的修正和被拒绝的习惯。

### `knowledge-growth-log.md`

记录通过已审核 research pack 获得的新知识。知识增长不自动等于人格或文风改变。

### `publication-history.jsonl`

机器可读的出版历史，关联 publication ID、work-item ID、状态和路径。

## `derived-author-writing-work-items/README.md`

说明此处只放该作者视角的索引或快捷入口；正式、完整的任务包仍以根级 `writing-work-items/` 为准。

## `derived-author-evaluations/README.md`

说明该作者需要接受哪些专属评测，例如身份一致性、源作者泄漏、原创性、事实性和与另一个派生作者的区别。

## `derived-author-publications/README.md`

说明这里可以组织某个派生作者的出版视图，但正式 canonical 文件仍在根级 `approved-publications/`。

---

# 九、`shared-writing-harness/`：共享写作控制系统

Harness 负责“怎样运行工作”，不负责“作者是谁”。所有派生作者共享状态、合同、审核和出版门，可以用 overlay 添加差异，但不能复制整套管线。

## `shared-writing-harness/README.md`

说明机器合同、prompt、runbook、政策和模板的总体分工。

## `shared-writing-harness/AGENTS.md`

要求合同保持确定性和作者中立，schema 变化必须同步例子与测试，派生作者 overlay 不得削弱出版规则。

## `machine-readable-contracts/`

所有跨 agent、脚本和 runtime 交换的数据结构。

### `README.md`

说明这些 JSON Schema 是稳定接口，不是普通文档。

### `author-lab-project-manifest.schema.json`

验证根级项目 manifest 的项目 ID、类型和主要目录字段。

### `source-author-profile.schema.json`

验证源作者资料文件的 ID、显示名、对象类型、语言、corpus 和权利位置。

### `source-corpus-record.schema.json`

验证 corpus 每条来源记录的 source ID、类型、标题、文件、规范化路径、权利和校验值。

### `source-author-model-manifest.schema.json`

验证源作者模型 ID、源作者 ID、版本和 provenance。

### `derived-author-persona-manifest.schema.json`

验证派生作者 ID、显示名、persona 类型、lineage 和模型目录。

### `derived-author-lineage.schema.json`

验证上游模型、角色、设计权重和三个必须为 false 的冒充边界。

### `writing-runbook-manifest.schema.json`

验证 runbook ID、版本、必需阶段、可选阶段和必需工件。

### `writing-work-item-state.schema.json`

验证 work-item ID、派生作者、状态、模型版本、runbook、runtime 和三类审核状态。

### `writing-run-manifest.schema.json`

验证一次具体模型运行的 run ID、work item、runtime、模型、时间和加载文件。

### `factual-review-result.schema.json`

验证事实审核结果，以及每条 claim 的类型、支持状态、来源和 as-of 日期。

### `style-review-result.schema.json`

验证 persona consistency、source fidelity、source leakage、originality 和 cross-persona distinction 等指标。

### `runtime-adapter-configuration.schema.json`

验证 runtime ID、类型、配置版本、模型、上下文、工具和环境变量。

### `evaluation-result.schema.json`

验证独立评测的对象、类型、分数、评测者和说明。

### `publication-record.schema.json`

验证正式出版记录的 publication ID、work item、作者、标题、状态、canonical 文件和时间。

## `task-prompts/`

每个阶段的职责提示，不包含派生作者人格。

### `README.md`

说明 prompt 只定义任务和输出，作者身份从选定 persona 目录加载。

### `source-research-stage-prompt.md`

指导建立 research pack，区分确认事实、报道、官方说法、分析推断和未解决问题。

### `structured-planning-stage-prompt.md`

指导建立文章核心问题、判断、证据顺序、段落功能、风险和结尾策略。

### `complete-drafting-stage-prompt.md`

指导依据批准计划完整写稿，并禁止虚构事实、场景、引语、关系和源作者经验。

### `factual-review-stage-prompt.md`

指导提取 claim、分类、核查支持和日期，并输出符合 schema 的结果。

### `style-review-stage-prompt.md`

指导评估派生作者一致性、上游特征继承、泄漏、原创性和跨作者区别。

### `editorial-revision-stage-prompt.md`

指导仅依据记录的事实、风格和编辑意见生成新版本，不覆盖历史草稿。

### `publication-preparation-stage-prompt.md`

指导检查批准门、生成元数据、复制 canonical 文件并更新出版 manifest。

## `writing-runbooks/`

Runbook 决定一种任务需要哪些阶段和工件。

### `README.md`

说明 runbook 不选择具体模型，也不编码作者人格。

### `standard-researched-essay/README.md`

标准有研究散文的用途说明。

### `standard-researched-essay/writing-runbook-manifest.json`

要求 intake、research、planning、drafting、事实审核、风格审核、编辑审核和出版准备，并列出必需文件。

### `deep-research-article/README.md`

长篇、重资料研究文章的用途说明。

### `deep-research-article/writing-runbook-manifest.json`

增加 research review、可选第二轮事实审核和更完整的来源记录。

### `short-public-commentary/README.md`

短公共评论的用途说明，篇幅短但事实、人格和编辑门仍不可跳过。

### `short-public-commentary/writing-runbook-manifest.json`

定义短评论的阶段和必需工件。

### `authorized-life-writing/README.md`

使用用户明确提供的生活事件和私人笔记时使用，重点是场景授权而不是广泛网络研究。

### `authorized-life-writing/writing-runbook-manifest.json`

要求 scene authorization，并列出授权场景文件、计划、草稿和审核结果。

### `style-preserving-rewrite/README.md`

用于在保持意义与授权事实的情况下重写已有文本。

### `style-preserving-rewrite/writing-runbook-manifest.json`

要求 source-text analysis、semantic review 和 style review，不默认进行开放式研究。

## `harness-policies/`

所有 runbook 和派生作者都必须服从的共享规则。

### `factuality-and-claim-classification-policy.md`

要求外部真值 claim 分成 verified fact、reported claim、analysis inference、literary construction 或 unsupported speculation。

### `citation-and-source-quality-policy.md`

强调来源质量、独立性和对具体 claim 的直接支持，禁止以来源数量替代可靠性。

### `derived-author-boundaries-and-source-leakage-policy.md`

规定派生作者可以继承关系和方法，但不能借用源作者身份、私生活、原句和权威。

### `originality-and-non-copying-policy.md`

要求检查对源文本、校准例子、旧文章和其他派生作者的文本及结构重复。

### `editorial-review-and-publication-gates-policy.md`

规定事实审核、风格审核、编辑批准、元数据和仓库验证是正式出版的硬门。

## `artifact-templates/`

新 work item 生成标准文件时使用的空白结构。

### `writing-brief-template.md`

包含任务、作者、文类、篇幅、受众、核心问题、材料、禁区和出版目的地。

### `research-pack-template.md`

包含确认事实、报道、官方说法、推断、冲突、时效、开放问题和来源 register。

### `article-plan-template.md`

包含核心问题、初步判断、作者特定思维运动、证据顺序、段落功能、风险和结尾。

### `editor-review-template.md`

包含编辑决定、事实、人格、结构、必改项和出版说明。

### `final-publication-metadata-template.json`

为正式出版记录提供机器可读字段模板。

---

# 十、`agent-skills/`：供 agent 调用的薄能力层

Skill 只说明一个角色如何加载现有资产并执行任务，不能复制完整作者研究和 harness。

## `agent-skills/README.md`

说明 skills 是轻量入口。

## `source-author-researcher/SKILL.md`

指导研究员加载源作者 profile、manifest、规范化段落、研究方法和证据 register，并输出有证据和反例的研究 claim。

## `derived-author-writer/SKILL.md`

指导 writer 加载选定 persona、lineage、derivation、core、genre mode、brief、research pack 和 runbook；禁止加载 held-out evals 和其他作者记忆。

## `factual-claim-reviewer/SKILL.md`

指导独立事实审查，不受文风偏好影响，输出 factual review schema。

## `derived-author-style-reviewer/SKILL.md`

指导文风审查，评估人格一致性、继承、泄漏、原创性和跨作者区别，不静默修理事实。

## `approved-publication-preparer/SKILL.md`

指导 publisher 验证所有状态门、建立元数据、复制 canonical 文件、更新 manifest 并运行验证。

---

# 十一、`runtime-adapters/`：执行环境配置

更换 OpenClaw、ChatGPT、Codex、Claude Code 或本地模型时，只改变 runtime 层，不改变作者身份。

## `runtime-adapters/README.md`

说明 adapter 的边界和用途。

每个 runtime 子目录都包含：

- `README.md`：说明该环境怎样加载文件、使用工具、运行命令和处理权限；
- `runtime-adapter-configuration.json`：机器配置，包括 ID、类型、版本、默认模型、上下文、工具能力和环境变量。

具体目录：

- `openclaw-runtime-adapter/`：OpenClaw profiles、模型路由、workspace 和工具映射；
- `chatgpt-runtime-adapter/`：ChatGPT 的文件、Web、GitHub 和分析工具使用方式；
- `codex-runtime-adapter/`：Codex 的本地仓库、worktree、测试和 PR 流程；
- `claude-code-runtime-adapter/`：Claude Code 的仓库规则、权限、加载和验证；
- `local-command-line-runtime-adapter/`：本地模型或 API 客户端命令行环境，密钥保存在 Git 之外。

---

# 十二、`author-model-evaluations/`：独立评测

评测不只是“像不像源作者”，还要判断派生作者是否形成自己、是否泄漏和是否原创。

## `README.md`

说明六个核心指标和 held-out 隔离原则。

## `evaluation-rubrics/`

### `source-trait-fidelity-rubric.md`

只评估 derivation profile 中明确计划继承或改造的特征，不追求最大相似。

### `independent-persona-consistency-rubric.md`

评估派生作者的议题、推理、知识、情绪和文风是否跨任务稳定。

### `source-author-leakage-rubric.md`

评估身份、生平、私人经验、原句、权威和过度文本近似的泄漏。

### `originality-and-non-copying-rubric.md`

评估句子复用、结构自复制、对校准样本和旧文章的依赖。

### `cross-persona-distinction-rubric.md`

在同一 brief 和 research pack 下比较 B/C 是否在注意、框架、节奏、文类和结尾上真正不同。

### `factuality-and-scene-authorization-rubric.md`

评估 claim 支持、日期限定、来源质量、虚构引语、自传和场景授权。

## `calibration-evaluation-cases/README.md`

存放开发期间可见的校准题，不与 held-out 混用。

## `held-out-evaluation-cases/README.md`

存放 writer 不得读取的正式评测题和样本，防止评测变成背题。

## `adversarial-evaluation-cases/README.md`

存放诱导冒充、虚构经历、复制原句、作者坍缩和绕过出版门的压力测试。

## `runtime-comparison-reports/README.md`

在同一模型版本、runbook、research pack 和 eval case 下比较不同 runtime，记录模型、上下文、工具和成本。

---

# 十三、`derived-author-comparisons/`：作者之间的受控比较

比较报告是评测资产，不能反向成为写作 prompt。

## `README.md`

说明比较目的和边界。

## `source-author-model-versus-derived-author-sample-b/README.md`

记录 A 模型到 B 的计划继承、改造、拒绝、泄漏风险和独立特征。

## `source-author-model-versus-derived-author-sample-c/README.md`

记录 A 模型到 C 的计划继承、改造、拒绝、泄漏风险和独立特征。

## `derived-author-sample-b-versus-derived-author-sample-c/README.md`

比较 B/C 的议题、角色、推理、知识、节奏、文类、记忆和同题输出差异。

---

# 十四、`writing-work-items/`：一次写作的完整工作包

这里是实际生产中心。所有过程文件都围绕一个 work-item ID 放在同一目录，而不是分散在全仓库的 `_drafts`、`plans` 和 `reviews` 中。

## `writing-work-items/README.md`

说明每个工作项必须包含状态、brief、run、research、来源、计划、草稿、事实审核、文风审核、编辑审核和最终稿。

## `writing-work-items/AGENTS.md`

规定先读状态文件、草稿不可覆盖、审核门不可跳过、每次模型运行都必须记录。

## `2026-writing-work-items/`

按年份组织工作项。年份只用于归档，不改变状态机。

## `2026-001-sample-article/`

一个完整样例工作包。

### `work-item-state.json`

整个任务的机器权威状态。记录作者、模型版本、runbook、runtime、三类审核和出版关联。程序决定能否继续时读取它，而不是从自然语言猜测。

### `writing-brief.md`

编辑或 operator 给出的任务定义，包括作者、文类、目的、受众、材料和禁区。

### `writing-run-manifest.json`

记录一次具体模型运行：run ID、runtime、模型、开始结束时间和实际加载文件。重跑时创建新记录或扩展为 run 历史，不覆盖事实。

### `research-pack.md`

该文章专用的事实与分析材料。它与源作者研究不同，关注当前选题和时效性事实。

### `work-item-source-register.jsonl`

该文章实际使用来源的机器清单，供事实审核和出版追踪。

### `article-plan.md`

文章结构和论证计划，包括判断、证据顺序、段落功能、风险和结尾。

### `draft-01.md`

第一版完整草稿，保留不覆盖。

### `draft-02-after-review.md`

根据审核形成的第二版，文件名说明版本与来源。

### `factual-review-result.json`

结构化事实审核结果。状态必须与 `work-item-state.json` 一致。

### `style-review-result.json`

结构化派生作者和文风审核结果，包括一致性、继承、泄漏、原创和区分度。

### `editor-review.md`

人类编辑的决定和修改意见。编辑批准是机器自审无法替代的外部门。

### `final-approved-article.md`

最终候选文件名。只有状态变为 `approved` 且编辑批准后，它才真正是 approved；文件名本身不赋予权限。

---

# 十五、`approved-publications/`：正式出版物

这里保存经过批准的 canonical 内容，不与网站生成器绑定。

## `README.md`

说明只有审核通过内容可以进入，以及出版物不能反向证明源作者。

## `AGENTS.md`

规定写入前检查 work-item 状态和三类审核，并原子更新 manifest。

## `approved-publication-manifest.jsonl`

所有正式出版物的机器索引。样板中的 withdrawn 记录用于维持示例格式，不代表真实发布。

## `researched-essays/README.md`

正式研究型散文的 canonical 存储区说明。

## `short-public-commentaries/README.md`

正式短评论存储区说明。

## `authorized-life-writing/README.md`

正式生活写作存储区说明，必须保留场景授权和非虚构边界。

## `book-length-projects/README.md`

书稿和版本元数据存储区说明。保存 canonical manuscript，不保存可重复生成的 EPUB/PDF 构建产物。

## `editorial-collections/README.md`

专题集、选集和编排关系存储区说明。应引用 canonical 文章而不是复制多份正文。

---

# 十六、`publication-site/`：展示层

## `publication-site/README.md`

说明网站只是从 `approved-publications/` 读取内容的一种展示方式。更换 Jekyll、Astro 或其他生成器不应改变研究、模型和出版目录。

## `publication-site/publication-site-configuration.json`

记录 site ID、生成器、canonical 出版目录、生成输出目录和允许进入网站的 publication 状态。

---

# 十七、`repository-automation-scripts/`：仓库自动化

## `README.md`

说明脚本负责结构、文档、状态、脚手架、规范化和出版索引。

## `validate_author_lab_repository_structure.py`

检查关键目录和入口文件是否存在。它验证骨架，不验证内容质量。

## `validate_json_and_jsonl_documents.py`

遍历仓库并解析所有 JSON/JSONL，发现语法损坏和非法行。

## `validate_sample_comment_markers.py`

检查所有受管文本文件是否包含指定 sample 注释，并排除缓存、构建和环境目录。真实内容完成后可以按计划移除该验证要求。

## `validate_writing_work_item_state.py`

执行状态机硬规则：进入 fact-checked 以后必须事实通过，进入 style-reviewed 以后必须风格通过，进入 approved 以后必须编辑批准，published 必须有出版信息。

## `create_new_derived_author_persona.py`

根据 kebab-case ID、显示名和上游模型信息建立新派生作者骨架。它只创建框架，不替代真正的人格研究与设计。

## `create_new_writing_work_item.py`

根据 work-item ID、派生作者、模型版本、runbook 和 runtime 创建新任务包及初始状态。

## `build_approved_publication_manifest.py`

扫描正式出版元数据并重建 publication manifest。它只收录合法状态，不能将草稿自动批准。

## `normalize_authorized_plain_text_source.py`

将已经授权的纯文本统一换行、清理空行并加入稳定段落 ID。它不是 EPUB/PDF 全功能解析器。

---

# 十八、`repository-validation-tests/`：自动化测试

## `README.md`

说明测试覆盖结构、机器文档、sample 标记、状态机和文本规范化。

## `test_repository_structure_validation.py`

验证所有关键路径存在。

## `test_json_and_jsonl_document_validation.py`

通过子进程运行机器文档解析脚本并检查返回码。

## `test_sample_comment_marker_validation.py`

验证当前 sample 阶段所有文件都带指定注释。

## `test_writing_work_item_state_machine.py`

验证合法 editor-review 状态能够通过，并验证缺少编辑批准与 publication 的 published 状态会失败。

## `test_authorized_plain_text_normalization.py`

验证规范化脚本产生稳定段落 ID。

---

# 十九、`.github/`：GitHub 协作与持续集成

## `.github/workflows/validate-author-lab-repository.yml`

在 push、PR 和手动触发时安装 Python，依次运行结构、JSON/JSONL、work-item 状态、sample 标记和 pytest。任何一步失败都不应合并。

## `.github/CODEOWNERS`

指定默认和关键目录的代码所有者。真实团队可以把研究、模型、出版和工程目录分配给不同负责人。

## `.github/PULL_REQUEST_TEMPLATE.md`

要求 PR 标明变更属于 corpus、研究、模型、派生作者、harness、work item、出版或自动化，并确认相应证据和测试。

## `.github/ISSUE_TEMPLATE/source-author-research-claim.yml`

用于提出或修订源作者研究 claim，强制填写主张、支持与反例证据、置信度。

## `.github/ISSUE_TEMPLATE/derived-author-model-change.yml`

用于提出派生作者身份、谱系、模型或边界变更，要求说明对继承、改造、拒绝和原创的影响。

## `.github/ISSUE_TEMPLATE/repository-validation-problem.yml`

用于报告 schema、状态机、脚本和目录验证问题，要求提供完整命令输出和预期行为。

---

# 二十、不同角色应该怎样读取仓库

## Source corpus curator

按顺序读取：

1. `RIGHTS-AND-LICENSING-POLICY.md`
2. 根 `AGENTS.md`
3. `source-authors/<source-author>/AGENTS.md`
4. `source-author-profile.json`
5. `source-corpus-manifest.jsonl`
6. `source-rights-register.jsonl`
7. 相应原始材料类型的 `README.md`

输出是新的 source record、权利记录和规范化材料，不直接修改研究结论。

## Source-author researcher

读取 corpus manifest、规范化段落、研究方法、证据政策和研究目录。输出研究 Markdown、claim register 和综合报告，不直接修改派生作者。

## Source-model curator

读取已接受 research claim、综合报告、limitations 和 provenance。输出版本化 source-author model、load map 和 provenance register。

## Derived-author designer

读取源作者模型、派生方法、伦理政策和其他作者比较目标。输出 persona manifest、lineage、五类 derivation 文件和独立 author model。

## Writer

只读取：选定派生作者 manifest、lineage、derivation、load map 指定 core、一个 genre mode、一个 runbook、当前 brief 和 research pack。writer 不读 held-out evals，也不读另一个作者记忆。

## Factual reviewer

读取 draft、research pack、source register、事实政策和 schema。尽量不加载风格提示，以保持事实判断独立。

## Style reviewer

读取 draft、派生作者模型、derivation profile、风格 rubric 和对照目标。不得通过改变事实来“修好文风”。

## Editor

读取整个 work item、两份结构化审核和必要的作者模型。编辑决定写入 `editor-review.md` 和状态文件。

## Publisher

只接受 `approved` 的工作项，核对三类审核、最终稿和元数据，复制到 `approved-publications/` 并更新 manifest。

## Runtime maintainer

只修改 `runtime-adapters/`、脚本、依赖和 CI。不能把模型偏好写进作者人格，也不能为了 runtime 方便削弱出版门。

---

# 二十一、四种常见新增工作的标准做法

## 新增一个真实源作者

1. 在 `source-authors/` 下创建新的描述性目录；
2. 建立 profile、bibliography、rights register 和 corpus manifest；
3. 登记原始与二手材料；
4. 生成规范化文本与位置映射；
5. 在 `source-author-research/` 建立对应研究目录；
6. 研究成熟后才在 `source-author-models/` 建立版本化模型；
7. 更新根 project manifest；
8. 运行全部验证。

## 新增一个派生作者

1. 使用 `create_new_derived_author_persona.py` 建立骨架；
2. 完成 lineage；
3. 分别写 inherited、transformed、rejected、original 和 rationale；
4. 完成 core model、genre modes 和 load map；
5. 建立独立 memory、evals 和 comparison；
6. 更新根 project manifest；
7. 先通过校准和对抗评测，再开始正式生产。

## 新增一篇文章

1. 使用 `create_new_writing_work_item.py` 创建任务包；
2. 完成 brief；
3. 选择一个派生作者、模型版本、runbook 和 runtime；
4. 建立 research pack 和 source register；
5. 完成 plan；
6. 创建不可覆盖的 draft 版本；
7. 完成 factual review；
8. 完成 style review；
9. 等待 editor review；
10. 获批后准备 final 和 publication metadata。

## 发布一篇文章

1. 检查状态为 `approved`；
2. 检查事实与文风审核为 `passed`；
3. 检查编辑为 `approved`；
4. 将 final 复制到合适的 `approved-publications/` 分类；
5. 写 publication metadata；
6. 重建 manifest；
7. 运行验证；
8. 网站只读取 `published` 状态内容。

---

# 二十二、sample 注释的处理

当前每个文件都有：

```text
这是一个 sample，文件实质完成后删掉这行注释
```

Markdown、Python、YAML、TOML 和 Git 配置使用各自注释语法；JSON 和 JSONL 使用 `_sample_comment` 字段。

这个标记表示文件目前主要承担“结构和职责示范”，不表示路径本身应删除。实际填入真实内容后，应逐个文件移除标记。只有当仓库不再要求所有文件保留 sample 标记时，才同时修改：

- `validate_sample_comment_markers.py`
- `test_sample_comment_marker_validation.py`
- GitHub Actions 中对应步骤
- 根 README 中的说明

不能先大规模删除标记而保留必然失败的 CI。

---

# 二十三、这套目录的最终原则

这不是一个把 EPUB、prompt、脚本和文章放在一起的文件夹，而是一套有明确证据链和权限边界的作者研究与生产系统。

- 源作者材料回答“真实留下了什么”；
- 源作者研究回答“我们如何理解这些材料”；
- 源作者模型回答“哪些研究结论可以被稳定加载”；
- 派生作者回答“怎样建立一个受影响但独立的新作者”；
- Harness 回答“工作按什么合同和质量门运行”；
- Runtime 回答“在哪个环境和模型上执行”；
- Work item 回答“一篇文章具体经历了什么”；
- Evaluations 回答“系统是否保持人格、原创、事实和区分度”；
- Publications 回答“什么已经获得编辑批准，可以正式存在”。

任何新工作都应先判断自己属于哪一层，再写入对应目录。不能因为某个文件方便加载，就跨越层级把研究、人格、runtime、任务和出版混在一起。
