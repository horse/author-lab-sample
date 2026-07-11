# Publication Preparation Stage Prompt

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

Required policy rule: `POLICY-PUBLICATION-001`.

Confirm that factual accuracy and persona/style gates passed, editor approval is explicit, required review stages are completed, the final file is non-empty, and persona/model IDs and versions still match the work item.

Do not manually copy a file or edit the publication manifest. Prepare the arguments and invoke `repository-automation-scripts/publish_approved_writing_work_item.py`. The transaction creates canonical content and metadata, rebuilds the publication manifest, updates the work-item state, and rolls back on failure.
