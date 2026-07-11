# Repository Instructions for Agents

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

## Default operating mode

This repository contains source-author evidence, source-author research, compiled source models, multiple derived-author personas, work items, evaluations, experiments, and publications. The default mode is repository maintenance, not author simulation.

Do not write as a source author. Enter a derived-author writing mode only when a canonical work item explicitly names:

- one `derived_author_id`;
- one `derived_author_model_id` and version;
- one runbook and version;
- one runtime adapter and configuration version.

## Source-of-truth hierarchy

1. `source-authors/` — source evidence, rights, storage, normalization, and segment maps.
2. `source-author-research/` — author-scoped evidence-backed claims, counterexamples, confidence, and limitations.
3. `source-author-models/` — compact models compiled from accepted claims with provenance.
4. `derived-author-personas/` — independent lineage, derivation, models, memory, and generated indexes.
5. `shared-writing-harness/` — author-neutral contracts, runbooks, policies, prompts, and templates.
6. `writing-work-items/` — task-specific state, stages, gates, immutable runs, sources, drafts, and reviews.
7. `author-model-evaluations/` and `author-model-experiments/` — measurement and version-pinned controlled comparisons.
8. `approved-publications/` — canonical approved output created through a recoverable transaction; never source-author evidence.

When records conflict, higher layers prevail. No downstream output may silently mutate an upstream layer.

Canonical policy rules:

- `POLICY-PROVENANCE-001` — generated output never becomes source-author evidence.
- `POLICY-DERIVATION-001` — derived authors may not claim source identity, experience, relationships, credentials, or endorsement.
- `POLICY-FACTUALITY-001` — external truth claims require classification and support.
- `POLICY-ORIGINALITY-001` — source text, calibration examples, previous publications, and other personas are not phrase banks or structural templates.
- `POLICY-PUBLICATION-001` — publication requires passed factual/style gates, editor approval, valid metadata, a verified final file, and publication-integrity validation.
- `POLICY-HELDOUT-001` — real held-out evaluation material remains outside writer-readable storage.

Full rule records are in `shared-writing-harness/harness-policies/policy-rule-register.jsonl`.

## Loading rules

- Source ingestion loads the source profile, corpus manifest, rights register, storage register, and normalization documentation.
- Source-author research loads authorized source evidence and research methods; it never loads derived-author output as evidence.
- Source-model compilation loads accepted research claims, limitations, and author-scoped provenance records.
- Persona design resolves an existing source model and exact version, then records inherited, transformed, rejected, and original traits separately.
- Writing loads only the selected persona manifest, lineage, derivation profile, loading-map core files, one genre mode, selected runbook, current brief, and current research pack.
- Fact review should not load style prompts unless needed to identify unsupported narrative invention.
- Style review must not alter factual claims or silently resolve factual failures.
- Writing agents must not load evaluator-only held-out content, blind labels, raw evaluation results, or experiment conclusions.
- Runtime adapters may supply execution settings but may not carry hidden author identity or weaken gates.

## Mutation rules

- Never commit restricted primary-source binaries to ordinary Git history. Use the registered external storage URI unless repository storage is explicitly authorized.
- Never overwrite source evidence. Add a new edition or source record and preserve the old record.
- Re-segmentation creates a new `segmentation_version`; do not reuse old segment IDs.
- Research claims and model provenance must remain within one `source_author_id`; cross-author references are invalid.
- Only an accepted research claim may support an approved source-model rule.
- Every derived author must be created through the canonical complete template, resolve an exact source-model version, register in the project manifest/component register, and maintain independent memory and generated indexes.
- Runbook manifests are the sole authority for required stages and artifacts. Do not hard-code a second list in scripts.
- Scaffolding must occur in a temporary sibling directory and be promoted only after complete rendering and validation.
- Work-item drafts, run records, reviews, failed stages, excluded runs, and experiment failure cases are append-only historical evidence; do not erase them.
- Every execution receives a new `writing-runs/run-*.json`; never overwrite an existing run or compare historical inputs with current HEAD.
- Persona work/publication directories contain generated indexes only. Canonical content remains in root work-item and publication directories.
- Publish only through `publish_approved_writing_work_item.py`; do not copy a draft directly into `approved-publications/` or hand-edit its manifest/indexes.
- Do not put credentials, API keys, private personal data, unauthorized copyrighted sources, or real held-out materials in Git.

## Repository modes

- `reference-sample`: populated managed records retain the sample marker; a canonical JSONL manifest may be genuinely empty.
- `active-author-lab`: only paths registered in `repository-placeholder-register.json` may retain markers; generated production records must not contain sample markers, statuses, checksums, or sentinel IDs.

Never switch modes by deleting markers alone. Update the project manifest, placeholder register, source/persona content, and validation state together.

## Naming and identity rules

Use descriptive kebab-case for directories and documents and snake_case for Python files. Preserve tool-standard names such as `README.md`, `AGENTS.md`, `SKILL.md`, `CODEOWNERS`, and workflow filenames.

IDs and versions in manifests are contracts, not display text. Renaming a directory does not automatically change its ID; changing an ID requires all references and indexes to be updated.

## Required checks

Before declaring repository work complete, run exactly the CI validation sequence:

```bash
python -m pip install -c validation-constraints.txt -e '.[development]'
python repository-automation-scripts/validate_author_lab_repository_structure.py
python repository-automation-scripts/validate_json_and_jsonl_documents.py
python repository-automation-scripts/validate_machine_readable_contracts.py
python repository-automation-scripts/validate_repository_cross_references.py
python repository-automation-scripts/validate_source_research_and_model_provenance.py
python repository-automation-scripts/validate_policy_rule_references.py
python repository-automation-scripts/validate_writing_work_item_state.py
python repository-automation-scripts/validate_writing_run_reproducibility.py
python repository-automation-scripts/validate_publication_integrity.py
python repository-automation-scripts/validate_sample_comment_markers.py
ruff check repository-automation-scripts repository-validation-tests
pytest repository-validation-tests --tb=short
```

A green validation suite proves repository contracts are internally consistent. It does not prove a real source-author model or A→B/C experiment has succeeded.
