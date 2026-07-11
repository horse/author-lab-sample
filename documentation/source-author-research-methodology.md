# Source-Author Research Methodology

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

源作者研究从经过 rights 与 storage 登记的 corpus 开始。研究层负责解释材料，不负责模仿、生成或替源作者回答新问题。

## 一、资料进入研究前的条件

每个 `source_id` 必须同时出现在：

- source corpus manifest；
- source rights register；
- source material storage and ingestion register。

三处必须一致记录：

- source author；
- storage URI；
- rights status；
- checksum；
- edition；
- segmentation version。

原始版权材料默认保存在仓库外 `private-storage://`。仓库中的 normalized text 和 location map 不能被误认为原始版本。

## 二、Edition 与 segmentation

研究引用必须使用完整 segment ID：

```text
SOURCE-ID.edition-01.segmentation-01.segment-00042-<hash-prefix>
```

每个 location record 同时保存完整 `content_sha256`。

- edition 改变意味着来源版本改变；
- segmentation version 改变意味着分段规则或顺序改变；
- content hash 相同只能证明文本内容相同，不能证明 segment ID 应保持不变；
- 重新分段后，旧研究 claim 继续指向旧 segmentation namespace，直到经过显式迁移和复核。

不能把按当前顺序生成的数字称为跨编辑稳定 ID。

## 三、Research claim

关于 concerns、worldview、knowledge、reasoning、emotion 与 style 的每条实质结论都应进入 `research-claim-evidence-register.jsonl`，至少包含：

- `research_claim_id`；
- claim；
- confidence；
- status；
- supporting segment IDs；
- counterexample segment IDs。

研究文件可以长篇讨论，但能够进入 source-author model 的规则必须能回到已接受 research claim。

## 四、证据等级

研究员应区分：

1. 源作者本人正式发表作品；
2. 源作者访谈、书信、日记、演讲与短帖；
3. 版本、编辑和翻译带来的差异；
4. 可靠传记与历史资料；
5. 批评、学术解释与争议观点；
6. 研究员自己的推断。

二手解释不能冒充源作者原话；高频出现也不能自动证明稳定人格特征，因为 corpus 可能受到文类、时期和保存偏差影响。

## 五、时期、文类与反例

研究不得把所有材料平均成一个声音。

必须分别观察：

- early / middle / late period；
- book、essay、criticism、diary、letter、speech、interview、short-form；
- 私人语境与公共语境；
- 原文与译文；
- 编辑版本与口头记录。

每个强结论都应主动寻找：

- 同时期反例；
- 跨时期变化；
- 文类限定；
- 编辑或翻译痕迹；
- 材料缺失造成的替代解释。

## 六、置信度与模型准入

建议使用：

- high：多类直接材料长期支持，反例已解释；
- medium：支持充分，但存在时期或文类限定；
- provisional：材料有限，暂时作为研究假设；
- open：存在多个合理解释，不进入模型规则。

只有达到项目规定门槛并处于 accepted 状态的 claim 才能编译进 source-author model。模型 provenance register 必须记录：

```text
model_rule_id
→ research_claim_ids
→ model_file
```

## 七、禁止的证据回流

以下内容不能成为关于源作者的研究证据：

- 派生作者文章；
- 模型自动补写；
- calibration 时生成的文本；
- publication 中的新表达；
- evaluator 对“像不像”的主观印象；
- 另一个派生作者的 memory。

这由 `POLICY-PROVENANCE-001` 强制执行。

## 八、研究完成的含义

完成某个研究文件不表示“作者已经被解释完”。完成意味着：

- 资料与 rights 可追溯；
- claim 可定位到版本化 segment；
- 反例和限制被记录；
- confidence 与 status 明确；
- source model 只接受经过门槛的内容；
- 未解决问题继续保留在 limitations 和 open questions 中。
