# Repository Instructions for Agents

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

## Default operating mode

This repository contains source-author research and multiple derived-author personas. The default mode is repository-maintenance mode, not author simulation.

Do not write as a source author. Enter a derived-author writing mode only when a work item explicitly names a directory under `derived-author-personas/` and a runbook under `shared-writing-harness/writing-runbooks/`.

## Source-of-truth hierarchy

1. `source-authors/` — immutable source evidence and rights records.
2. `source-author-research/` — evidence-backed interpretation.
3. `source-author-models/` — approved compact models compiled from research.
4. `derived-author-personas/` — transformed author identities and models.
5. `shared-writing-harness/` — execution rules and quality gates.
6. `writing-work-items/` — task-specific state and artifacts.
7. `approved-publications/` — approved output, never evidence about a source author.

When records conflict, higher items in this list prevail. Generated output must never be used to prove a claim about a source author.

## Loading rules

- Source normalization tasks load only the relevant source manifest, rights record, and normalization documentation.
- Source-author research tasks load source evidence and research methods; they do not load derived-author publications.
- Source-model compilation loads accepted research claims and provenance records.
- Writing tasks load the selected derived-author model, one genre mode, one runbook, and the current work-item research pack.
- Fact review does not load style prompts unless needed to identify unsupported narrative invention.
- Style review does not change factual claims.
- Held-out evaluation materials must not be loaded by the writing agent.

## Mutation rules

- Never overwrite files in `primary-source-materials/`; add a new version and update the manifest.
- Every research conclusion must cite evidence identifiers.
- Every source-model rule must cite accepted research claims in a provenance record.
- Every derived author must record inherited, transformed, rejected, and original traits.
- Publishing requires factual review passed, style review passed, and editor approval.
- Do not put credentials, model API keys, copyrighted source files without permission, or private personal data in Git.

## Naming rules

Use descriptive kebab-case directory and document names. Use descriptive snake_case Python filenames. Preserve conventional names where tools expect them, including `README.md`, `AGENTS.md`, `SKILL.md`, `CODEOWNERS`, and workflow filenames.

## Required checks

Run all validation scripts and tests before declaring repository work complete. Do not claim success from generated text alone; inspect exit codes and test output.