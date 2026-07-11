# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_writing_work_item_state.py"


def load_script_module():
    spec = spec_from_file_location("state_validator", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_under_review_accepts_completed_fact_and_style_stages_with_passed_gates():
    module = load_script_module()
    document = {
        "lifecycle_status": "under-review",
        "stage_executions": {
            "factual-review": {"status": "completed"},
            "style-review": {"status": "completed"},
            "editor-review": {"status": "in-progress"},
        },
        "quality_gates": {
            "factual_accuracy": "passed",
            "persona_and_style": "passed",
            "editorial_approval": "pending",
        },
        "publication": None,
    }
    assert module.validate_state_document(document) == []


def test_published_rejects_missing_editor_approval_and_publication_metadata():
    module = load_script_module()
    document = {
        "lifecycle_status": "published",
        "stage_executions": {
            "factual-review": {"status": "completed"},
            "style-review": {"status": "completed"},
            "editor-review": {"status": "in-progress"},
        },
        "quality_gates": {
            "factual_accuracy": "passed",
            "persona_and_style": "passed",
            "editorial_approval": "pending",
        },
        "publication": None,
    }
    errors = module.validate_state_document(document)
    assert "published requires editorial_approval=approved." in errors
    assert "published lifecycle_status requires publication metadata." in errors


def test_passed_gate_requires_corresponding_stage_completion():
    module = load_script_module()
    document = {
        "lifecycle_status": "in-progress",
        "stage_executions": {
            "factual-review": {"status": "in-progress"},
            "style-review": {"status": "not-started"},
        },
        "quality_gates": {
            "factual_accuracy": "passed",
            "persona_and_style": "not-evaluated",
            "editorial_approval": "not-evaluated",
        },
        "publication": None,
    }
    assert "factual_accuracy=passed requires factual-review stage status=completed." in module.validate_state_document(document)
