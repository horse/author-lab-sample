# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIRECTORY = REPOSITORY_ROOT / "repository-automation-scripts"
SCRIPT_PATH = SCRIPT_DIRECTORY / "validate_publication_integrity.py"


def load_module():
    if str(SCRIPT_DIRECTORY) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIRECTORY))
    spec = spec_from_file_location("publication_integrity", SCRIPT_PATH)
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
        {
            "repository_mode": "active-author-lab",
            "writing_work_items_directory": "writing-work-items",
            "approved_publications_directory": "approved-publications",
            "derived_author_persona_directories": ["derived-author-personas/derived-b"],
        },
    )
    write_json(
        root / "derived-author-personas/derived-b/derived-author-persona-manifest.json",
        {
            "derived_author_id": "derived-b",
            "author_model_directory": "derived-author-model",
            "work_items_directory": "derived-author-writing-work-items",
            "publications_directory": "derived-author-publications",
        },
    )
    write_json(
        root / "derived-author-personas/derived-b/derived-author-model/derived-author-model-manifest.json",
        {
            "derived_author_model_id": "derived-b-model",
            "derived_author_id": "derived-b",
            "model_version": "1.0.0",
        },
    )
    work_root = root / "writing-work-items/2026-writing-work-items/2026-001-test"
    write_json(
        work_root / "work-item-state.json",
        {
            "work_item_id": "2026-001-test",
            "derived_author_id": "derived-b",
            "derived_author_model_id": "derived-b-model",
            "derived_author_model_version": "1.0.0",
            "lifecycle_status": "approved",
            "stage_executions": {
                "factual-review": {"status": "completed"},
                "style-review": {"status": "completed"},
                "editor-review": {"status": "completed"},
                "publication-preparation": {"status": "not-started"},
            },
            "quality_gates": {
                "factual_accuracy": "passed",
                "persona_and_style": "passed",
                "editorial_approval": "approved",
            },
            "publication": None,
        },
    )
    (work_root / "final-approved-article.md").write_text("# Approved\n", encoding="utf-8")
    (root / "approved-publications").mkdir(parents=True, exist_ok=True)
    (root / "approved-publications/approved-publication-manifest.jsonl").write_text("", encoding="utf-8")
    (root / "derived-author-personas/derived-b/derived-author-writing-work-items").mkdir(parents=True, exist_ok=True)
    (root / "derived-author-personas/derived-b/derived-author-publications").mkdir(parents=True, exist_ok=True)
    (root / "derived-author-personas/derived-b/derived-author-writing-work-items/derived-author-work-item-index.jsonl").write_text(
        json.dumps(
            {
                "derived_author_id": "derived-b",
                "canonical_work_item_id": "2026-001-test",
                "lifecycle_status": "approved",
                "canonical_state_file": "writing-work-items/2026-writing-work-items/2026-001-test/work-item-state.json",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (root / "derived-author-personas/derived-b/derived-author-publications/derived-author-publication-index.jsonl").write_text("", encoding="utf-8")


def test_manual_manifest_record_without_canonical_transaction_is_rejected(tmp_path):
    module = load_module()
    prepare_repository(tmp_path)
    fake = {
        "publication_id": "publication-2026-001-fake",
        "work_item_id": "2026-001-test",
        "derived_author_id": "derived-b",
        "derived_author_model_id": "derived-b-model",
        "derived_author_model_version": "1.0.0",
        "title": "Fake",
        "publication_status": "approved",
        "canonical_file": "approved-publications/researched-essays/publication-2026-001-fake/article.md",
        "published_at": None,
    }
    (tmp_path / "approved-publications/approved-publication-manifest.jsonl").write_text(
        json.dumps(fake) + "\n", encoding="utf-8"
    )

    errors = module.validate_publication_integrity(tmp_path)

    assert any("manifest" in error.lower() or "canonical" in error.lower() for error in errors)


def test_stale_persona_publication_index_is_rejected(tmp_path):
    module = load_module()
    prepare_repository(tmp_path)
    index = tmp_path / "derived-author-personas/derived-b/derived-author-publications/derived-author-publication-index.jsonl"
    index.write_text('{"derived_author_id":"derived-b","canonical_publication_id":"stale"}\n', encoding="utf-8")

    errors = module.validate_publication_integrity(tmp_path)

    assert any("persona index" in error.lower() for error in errors)
