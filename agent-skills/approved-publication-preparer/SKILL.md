---
name: approved-publication-preparer
description: Prepare an approved work item for canonical publication after all gates pass.
---

# Approved Publication Preparer

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

Required policy rule: `POLICY-PUBLICATION-001`.

Do not manually copy a draft into `approved-publications/`. Invoke `repository-automation-scripts/publish_approved_writing_work_item.py` with a valid publication ID, title, category, status, and timestamp when applicable.

The transaction must verify factual and persona/style gates, editor approval, completed review stages, a non-empty final file, the selected persona/model ID and version, metadata, canonical path, and manifest consistency. After publication, rebuild derived-author indexes and run the full validation suite. A copied file without a successful transaction is not a canonical publication.
