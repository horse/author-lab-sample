# Factual Review Stage Prompt

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

Required policy rule: `POLICY-FACTUALITY-001`.

Extract factual and quasi-factual claims from the current draft. Classify each claim, verify direct support and date scope, record sources, identify fabricated quotations, scenes, relationships, credentials, autobiographical assertions, and unsupported narrative invention, then output a document conforming to `factual-review-result.schema.json`.

Do not revise style, rescue unsupported claims through tone, or mark the quality gate directly. The reviewer writes the review artifact; the state transition occurs only after the review result is accepted.
