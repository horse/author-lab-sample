# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "create_new_writing_work_item.py"
SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_script_module():
    spec = spec_from_file_location("work_item_scaffolder", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_repository(root: Path) -> None:
    write_json(
        root / "author-lab-project-manifest.json",
        {"writing_work_items_directory": "writing-work-items"},
    )
    write_json(
        root / "derived-author-personas/derived-b/derived-author-persona-manifest.json",
        {
            "derived_author_id": "derived-b",
            "author_model_directory": "derived-author-model",
        },
    )
    write_json(
        root / "derived-author-personas/derived-b/derived-author-model/derived-author-model-manifest.json",
        {
            "derived_author_model_id": "derived-b-model",
            "derived_author_id": "derived-b",
            "model_version": "1.2.3",
        },
    )
    write_json(
        root / "runtime-adapters/test-runtime/runtime-adapter-configuration.json",
        {
            "runtime_adapter_id": "test-runtime",
            "configuration_version": "2.0.0",
        },
    )
    template_path = root / "shared-writing-harness/artifact-templates/custom-template.md"
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(
        "# Custom Artifact\n\n<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->\n\n{{work_item_id}} / {{derived_author_id}}\n",
        encoding="utf-8",
    )
    write_json(
        root / "shared-writing-harness/writing-runbooks/custom-runbook/writing-runbook-manifest.json",
        {
            "runbook_id": "custom-runbook",
            "runbook_version": "3.0.0",
            "required_stages": ["intake", "custom-stage"],
            "optional_stages": ["optional-stage"],
            "required_artifacts": ["custom-artifact.md"],
            "artifact_templates": {
                "custom-artifact.md": "shared-writing-harness/artifact-templates/custom-template.md"
            },
            "required_policy_rule_ids": ["POLICY-FACTUALITY-001"],
        },
    )


def test_scaffolder_reads_artifacts_stages_and_versions_from_selected_contracts(tmp_path):
    module = load_script_module()
    prepare_repository(tmp_path)

    work_root = module.create_work_item(
        repository_root=tmp_path,
        work_item_id="2026-001-custom-article",
        derived_author_id="derived-b",
        runbook_id="custom-runbook",
        runtime_adapter_id="test-runtime",
    )

    assert (work_root / "custom-artifact.md").read_text(encoding="utf-8").endswith(
        "2026-001-custom-article / derived-b\n"
    )
    assert not (work_root / "writing-brief.md").exists()
    state = json.loads((work_root / "work-item-state.json").read_text(encoding="utf-8"))
    assert state["derived_author_model_id"] == "derived-b-model"
    assert state["derived_author_model_version"] == "1.2.3"
    assert state["runbook_version"] == "3.0.0"
    assert state["runtime_adapter_version"] == "2.0.0"
    assert state["stage_executions"] == {
        "intake": {"status": "in-progress"},
        "custom-stage": {"status": "not-started"},
        "optional-stage": {"status": "not-started"},
    }


def test_scaffolder_rejects_required_artifact_without_template(tmp_path):
    module = load_script_module()
    prepare_repository(tmp_path)
    runbook_path = tmp_path / "shared-writing-harness/writing-runbooks/custom-runbook/writing-runbook-manifest.json"
    runbook = json.loads(runbook_path.read_text(encoding="utf-8"))
    runbook["required_artifacts"].append("missing-template.md")
    write_json(runbook_path, runbook)

    try:
        module.create_work_item(
            repository_root=tmp_path,
            work_item_id="2026-002-invalid-runbook",
            derived_author_id="derived-b",
            runbook_id="custom-runbook",
            runtime_adapter_id="test-runtime",
        )
    except SystemExit as exc:
        assert "missing-template.md" in str(exc)
    else:
        raise AssertionError("Expected missing artifact template to reject scaffolding")
