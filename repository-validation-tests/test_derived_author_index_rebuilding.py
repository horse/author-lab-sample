# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "rebuild_derived_author_indexes.py"


def load_script_module():
    spec = spec_from_file_location("persona_index_builder", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_rebuild_indexes_uses_canonical_work_items_and_publications(tmp_path):
    module = load_script_module()
    write_json(
        tmp_path / "author-lab-project-manifest.json",
        {
            "derived_author_persona_directories": ["derived-author-personas/derived-b"],
            "writing_work_items_directory": "writing-work-items",
            "approved_publications_directory": "approved-publications",
        },
    )
    write_json(
        tmp_path / "derived-author-personas/derived-b/derived-author-persona-manifest.json",
        {
            "derived_author_id": "derived-b",
            "work_items_directory": "derived-author-writing-work-items",
            "publications_directory": "derived-author-publications",
        },
    )
    write_json(
        tmp_path / "writing-work-items/2026-writing-work-items/2026-001-test/work-item-state.json",
        {
            "work_item_id": "2026-001-test",
            "derived_author_id": "derived-b",
            "lifecycle_status": "published",
        },
    )
    publication_manifest = tmp_path / "approved-publications/approved-publication-manifest.jsonl"
    publication_manifest.parent.mkdir(parents=True, exist_ok=True)
    publication_manifest.write_text(
        json.dumps(
            {
                "publication_id": "publication-2026-001-test",
                "work_item_id": "2026-001-test",
                "derived_author_id": "derived-b",
                "publication_status": "published",
                "canonical_file": "approved-publications/researched-essays/publication-2026-001-test/article.md",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    module.rebuild_indexes(tmp_path)

    work_records = [
        json.loads(line)
        for line in (
            tmp_path
            / "derived-author-personas/derived-b/derived-author-writing-work-items/derived-author-work-item-index.jsonl"
        )
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    publication_records = [
        json.loads(line)
        for line in (
            tmp_path
            / "derived-author-personas/derived-b/derived-author-publications/derived-author-publication-index.jsonl"
        )
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    assert work_records[0]["canonical_work_item_id"] == "2026-001-test"
    assert work_records[0]["lifecycle_status"] == "published"
    assert publication_records[0]["canonical_publication_id"] == "publication-2026-001-test"
    assert publication_records[0]["publication_status"] == "published"
