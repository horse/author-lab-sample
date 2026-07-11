# Complete Pre-Real-Run Remediation Implementation Plan

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

> **For agentic workers:** This plan was executed test-first. The remaining unchecked items are post-merge operational closure, not unimplemented repository behavior.

**Goal:** Repair every externally identified pre-real-run blocker, strengthen the remaining weak contracts, verify the merged tree, and remove stale merged branches.

**Architecture:** Preserve the existing one-way Author Lab data model. Use shared repository-mode and atomic-update helpers, author-scoped provenance, exact experiment versions, immutable commit-pinned runs, and independently validated recoverable publication.

**Tech Stack:** Python 3.11, JSON Schema Draft 2020-12, JSON/JSONL, Markdown, pytest, Ruff, GitHub Actions.

## Global constraints satisfied

- [x] No parallel legacy/new directory structures were created.
- [x] The legacy single `writing-run-manifest.json` contract was removed rather than supported in parallel.
- [x] No source research, held-out material, runtime results, evaluation scores, or publications were fabricated.
- [x] Reference-sample mode retains markers; active-author-lab generators emit unmarked production records.
- [x] Persona, work-item, and experiment scaffolding is staged and atomic from the caller's perspective.
- [x] Every production machine-readable document remains schema-registered.
- [x] Behavior changes were introduced with failing regression tests and finished with a green full suite.

---

## Task 1 — Repository-mode support and active-mode generation

- [x] Added `repository_mode_support.py`.
- [x] Migrated persona, work-item, experiment, publication, and index generation.
- [x] Active mode rejects markers, fake checksums, sample statuses, and `SAMPLE-*` sentinels.
- [x] Added direct active-mode tests for persona, work item, experiment, and publication.

## Task 2 — Atomic scaffolding and persona registration

- [x] Added `atomic_repository_update.py`.
- [x] Persona creation resolves exact source-model ID/version.
- [x] Persona creation updates project manifest and component register.
- [x] Persona, work-item, and experiment rendering happens in temporary sibling directories.
- [x] Rendering or registration failure leaves no canonical partial object.

## Task 3 — Author-scoped accepted provenance

- [x] Research claims require `source_author_id` and constrained statuses.
- [x] Source-model provenance requires source author/model IDs and constrained statuses.
- [x] Segment and claim indexes are isolated by source author.
- [x] Cross-author segment and claim references fail.
- [x] Approved model rules require accepted claims.

## Task 4 — Version-pinned distinct experiment conditions

- [x] Conditions store exact persona, author-model, and source-model IDs/versions.
- [x] Generic baseline cannot load author data.
- [x] Source-direct baseline pins an exact source model.
- [x] B and C must be distinct personas with exact derived/upstream model versions.
- [x] Condition roles and condition IDs must be unique.

## Task 5 — Immutable multi-run history

- [x] Removed the legacy sample `writing-run-manifest.json`.
- [x] Added `writing-runs/run-*.json` and run-specific output directories.
- [x] Validator supports multiple immutable runs and duplicate-run detection.
- [x] Loaded-file hashes are checked with `git show <commit>:<path>`.
- [x] Unknown commits, path traversal, non-run-scoped outputs, and active fake not-run records fail.

## Task 6 — Recoverable publication transaction and independent CI gate

- [x] Zero publications use an empty canonical JSONL manifest.
- [x] Removed the Sample B publication sentinel from records, indexes, helpers, and schema.
- [x] Added publication lock, journal, staging, backups, recovery, and rollback.
- [x] Manifest, state, and persona indexes are precomputed and updated together.
- [x] Canonical article hash must equal the work-item final approved article hash.
- [x] Added `validate_publication_integrity.py` to detect manual bypass and stale indexes.
- [x] Added staging failure, journal recovery, empty-manifest, manual-bypass, active-mode, and stale-index tests.

## Task 7 — Lifecycle, generated indexes, CI, dependencies, and documentation

- [x] Added rejected, cancelled, abandoned, and superseded lifecycle outcomes.
- [x] Archived work requires an archive reason without requiring successful gates.
- [x] Publication linkage is a typed state object.
- [x] Persona work/publication indexes are deterministic and validated against canonical objects.
- [x] README and AGENTS use the exact CI validation sequence.
- [x] GitHub Actions are pinned to commit SHAs and checkout full Git history.
- [x] Added `validation-constraints.txt` and Ruff to CI.
- [x] Rewrote the canonical repository reference, architecture, research methodology, state-machine documentation, navigation, component status, and changelog.

## Task 8 — External review, merge, exact-main verification, and branch cleanup

- [x] Opened PR #4 from `fix/complete-pre-real-run-remediation` to `main`.
- [x] Inspected all changed filenames and found no unresolved review threads before finalization.
- [x] Required and obtained a successful fresh merge-ref workflow.
- [ ] Squash merge with expected head SHA.
- [ ] Confirm the exact merged `main` tree through its push workflow or equivalent content verification.
- [ ] Remove stale branch content and delete branch refs where connector permissions support deletion.
- [ ] Record any unavoidable connector limitation transparently.

## Fresh pre-merge verification

PR head:

```text
e9c644fc0730c03d9027e41cac676b5552471205
```

GitHub Actions:

```text
Workflow: Validate Author Lab Repository
Run ID: 29149029766
Run number: 195
Job ID: 86535385337
Conclusion: success
```

Successful steps:

1. repository structure;
2. JSON/JSONL syntax;
3. registered machine-readable contracts;
4. repository cross references and generated indexes;
5. author-scoped source research/model provenance;
6. canonical policy references;
7. work-item state;
8. immutable writing-run reproducibility;
9. publication integrity;
10. repository-mode placeholders and sentinels;
11. Ruff;
12. all pytest tests.

This proves the repository's pre-real-run contracts are internally executable and consistent. It does not claim that real source-author research or a real A→B/C experiment has been completed.
