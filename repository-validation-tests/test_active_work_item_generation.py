# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts/create_new_writing_work_item.py"
SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_module():
    spec = spec_from_file_location("active_work_item", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_active_work_item_contains_no_sample_records(tmp_path):
    module = load_module()
    write_json(
        tmp_path / "author-lab-project-manifest.json",
        {
            "repository_mode": "active-author-lab",
            "writing_work_items_directory": "writing-work-items",
            "derived_author_persona_directories": ["derived-author-personas/derived-b"],
        },
    )
    write_json(
        tmp_path / "derived-author-personas/derived-b/derived-author-persona-manifest.json",
        {"derived_author_id": "derived-b", "author_model_directory": "derived-author-model"},
    )
    write_json(
        tmp_path / "derived-author-personas/derived-b/derived-author-model/derived-author-model-manifest.json",
        {
            "derived_author_model_id": "derived-b-model",
            "derived_author_id": "derived-b",
            "model_version": "1.0.0",
        },
    )
    write_json(
        tmp_path / "runtime-adapters/runtime/runtime-adapter-configuration.json",
        {"runtime_adapter_id": "runtime", "configuration_version": "1.0.0"},
    )
    template = tmp_path / "shared-writing-harness/artifact-templates/brief.md"
    template.parent.mkdir(parents=True, exist_ok=True)
    template.write_text(
        "# Brief\n\n<!-- 这是一个 sample，文件实质完成后删掉这行注释 -->\n\n{{work_item_id}}\n",
        encoding="utf-8",
    )
    write_json(
        tmp_path / "shared-writing-harness/writing-runbooks/runbook/writing-runbook-manifest.json",
        {
            "runbook_id": "runbook",
            "runbook_version": "1.0.0",
            "required_stages": ["intake"],
            "optional_stages": [],
            "required_artifacts": ["brief.md"],
            "artifact_templates": {
                "brief.md": "shared-writing-harness/artifact-templates/brief.md"
            },
            "required_policy_rule_ids": [],
        },
    )

    work_root = module.create_work_item(
        repository_root=tmp_path,
        work_item_id="2026-001-active-work",
        derived_author_id="derived-b",
        runbook_id="runbook",
        runtime_adapter_id="runtime",
    )

    for path in work_root.rglob("*"):
        if path.is_file():
            assert SAMPLE_MARKER not in path.read_text(encoding="utf-8")
    assert list((work_root / "writing-runs").glob("run-*.json")) == []
    state = json.loads((work_root / "work-item-state.json").read_text(encoding="utf-8"))
    assert "_sample_comment" not in state
    assert state["archive_reason"] is None
