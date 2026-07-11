# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts/validate_writing_work_item_state.py"


def load_module():
    spec = spec_from_file_location("extended_lifecycle", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def base_document() -> dict:
    return {
        "lifecycle_status": "in-progress",
        "stage_executions": {
            "factual-review": {"status": "not-started"},
            "style-review": {"status": "not-started"},
            "editor-review": {"status": "not-started"},
        },
        "quality_gates": {
            "factual_accuracy": "not-evaluated",
            "persona_and_style": "not-evaluated",
            "editorial_approval": "not-evaluated",
        },
        "publication": None,
        "archive_reason": None,
    }


def test_rejected_cancelled_abandoned_and_superseded_do_not_require_passed_gates():
    module = load_module()

    for status in ("rejected", "cancelled", "abandoned", "superseded"):
        document = base_document()
        document["lifecycle_status"] = status
        assert module.validate_state_document(document) == []


def test_archived_requires_reason_but_not_successful_gates():
    module = load_module()
    document = base_document()
    document["lifecycle_status"] = "archived"
    document["archive_reason"] = "Cancelled after source-rights review."

    assert module.validate_state_document(document) == []

    document["archive_reason"] = None
    errors = module.validate_state_document(document)
    assert any("archive_reason" in error for error in errors)


def test_approved_publication_linkage_requires_typed_metadata():
    module = load_module()
    document = base_document()
    document["lifecycle_status"] = "approved"
    document["stage_executions"] = {
        "factual-review": {"status": "completed"},
        "style-review": {"status": "completed"},
        "editor-review": {"status": "completed"},
    }
    document["quality_gates"] = {
        "factual_accuracy": "passed",
        "persona_and_style": "passed",
        "editorial_approval": "approved",
    }
    document["publication"] = {"publication_id": "incomplete"}

    errors = module.validate_state_document(document)

    assert any("publication metadata" in error for error in errors)
