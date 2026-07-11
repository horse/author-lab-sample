# Pre-Real-Run Complete Repository Upgrade Implementation Plan

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Upgrade the existing Author Lab reference scaffold directly into a complete pre-real-run repository whose contracts, scaffolding, storage rules, state model, publication gates, experiment interface, tests, and documentation agree.

**Architecture:** Keep the existing evidence → research → source model → derived author → work item → evaluation → publication structure. Replace duplicated hard-coded assumptions with manifest-driven discovery, a document schema registry, a persona scaffold template, runbook-driven work-item generation, explicit lifecycle/stage/gate state, and transactional publication validation.

**Tech Stack:** Python 3.11, JSON Schema Draft 2020-12, JSON, JSONL, Markdown, pytest, GitHub Actions.

## Global Constraints

- Do not create parallel legacy and new structures.
- Do not generate real experiment results or held-out evaluation content.
- Do not expand runtime or publication categories beyond the existing scope.
- Every created file must contain the required sample marker using valid syntax.
- Every machine-readable contract must be validated by an executable registry entry.
- Every cross-reference used by a work item or publication must resolve.
- Tests must be added before behavior changes.

---

### Task 1: Repository readiness, component, placeholder, and storage registers

**Files:**
- Modify: `author-lab-project-manifest.json`
- Create: `repository-component-status-register.json`
- Create: `repository-placeholder-register.json`
- Create: `source-material-storage-and-ingestion-register.jsonl`
- Modify: `.gitignore`
- Modify: `source-authors/source-author-sample/source-corpus/source-corpus-manifest.jsonl`
- Modify: `source-authors/source-author-sample/source-rights-register.jsonl`
- Test: `repository-validation-tests/test_repository_mode_and_registers.py`

- [ ] Write tests for repository mode, component path resolution, placeholder behavior, and external source-material storage.
- [ ] Verify tests fail against the current scaffold.
- [ ] Add the registers and update the project manifest and storage records.
- [ ] Update Git ignore rules to prevent primary-source binaries from entering Git while preserving README files.
- [ ] Verify tests pass.

### Task 2: Executable JSON Schema registry

**Files:**
- Create: `shared-writing-harness/machine-readable-contracts/document-schema-registry.json`
- Create: `shared-writing-harness/machine-readable-contracts/repository-component-status-register.schema.json`
- Create: `shared-writing-harness/machine-readable-contracts/repository-placeholder-register.schema.json`
- Create: `shared-writing-harness/machine-readable-contracts/source-material-storage-record.schema.json`
- Create: `repository-automation-scripts/validate_machine_readable_contracts.py`
- Modify: existing core schemas to cover all required fields and reject misspelled properties
- Test: `repository-validation-tests/test_machine_readable_contract_validation.py`

- [ ] Write failing tests for missing required fields and a valid repository-wide validation run.
- [ ] Verify the invalid document is rejected for the intended schema reason.
- [ ] Implement the path-pattern schema registry and JSON/JSONL record validation.
- [ ] Tighten core schemas without invalidating valid sample documents.
- [ ] Verify tests pass.

### Task 3: Manifest-driven structure and cross-reference validation

**Files:**
- Modify: `repository-automation-scripts/validate_author_lab_repository_structure.py`
- Create: `repository-automation-scripts/validate_repository_cross_references.py`
- Test: `repository-validation-tests/test_manifest_driven_structure_validation.py`
- Test: `repository-validation-tests/test_repository_cross_reference_validation.py`

- [ ] Write failing tests proving validators no longer depend on Sample A/B/C names and reject missing runbooks/models/runtimes.
- [ ] Implement discovery from `author-lab-project-manifest.json`.
- [ ] Build ID and version indexes for authors, models, personas, runbooks, runtimes, work items, and publications.
- [ ] Verify all current references resolve.

### Task 4: Separate lifecycle, stage execution, and quality gates

**Files:**
- Modify: `shared-writing-harness/machine-readable-contracts/writing-work-item-state.schema.json`
- Modify: `repository-automation-scripts/validate_writing_work_item_state.py`
- Modify: `writing-work-items/2026-writing-work-items/2026-001-sample-article/work-item-state.json`
- Test: `repository-validation-tests/test_writing_work_item_state_machine.py`

- [ ] Replace tests for the old overloaded state field with failing tests for lifecycle, stages, and gates.
- [ ] Implement the new state validator.
- [ ] Convert the sample work item without retaining parallel legacy fields.
- [ ] Verify tests pass.

### Task 5: Runbook-driven work-item scaffolding

**Files:**
- Modify: all `shared-writing-harness/writing-runbooks/*/writing-runbook-manifest.json`
- Create: missing artifact templates under `shared-writing-harness/artifact-templates/`
- Modify: `repository-automation-scripts/create_new_writing_work_item.py`
- Test: `repository-validation-tests/test_runbook_driven_work_item_scaffolding.py`

- [ ] Write a failing test that creates a work item and expects exact runbook artifacts and initialized stage records.
- [ ] Add canonical artifact-template mappings to runbook manifests.
- [ ] Make the scaffolder resolve persona model and runtime versions and create artifacts from the selected runbook.
- [ ] Verify generated work items pass schema and state validation.

### Task 6: Complete persona scaffold template

**Files:**
- Create: `shared-writing-harness/scaffold-templates/derived-author-persona-template/`
- Modify: `repository-automation-scripts/create_new_derived_author_persona.py`
- Create: `repository-automation-scripts/rebuild_derived_author_indexes.py`
- Add generated work-item and publication index files for Sample B/C
- Test: `repository-validation-tests/test_complete_derived_author_persona_scaffolding.py`

- [ ] Write a failing test expecting the complete required persona structure.
- [ ] Create one template manifest and generic file templates covering the full persona model.
- [ ] Make the generator render the template rather than maintain a second hard-coded structure.
- [ ] Make persona work/publication views generated JSONL indexes rather than duplicate canonical text.
- [ ] Verify Sample B/C satisfy the same template contract.

### Task 7: Versioned source segmentation

**Files:**
- Modify: `repository-automation-scripts/normalize_authorized_plain_text_source.py`
- Modify: `repository-validation-tests/test_authorized_plain_text_normalization.py`
- Modify: `documentation/source-author-research-methodology.md`

- [ ] Write failing tests requiring edition ID, segmentation version, and content fingerprints.
- [ ] Implement versioned segment anchors and a JSONL location map.
- [ ] Remove claims that ordinal paragraph IDs are stable across re-segmentation.
- [ ] Verify tests pass.

### Task 8: Transactional publication gate

**Files:**
- Create: `repository-automation-scripts/publish_approved_writing_work_item.py`
- Modify: `repository-automation-scripts/build_approved_publication_manifest.py`
- Test: `repository-validation-tests/test_transactional_publication_gate.py`

- [ ] Write failing tests for rejected pending editorial approval, missing final file, and a valid approved publication.
- [ ] Implement work-item, gate, persona, model, metadata, and canonical-file validation.
- [ ] Update publication state only after all output operations succeed.
- [ ] Verify manifest rebuilding rejects invalid metadata.

### Task 9: Formal experiment object and held-out boundary

**Files:**
- Create: `author-model-experiments/README.md`
- Create: `author-model-experiments/AGENTS.md`
- Create: `author-model-experiments/experiment-scaffold-template/`
- Create: `shared-writing-harness/machine-readable-contracts/author-model-experiment-manifest.schema.json`
- Create: `repository-automation-scripts/create_new_author_model_experiment.py`
- Test: `repository-validation-tests/test_author_model_experiment_scaffolding.py`

- [ ] Write a failing test for a four-condition experiment scaffold and evaluator-only held-out URI.
- [ ] Implement the experiment manifest and directory template without results.
- [ ] Require generic, source-model-direct, derived-author-b, and derived-author-c condition roles.
- [ ] Reject local writer-readable held-out material paths.

### Task 10: Canonical policy rule registry

**Files:**
- Create: `shared-writing-harness/harness-policies/policy-rule-register.jsonl`
- Create: `shared-writing-harness/machine-readable-contracts/policy-rule-record.schema.json`
- Modify: `AGENTS.md`
- Modify: `shared-writing-harness/AGENTS.md`
- Modify: relevant skills and prompts to cite rule IDs
- Test: `repository-validation-tests/test_policy_rule_references.py`

- [ ] Write failing tests for unknown policy-rule references.
- [ ] Register canonical policy IDs and source files.
- [ ] Convert repeated agent, skill, prompt, and rubric reminders into summaries with rule references.
- [ ] Verify every referenced policy ID exists.

### Task 11: Documentation, README status, and CI

**Files:**
- Modify: `README.md`
- Modify: `documentation/complete-repository-file-and-directory-reference.md`
- Modify: `documentation/repository-architecture-and-data-flow.md`
- Modify: `documentation/writing-work-item-state-machine.md`
- Modify: `.github/workflows/validate-author-lab-repository.yml`
- Modify: `CHANGELOG.md`

- [ ] Document Core, Optional, Example, and implementation states.
- [ ] Document external source storage, placeholder modes, executable contracts, experiment objects, and held-out isolation.
- [ ] Add schema and cross-reference validation to CI.
- [ ] Run every validation script and pytest.
- [ ] Confirm the final branch is green before merge.
