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


def test_editor_review_state_accepts_passed_fact_and_style_reviews():
    module = load_script_module()
    document = {
        "status": "editor-review",
        "reviews": {"factual_review": "passed", "style_review": "passed", "editor_review": "pending"},
        "publication": None,
    }
    assert module.validate_state_document(document) == []


def test_published_state_rejects_missing_editor_approval_and_publication_metadata():
    module = load_script_module()
    document = {
        "status": "published",
        "reviews": {"factual_review": "passed", "style_review": "passed", "editor_review": "pending"},
        "publication": None,
    }
    errors = module.validate_state_document(document)
    assert "Approved or later status requires editor_review=approved." in errors
    assert "Published status requires publication metadata." in errors
