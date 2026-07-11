# Pre-Real-Run Complete Repository Upgrade Implementation Plan

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

> **For agentic workers:** This plan has been executed and verified. The checkboxes record completed work; they are not a request to create a parallel repository version.

**Goal:** Upgrade the existing Author Lab reference scaffold directly into a complete pre-real-run repository whose contracts, scaffolding, storage rules, state model, publication gates, experiment interface, tests, and documentation agree.

**Architecture:** Preserve evidence → research → source model → derived author → work item → evaluation/experiment → publication. Replace hard-coded or duplicated assumptions with manifest-driven discovery, executable schema registration, canonical scaffold templates, explicit lifecycle/stage/gate state, reproducible run records, and transactional publication.

**Tech Stack:** Python 3.11, JSON Schema Draft 2020-12, JSON, JSONL, Markdown, pytest, GitHub Actions.

## Global constraints satisfied

- [x] No parallel legacy/new directory structures were created.
- [x] No real source-author claims, held-out content, model runs, evaluation scores, or experiment conclusions were fabricated.
- [x] Runtime and publication categories were not expanded beyond the existing architecture.
- [x] Every new managed file contains the required sample marker.
- [x] Production machine documents are schema registered or explicitly classified as schemas/templates.
- [x] Cross-references used by source research, models, personas, work items, experiments, and publications resolve.
- [x] Behavior changes received regression tests.

---

## Task 1 — Repository readiness, components, placeholders, and storage

- [x] Added repository mode and pre-real-run readiness to the project manifest.
- [x] Added component, placeholder, and source-storage registers.
- [x] Distinguished infrastructure readiness, real-content status, and experimental validation.
- [x] Protected primary-source binaries with Git ignore rules while preserving README files.
- [x] Replaced repository-local copyrighted-source paths with registered external storage URIs.
- [x] Added reference-sample and active-author-lab placeholder behavior with tests.

## Task 2 — Executable machine-readable contracts

- [x] Added the document path-pattern → JSON Schema registry.
- [x] Added schema execution for JSON and JSONL records.
- [x] Rejected production machine documents without a schema or explicit template/schema classification.
- [x] Tightened stable contracts with `additionalProperties: false` where appropriate.
- [x] Added schemas for repository control, evidence, rights, storage, segments, research claims, provenance, source/derived models, loading maps, indexes, work items, runs, reviews, experiments, evaluations, publication, policies, and site configuration.
- [x] Added invalid-document and coverage tests.

## Task 3 — Manifest-driven structure and cross-references

- [x] Removed Sample A/B/C names from structure discovery.
- [x] Made project manifest and persona template the structure authorities.
- [x] Built ID/version/path indexes for source authors, source models, personas, derived models, runbooks, runtimes, work items, experiments, and publications.
- [x] Validated runbook artifacts/templates/policies, work-item stages/artifacts, experiment conditions/controls, and publication links.
- [x] Added source corpus ↔ rights ↔ storage ↔ normalized text ↔ segment-map validation.

## Task 4 — Lifecycle, stage execution, and quality gates

- [x] Removed the overloaded legacy work-item `status` and `reviews` structure.
- [x] Added `lifecycle_status`, `stage_executions`, and `quality_gates`.
- [x] Added stage/gate consistency validation and regression tests.
- [x] Converted the sample work item without retaining parallel legacy fields.

## Task 5 — Runbook-driven work-item scaffolding

- [x] Made runbook manifests authoritative for stages, required artifacts, artifact templates, and policy IDs.
- [x] Added missing templates for drafts, reviews, sources, authorized scenes/text, semantic review, and final output.
- [x] Made the scaffolder resolve persona model, runbook, and runtime versions.
- [x] Added behavior tests proving custom runbook artifacts/stages are generated without hard-coded defaults.

## Task 6 — Complete persona template and generated views

- [x] Added one complete derived-author persona template manifest.
- [x] Made the persona generator render the template and self-check required paths.
- [x] Added full lineage, derivation, core model, genre, memory, harness, evaluation, and index structure.
- [x] Replaced persona-local duplicate work/publication storage with generated JSONL indexes.
- [x] Added index rebuilding and complete template behavior tests.

## Task 7 — Versioned source segmentation and provenance

- [x] Added edition ID, segmentation version, ordinal, and SHA-256 to segment identity.
- [x] Generated a JSONL source-location map.
- [x] Removed the claim that simple ordinal IDs remain stable across re-segmentation.
- [x] Updated sample normalized text and research claim references.
- [x] Added segment → research claim → source-model rule/model-file provenance validation and tests.

## Task 8 — Transactional publication gate

- [x] Added tests for pending editor approval, missing final file, and successful publication.
- [x] Added gate, stage, persona/model version, metadata, and canonical-file validation.
- [x] Added staging, atomic replacement, manifest rebuild, state update, and rollback.
- [x] Made publication-manifest rebuilding execute the gate rather than merely aggregate JSON.

## Task 9 — Formal experiment object and held-out boundary

- [x] Added the first-class `author-model-experiments/` layer.
- [x] Added generic, source-model-direct, Derived B, and Derived C conditions.
- [x] Added shared controlled execution: runtime/runbook versions, model parameters, context budget, tool permissions, repetition count, and randomness control.
- [x] Required evaluator-only `evaluator-storage://` held-out URIs.
- [x] Added runtime-run, raw-result, aggregate-analysis, failure-case, and conclusion contracts without fabricated results.
- [x] Added experiment scaffolding tests.

## Task 10 — Canonical policy rules

- [x] Added the policy-rule register and schema.
- [x] Added canonical IDs for provenance, derivation, factuality, originality, publication, and held-out isolation.
- [x] Updated root/shared AGENTS, relevant skills, prompts, and runbooks to reference policy IDs.
- [x] Added repository-wide unknown-policy-reference validation and tests.

## Task 11 — Reproducible runs

- [x] Expanded writing-run manifests with commit SHA, model/runbook/runtime versions, model parameters, context budget, tool permissions, loaded-file hashes, outputs, timestamps, and exit status.
- [x] Marked the sample run explicitly `not-run` instead of pretending it executed.
- [x] Added completed-run hash, version, and output validation with tests.
- [x] Added a formal experiment runtime-run schema.

## Task 12 — Documentation and CI

- [x] Updated the root README with accurate pre-real-run status.
- [x] Rewrote the complete path-by-path repository reference.
- [x] Updated architecture/data-flow, research methodology, state-machine, documentation index, and changelog.
- [x] Recorded the direct repository milestone without a parallel repository-version scheme.
- [x] Added structure, syntax, schema, cross-reference, provenance, policy, state, run reproducibility, placeholder, and pytest steps to GitHub Actions.
- [x] Preserved failure diagnostics as an Actions artifact when placeholder validation fails.

## Verification result

Final PR-head GitHub Actions run:

- Workflow: `Validate Author Lab Repository`
- Run: `29146477581` / run number `132`
- Job: `validate-repository` (`86528806105`)
- Result: `success`

Successful steps:

1. repository structure;
2. JSON/JSONL syntax;
3. registered machine-readable contracts;
4. repository cross references;
5. source research and model provenance;
6. canonical policy references;
7. work-item states;
8. writing-run reproducibility;
9. repository-mode-aware placeholders;
10. all pytest tests.

The successful validation proves internal repository consistency and executable pre-real-run contracts. It does not claim that real source-author research or a real A→B/C experiment has been completed.
