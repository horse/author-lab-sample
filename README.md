# Author Lab Sample

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

`author-lab-sample` is a reference repository for researching one source author, compiling a source-author model, deriving multiple pseudonymous authors, running writing harnesses across runtimes, evaluating outputs, and publishing approved work.

## Repository model

```text
source materials → source-author research → source-author model
                                           → derived author B
                                           → derived author C

derived author + runbook + runtime + work item → reviews → approved publication
```

Generated writing never becomes evidence about the source author. Source-author evidence, research conclusions, compiled models, derived-author models, work records, and publications are kept in separate directories.

## Primary directories

- `source-authors/` — original and secondary materials for real source authors.
- `source-author-research/` — evidence-backed research about source authors.
- `source-author-models/` — compact, versioned models compiled from research.
- `derived-author-personas/` — independently maintained pseudonymous authors derived from one or more source models.
- `shared-writing-harness/` — contracts, prompts, runbooks, policies, and templates shared by all derived authors.
- `agent-skills/` — thin task skills that load the correct model and harness assets.
- `runtime-adapters/` — runtime-specific configuration without author knowledge.
- `writing-work-items/` — self-contained writing packages and state records.
- `author-model-evaluations/` — fidelity, identity, leakage, originality, and distinction evaluations.
- `approved-publications/` — editorially approved outputs only.
- `repository-automation-scripts/` and `repository-validation-tests/` — validation and scaffolding tools.

## Validation

```bash
python -m pip install -e '.[development]'
python repository-automation-scripts/validate_author_lab_repository_structure.py
python repository-automation-scripts/validate_json_and_jsonl_documents.py
python repository-automation-scripts/validate_sample_comment_markers.py
pytest repository-validation-tests
```

Read `AGENTS.md` before any agent modifies this repository.