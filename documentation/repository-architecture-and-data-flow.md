# Repository Architecture and Data Flow

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

The repository separates evidence, interpretation, executable models, derived identities, task execution, evaluation, and publication.

```text
source-author corpus
  → evidence-backed research claims
  → versioned source-author model
  → derived-author derivation profile
  → derived-author executable model
  → work item using a selected runbook and runtime
  → factual review + style review + editor approval
  → approved publication
```

No downstream artifact may silently modify an upstream layer. Generated publications may improve harness engineering but cannot validate claims about a source author.