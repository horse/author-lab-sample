# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def run_script(script_name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPOSITORY_ROOT / "repository-automation-scripts" / script_name), *arguments],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_project_manifest_declares_pre_real_run_repository_contracts():
    manifest = json.loads((REPOSITORY_ROOT / "author-lab-project-manifest.json").read_text(encoding="utf-8"))
    assert manifest["repository_mode"] == "reference-sample"
    assert manifest["readiness_status"] == "pre-real-run-complete"
    assert manifest["component_status_register"] == "repository-component-status-register.json"
    assert manifest["placeholder_register"] == "repository-placeholder-register.json"
    assert manifest["source_material_storage_register"] == "source-material-storage-and-ingestion-register.jsonl"
    assert manifest["document_schema_registry"] == "shared-writing-harness/machine-readable-contracts/document-schema-registry.json"
    assert manifest["author_model_experiments_directory"] == "author-model-experiments"


def test_machine_readable_contracts_are_validated_against_registered_schemas():
    result = run_script("validate_machine_readable_contracts.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "schema validation passed" in result.stdout.lower()


def test_repository_cross_references_resolve():
    result = run_script("validate_repository_cross_references.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "cross-reference validation passed" in result.stdout.lower()


def test_structure_validation_is_manifest_driven():
    result = run_script("validate_author_lab_repository_structure.py")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "manifest-driven" in result.stdout.lower()


def test_primary_source_manifest_uses_external_storage_uri():
    first_record = json.loads(
        (REPOSITORY_ROOT / "source-authors/source-author-sample/source-corpus/source-corpus-manifest.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()[0]
    )
    assert first_record["storage_uri"].startswith("private-storage://")
    assert "original_file" not in first_record


def test_work_item_state_separates_lifecycle_stages_and_quality_gates():
    state = json.loads(
        (
            REPOSITORY_ROOT
            / "writing-work-items/2026-writing-work-items/2026-001-sample-article/work-item-state.json"
        ).read_text(encoding="utf-8")
    )
    assert state["lifecycle_status"] == "under-review"
    assert state["stage_executions"]["factual-review"]["status"] == "completed"
    assert state["quality_gates"]["factual_accuracy"] == "passed"
    assert "status" not in state
    assert "reviews" not in state


def test_runbook_driven_scaffolder_and_complete_persona_template_exist():
    assert (REPOSITORY_ROOT / "shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json").exists()
    work_script = (REPOSITORY_ROOT / "repository-automation-scripts/create_new_writing_work_item.py").read_text(encoding="utf-8")
    persona_script = (REPOSITORY_ROOT / "repository-automation-scripts/create_new_derived_author_persona.py").read_text(encoding="utf-8")
    assert "required_artifacts" in work_script
    assert "template-manifest.json" in persona_script


def test_experiment_scaffold_requires_external_held_out_uri():
    schema = json.loads(
        (
            REPOSITORY_ROOT
            / "shared-writing-harness/machine-readable-contracts/author-model-experiment-manifest.schema.json"
        ).read_text(encoding="utf-8")
    )
    held_out = schema["properties"]["held_out_evaluation_pack_uri"]
    assert "evaluator-storage" in held_out["pattern"]


def test_ci_runs_schema_and_cross_reference_validation():
    workflow = (REPOSITORY_ROOT / ".github/workflows/validate-author-lab-repository.yml").read_text(encoding="utf-8")
    assert "validate_machine_readable_contracts.py" in workflow
    assert "validate_repository_cross_references.py" in workflow
