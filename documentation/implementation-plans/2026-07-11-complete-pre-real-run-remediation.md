# Complete Pre-Real-Run Remediation Implementation Plan

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans and superpowers:test-driven-development. Every behavior change begins with a failing regression test.

**Goal:** Repair every externally identified pre-real-run blocker, strengthen the remaining weak contracts, verify the merged tree, and remove stale merged branches.

**Architecture:** Keep the existing one-way Author Lab data model. Add shared repository-mode and transaction helpers, make scaffolders atomic and self-registering, namespace provenance by source author, pin experiment/run history immutably, and make CI independently enforce publication integrity and generated indexes.

**Tech Stack:** Python 3.11, JSON Schema Draft 2020-12, JSON/JSONL, Markdown, pytest, Ruff, GitHub Actions.

## Global constraints

- Do not create parallel legacy/new directory structures.
- Remove the legacy single `writing-run-manifest.json` contract rather than supporting both forms.
- Do not fabricate source research, held-out material, runtime results, evaluation scores, or publications.
- Reference-sample mode retains sample markers; active-author-lab mode must generate unmarked production records.
- All generators must be all-or-nothing from the caller's perspective.
- Every machine-readable production document must remain schema-registered.
- Final success requires a fresh workflow on the exact merged `main` commit.

---

### Task 1: Repository-mode support and active-mode regression tests

**Files:**
- Create: `repository-automation-scripts/repository_mode_support.py`
- Create: `repository-validation-tests/test_active_repository_mode_generation.py`
- Modify: `repository-automation-scripts/validate_sample_comment_markers.py`
- Modify: all persona/work-item/experiment/publication/index generators

**Interfaces:**
- Produces `RepositoryModeContext.from_project(root)`, `json_marker_fields()`, `markdown_marker()`, `initial_status(sample, active)`, and `register_generated_placeholders(paths)`.

- [ ] Write tests proving every generator emits markers only in `reference-sample` mode and emits no sample sentinel strings in `active-author-lab` mode.
- [ ] Run the focused tests and confirm they fail on current unconditional marker behavior.
- [ ] Implement the shared mode context and migrate all generators/index builders.
- [ ] Run focused and full tests.

### Task 2: Atomic scaffolding and persona registration

**Files:**
- Create: `repository-automation-scripts/atomic_repository_update.py`
- Modify: `create_new_derived_author_persona.py`
- Modify: `create_new_writing_work_item.py`
- Modify: `create_new_author_model_experiment.py`
- Modify: `repository-component-status-register.json`
- Test: `test_atomic_scaffolding_and_registration.py`

**Interfaces:**
- Produces `staged_directory(target)`, `atomic_json_updates(updates)`, and recovery-safe cleanup.

- [ ] Write failing tests for missing source model, wrong source-model version, automatic manifest/component registration, and no partial directory after rendering failure.
- [ ] Implement temporary-sibling generation and atomic registration.
- [ ] Validate newly generated persona/work item/experiment with structure, schemas, and cross references before commit.
- [ ] Run focused and full tests.

### Task 3: Author-scoped accepted provenance

**Files:**
- Modify schemas: research claim and source-model provenance.
- Modify sample JSONL records.
- Modify `validate_source_research_and_model_provenance.py`.
- Modify research/model methodology documentation.
- Test: `test_author_scoped_provenance.py`.

- [ ] Write failing tests for cross-author segment use, cross-author claim use, and an approved model rule backed by an unaccepted claim.
- [ ] Add `source_author_id` and `source_author_model_id` contract fields and status enums.
- [ ] Build per-author segment/claim indexes and enforce accepted-claim gates.
- [ ] Run focused and full tests.

### Task 4: Version-pinned distinct experiment conditions

**Files:**
- Modify `author-model-experiment-manifest.schema.json`.
- Modify experiment scaffold and generator.
- Modify cross-reference validator.
- Test: `test_experiment_condition_pinning.py`.

- [ ] Write failing tests for duplicate roles/IDs, identical B/C personas, missing model versions, and drift from current manifests.
- [ ] Store exact persona, derived model, source model IDs and versions per condition.
- [ ] Enforce role uniqueness, condition-ID uniqueness, and B/C distinction.
- [ ] Run focused and full tests.

### Task 5: Immutable multi-run history

**Files:**
- Delete: sample `writing-run-manifest.json`.
- Create: sample `writing-runs/run-sample-not-run.json` and `writing-runs/README.md`.
- Modify schema registry and run schema.
- Modify work-item scaffolder and reproducibility validator.
- Test: `test_immutable_writing_run_history.py`.

- [ ] Write failing tests for multiple run records, duplicate run IDs, unknown commits, historical hashes, path traversal, and active-mode sample not-run records.
- [ ] Move the canonical contract to `writing-work-items/**/writing-runs/run-*.json`.
- [ ] Validate hashes against `git show <commit>:<path>` rather than current HEAD.
- [ ] Ensure output artifacts are immutable run-scoped paths.
- [ ] Run focused and full tests.

### Task 6: Recoverable publication transaction and independent CI gate

**Files:**
- Modify `publication_gate_support.py`, publisher, manifest builder, index builder.
- Create `validate_publication_integrity.py`.
- Modify workflow and schema/registry as needed.
- Extend `test_transactional_publication_gate.py`.

- [ ] Write failing tests for staging failure cleanup, manifest/state replacement failure rollback, empty manifest, interrupted journal recovery, stale persona indexes, and manual gate bypass.
- [ ] Move all staging work inside guarded cleanup and add lock/journal recovery.
- [ ] Make empty JSONL canonical; remove Sample B sentinel.
- [ ] Prepare canonical files, manifest, state, and indexes before applying replacements.
- [ ] Add read-only publication-integrity validation to CI.
- [ ] Run focused and full tests.

### Task 7: Lifecycle semantics, generated-index validation, and documentation parity

**Files:**
- Modify work-item state schema/validator/sample.
- Modify cross-reference/index validation.
- Modify README, AGENTS, state-machine docs, complete repository guide, changelog, component status.
- Modify workflow and dependency files.
- Tests: lifecycle/archive and index-integrity tests.

- [ ] Write failing tests for rejected/cancelled/abandoned/superseded archive flows and malformed publication linkage.
- [ ] Add lifecycle statuses and typed publication/archive fields.
- [ ] Validate generated persona indexes exactly match canonical objects.
- [ ] Make README and AGENTS command lists identical to CI.
- [ ] Pin Actions by commit SHA, add a Python constraints file, and run Ruff in CI.
- [ ] Run every validation command, pytest, and Ruff.

### Task 8: External review, merge, exact-main verification, and branch cleanup

**Files:**
- Update this plan with final evidence.
- Update PR description with limitations and verification.

- [ ] Open PR from `fix/complete-pre-real-run-remediation` to `main`.
- [ ] Inspect all changed files and review threads.
- [ ] Require a successful merge-ref workflow.
- [ ] Squash merge with expected head SHA.
- [ ] Confirm the exact merged `main` commit has a successful push workflow.
- [ ] Delete `scaffold/complete-author-lab-architecture`, `documentation/complete-repository-file-guide`, `upgrade/pre-real-run-complete`, and the remediation branch.
- [ ] Confirm only intended active branches remain and report any connector limitation transparently.
