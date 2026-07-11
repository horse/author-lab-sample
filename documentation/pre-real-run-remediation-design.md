# Pre-Real-Run Remediation Design

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

## Purpose

This design closes the gap between the repository's reference architecture and its first real A→B/C experiment. It repairs the existing contracts directly; it does not create a second generation of directories, scripts, schemas, or state machines.

## Design principles

1. `author-lab-project-manifest.json` remains the control plane.
2. `repository_mode` controls sample markers and initial statuses for every generator.
3. All scaffolders build in a temporary sibling directory, validate the complete result, update control-plane records, and only then atomically move the object into its canonical path.
4. Source evidence, research claims, and source-model provenance are namespaced by `source_author_id`; cross-author references are rejected.
5. Only accepted research claims may support an approved source-model rule.
6. Experiments pin exact source/derived model IDs and versions for every condition and require B and C to be different personas.
7. Writing runs are immutable records under `writing-runs/`; validation reads historical loaded files from the recorded Git commit rather than comparing them with current HEAD.
8. Publication is a recoverable repository transaction with a journal, lock, staging directory, canonical content, manifest, work-item state, and generated persona indexes.
9. CI independently validates publication gates and generated indexes; it does not assume that contributors used the intended commands.
10. Failed, cancelled, rejected, abandoned, and superseded work can be archived without pretending that quality gates passed.

## Repository-mode behavior

A shared `repository_mode_support.py` module supplies:

- `RepositoryModeContext.from_project(repository_root)`;
- marker-aware Markdown and JSON rendering;
- mode-aware initial statuses;
- placeholder-register updates for generated reference-sample files;
- active-mode rejection of unresolved sample sentinel values.

`reference-sample` continues to produce marked instructional scaffolds. `active-author-lab` produces unmarked records with neutral initial statuses such as `draft`, `unreviewed`, `registered`, and `not-run`.

## Object registration

Persona creation resolves an existing source model and version, writes the complete template, and updates both:

- `author-lab-project-manifest.json::derived_author_persona_directories`;
- `repository-component-status-register.json`.

Work items and experiments are discoverable from their canonical root directories, so they do not require parallel manually maintained directory lists.

## Provenance contract

Research claim records gain `source_author_id`. Source-model provenance records gain `source_author_id` and `source_author_model_id`. Validators build a separate segment and claim index for each source author and reject cross-author references. Model provenance statuses become an enum; approved/active model rules may reference only accepted claims.

## Experiment contract

Every condition records:

- condition role and ID;
- persona ID when applicable;
- exact author-model ID and version;
- exact upstream source-model ID and version when applicable.

Condition IDs and roles are unique. Generic baseline has no author model. Source-direct baseline pins one source model. B and C pin distinct persona and derived-model identities.

## Writing-run contract

The legacy single `writing-run-manifest.json` is removed. A work item contains `writing-runs/`, with one immutable `run-*.json` per execution. Each record pins `repository_commit_sha`, loaded path/hash pairs, runtime/runbook/model versions, parameters, permissions, timestamps, outputs, and status.

The validator obtains historical blobs with `git show <sha>:<path>` when a local Git repository is available. It rejects unknown commits, path traversal, duplicate run IDs, mutable output references, or hashes that do not match the recorded commit. A sample not-run record may exist only in reference-sample mode.

## Publication transaction

Publication uses a repository lock and transaction journal. All mutable files are prepared in staging first. The command validates the work item, computes canonical metadata, prepares the new manifest and persona indexes, writes a journal containing backups and intended replacements, and then applies replacements. Recovery either completes or rolls back an interrupted journal on the next invocation.

An empty publication manifest is a valid empty JSONL file. No Sample B sentinel record is generated.

CI runs a read-only publication-integrity validator that independently checks work-item gates, metadata, canonical hashes, manifest equality, state linkage, and generated persona indexes.

## Lifecycle and governance

Lifecycle statuses add `rejected`, `cancelled`, `abandoned`, and `superseded`. Only `approved` and `published` require all gates. `archived` requires an `archive_reason` and may preserve either successful or unsuccessful outcomes.

README and AGENTS list the exact same validation commands as CI. CI also runs Ruff, uses a constraints file for Python dependencies, and pins GitHub Actions to immutable commit SHAs.

## Branch cleanup

After the remediation PR is merged and the exact `main` commit has a successful push workflow, the merged branches are deleted:

- `scaffold/complete-author-lab-architecture`;
- `documentation/complete-repository-file-guide`;
- `upgrade/pre-real-run-complete`;
- the remediation branch itself.

Branch deletion is operational cleanup and does not alter Git history or workflow-run history.

## Completion criteria

The remediation is complete only when:

- all new regression tests first fail on the old behavior and pass on the repaired behavior;
- all repository validation scripts pass;
- all pytest tests pass;
- Ruff passes;
- the PR merge-ref workflow passes;
- the squash/merge commit on `main` receives its own successful push workflow;
- old merged branches are no longer present.
