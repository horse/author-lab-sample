# Shared Writing Harness Instructions for Agents

<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->

The shared harness controls how work is executed; it does not define who an author is. Keep contracts deterministic, author-neutral, and independently testable.

## Canonical responsibilities

- `machine-readable-contracts/` defines JSON Schema interfaces and the path-to-schema registry.
- `writing-runbooks/` defines required/optional stages, required artifacts, artifact templates, and policy-rule references.
- `harness-policies/` is the normative source for factuality, derivation, originality, citation, and publication rules.
- `task-prompts/` defines the output of one stage only.
- `artifact-templates/` supplies initial files; templates are not completed runtime records.
- `scaffold-templates/` defines complete multi-file structures such as a derived-author persona.

## Controlled repetition

Rules may be summarized near the point of use, but their meaning comes from canonical policy IDs:

- `POLICY-PROVENANCE-001`
- `POLICY-DERIVATION-001`
- `POLICY-FACTUALITY-001`
- `POLICY-ORIGINALITY-001`
- `POLICY-PUBLICATION-001`
- `POLICY-HELDOUT-001`

AGENTS files state local operational boundaries. Runbooks reference applicable policy IDs. Skills describe loading and execution. Prompts describe the current stage. Rubrics describe measurement. Do not let any of these redefine the policy independently.

## Contract changes

A machine-document change is incomplete unless all affected layers agree:

```text
schema
→ document-schema-registry entry
→ sample/example document
→ semantic/cross-reference validator
→ test
→ documentation
```

New production JSON or JSONL files must receive a schema registration. Files that are genuinely templates or schema definitions need an explicit classification and reason in `excluded_path_patterns`; they must not be silently unvalidated.

Schema changes should reject misspelled or unknown properties where the interface is stable. Keep `additionalProperties: true` only when extension behavior is deliberate and documented.

## Runbook rules

A runbook manifest is the sole source of truth for:

- required stages;
- optional stages;
- required artifacts;
- template path for every required artifact;
- required policy-rule IDs.

The work-item scaffolder and cross-reference validator both read the runbook. Do not add a hard-coded artifact or stage list elsewhere.

## Persona overlay rules

Persona overlays may add loading choices, distinctions, and author-specific constraints. They may not:

- copy the complete shared harness;
- remove a required runbook stage;
- weaken factual, originality, held-out, or publication rules;
- introduce hidden source-author biography or authority;
- make another persona's memory available by default.

## Publication rules

Publication policy cannot be overridden by a persona, prompt, runtime, or runbook. Only the transactional publication command may create canonical approved output. Required rule: `POLICY-PUBLICATION-001`.

## Experiment rules

Runbook and runtime settings used in controlled experiments must remain inspectable and versioned. Real held-out content is evaluator-only under `POLICY-HELDOUT-001`; experiment manifests store an external URI, not the test content.
