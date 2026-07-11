# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIRECTORY = REPOSITORY_ROOT / "repository-automation-scripts"
PUBLISHER_PATH = SCRIPT_DIRECTORY / "publish_approved_writing_work_item.py"
SUPPORT_PATH = SCRIPT_DIRECTORY / "publication_gate_support.py"
SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_module(name: str, path: Path):
    if str(SCRIPT_DIRECTORY) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIRECTORY))
    spec = spec_from_file_location(name, path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_repository(root: Path) -> Path:
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
    (work_root / "final-approved-article.md").write_text("# Final\n", encoding="utf-8")
    (root / "approved-publications").mkdir(parents=True, exist_ok=True)
    (root / "approved-publications/approved-publication-manifest.jsonl").write_text("", encoding="utf-8")
    return work_root


def test_empty_publication_manifest_serializes_as_empty_jsonl():
    support = load_module("publication_support_empty", SUPPORT_PATH)
    assert support.serialize_publication_manifest([]) == ""


def test_staging_copy_failure_is_cleaned_up(tmp_path, monkeypatch):
    publisher = load_module("publication_staging_cleanup", PUBLISHER_PATH)
    work_root = prepare_repository(tmp_path)
    before_state = (work_root / "work-item-state.json").read_text(encoding="utf-8")

    def fail_copy(*args, **kwargs):
        raise OSError("simulated copy failure")

    monkeypatch.setattr(publisher.shutil, "copyfile", fail_copy)
    try:
        publisher.publish_approved_work_item(
            repository_root=tmp_path,
            work_item_id="2026-001-test",
            publication_id="publication-2026-001-test",
            title="Test",
            publication_category="researched-essays",
            publication_status="approved",
            published_at=None,
        )
    except OSError:
        pass
    else:
        raise AssertionError("Expected simulated copy failure")

    staging = tmp_path / "approved-publications/.publication-staging"
    assert not staging.exists() or list(staging.iterdir()) == []
    assert (work_root / "work-item-state.json").read_text(encoding="utf-8") == before_state
    assert (tmp_path / "approved-publications/approved-publication-manifest.jsonl").read_text(encoding="utf-8") == ""


def test_interrupted_transaction_journal_is_recovered_before_new_publish(tmp_path):
    publisher = load_module("publication_journal_recovery", PUBLISHER_PATH)
    work_root = prepare_repository(tmp_path)
    journal = tmp_path / "approved-publications/.publication-transaction.json"
    write_json(
        journal,
        {
            "transaction_id": "interrupted",
            "status": "prepared",
            "target_root": "approved-publications/researched-essays/publication-2026-099-interrupted",
            "staging_root": "approved-publications/.publication-staging/interrupted",
            "backups": {},
        },
    )

    publisher.recover_incomplete_publication_transaction(tmp_path)

    assert not journal.exists()
    assert (work_root / "work-item-state.json").is_file()


def test_active_publication_transaction_emits_no_sample_markers_or_sentinels(tmp_path):
    publisher = load_module("publication_active_mode", PUBLISHER_PATH)
    prepare_repository(tmp_path)

    publication_root = publisher.publish_approved_work_item(
        repository_root=tmp_path,
        work_item_id="2026-001-test",
        publication_id="publication-2026-001-test",
        title="Test",
        publication_category="researched-essays",
        publication_status="published",
        published_at="2026-07-11T12:00:00+09:00",
    )

    checked_paths = [
        publication_root / "publication-metadata.json",
        tmp_path / "approved-publications/approved-publication-manifest.jsonl",
        tmp_path / "derived-author-personas/derived-b/derived-author-writing-work-items/derived-author-work-item-index.jsonl",
        tmp_path / "derived-author-personas/derived-b/derived-author-publications/derived-author-publication-index.jsonl",
    ]
    for path in checked_paths:
        text = path.read_text(encoding="utf-8")
        assert SAMPLE_MARKER not in text
        assert "SAMPLE-NOT-PUBLISHED" not in text
        assert "generated-empty" not in text
