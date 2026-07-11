# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIRECTORY = REPOSITORY_ROOT / "repository-automation-scripts"
SCRIPT_PATH = SCRIPT_DIRECTORY / "publish_approved_writing_work_item.py"


def load_script_module():
    sys.path.insert(0, str(SCRIPT_DIRECTORY))
    spec = spec_from_file_location("publication_transaction", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_repository(root: Path, *, editorial_approval: str = "approved", include_final: bool = True) -> Path:
    write_json(
        root / "author-lab-project-manifest.json",
        {
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
    work_root = root / "writing-work-items/2026-writing-work-items/2026-001-test-article"
    write_json(
        work_root / "work-item-state.json",
        {
            "work_item_id": "2026-001-test-article",
            "derived_author_id": "derived-b",
            "derived_author_model_id": "derived-b-model",
            "derived_author_model_version": "1.0.0",
            "lifecycle_status": "approved" if editorial_approval == "approved" else "under-review",
            "stage_executions": {
                "factual-review": {"status": "completed"},
                "style-review": {"status": "completed"},
                "editor-review": {
                    "status": "completed" if editorial_approval == "approved" else "in-progress"
                },
                "publication-preparation": {"status": "not-started"},
            },
            "quality_gates": {
                "factual_accuracy": "passed",
                "persona_and_style": "passed",
                "editorial_approval": editorial_approval,
            },
            "publication": None,
        },
    )
    if include_final:
        (work_root / "final-approved-article.md").write_text(
            "# Approved article\n\nReviewed content.\n",
            encoding="utf-8",
        )
    (root / "approved-publications").mkdir(parents=True, exist_ok=True)
    (root / "approved-publications/approved-publication-manifest.jsonl").write_text("", encoding="utf-8")
    return work_root


def test_publication_rejects_pending_editorial_approval_without_mutating_state(tmp_path):
    module = load_script_module()
    work_root = prepare_repository(tmp_path, editorial_approval="pending")
    before = (work_root / "work-item-state.json").read_text(encoding="utf-8")

    try:
        module.publish_approved_work_item(
            repository_root=tmp_path,
            work_item_id="2026-001-test-article",
            publication_id="publication-2026-001-test-article",
            title="Test Article",
            publication_category="researched-essays",
            publication_status="published",
            published_at="2026-07-11T12:00:00+09:00",
        )
    except ValueError as exc:
        assert "editorial_approval=approved" in str(exc)
    else:
        raise AssertionError("Expected pending editorial approval to reject publication")

    assert (work_root / "work-item-state.json").read_text(encoding="utf-8") == before
    assert not (tmp_path / "approved-publications/researched-essays/publication-2026-001-test-article").exists()


def test_publication_rejects_missing_final_file_without_mutating_state(tmp_path):
    module = load_script_module()
    work_root = prepare_repository(tmp_path, include_final=False)
    before = (work_root / "work-item-state.json").read_text(encoding="utf-8")

    try:
        module.publish_approved_work_item(
            repository_root=tmp_path,
            work_item_id="2026-001-test-article",
            publication_id="publication-2026-001-test-article",
            title="Test Article",
            publication_category="researched-essays",
            publication_status="approved",
            published_at=None,
        )
    except ValueError as exc:
        assert "final-approved-article.md" in str(exc)
    else:
        raise AssertionError("Expected missing final file to reject publication")

    assert (work_root / "work-item-state.json").read_text(encoding="utf-8") == before


def test_valid_publication_writes_canonical_files_manifest_and_state(tmp_path):
    module = load_script_module()
    work_root = prepare_repository(tmp_path)

    publication_root = module.publish_approved_work_item(
        repository_root=tmp_path,
        work_item_id="2026-001-test-article",
        publication_id="publication-2026-001-test-article",
        title="Test Article",
        publication_category="researched-essays",
        publication_status="published",
        published_at="2026-07-11T12:00:00+09:00",
    )

    assert (publication_root / "article.md").is_file()
    metadata = json.loads((publication_root / "publication-metadata.json").read_text(encoding="utf-8"))
    assert metadata["work_item_id"] == "2026-001-test-article"
    assert metadata["derived_author_model_id"] == "derived-b-model"
    assert metadata["derived_author_model_version"] == "1.0.0"
    state = json.loads((work_root / "work-item-state.json").read_text(encoding="utf-8"))
    assert state["lifecycle_status"] == "published"
    assert state["publication"]["publication_id"] == "publication-2026-001-test-article"
    assert state["stage_executions"]["publication-preparation"]["status"] == "completed"
    manifest_records = [
        json.loads(line)
        for line in (tmp_path / "approved-publications/approved-publication-manifest.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    assert [record["publication_id"] for record in manifest_records] == [
        "publication-2026-001-test-article"
    ]
