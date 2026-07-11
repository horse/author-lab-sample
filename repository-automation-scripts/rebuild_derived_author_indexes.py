#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            for record in records
        ),
        encoding="utf-8",
    )


def rebuild_indexes(repository_root: Path) -> None:
    project = load_json(repository_root / "author-lab-project-manifest.json")
    work_items_root = repository_root / project["writing_work_items_directory"]
    publications_root = repository_root / project["approved_publications_directory"]
    publication_records = load_jsonl(
        publications_root / "approved-publication-manifest.jsonl"
    )

    work_item_states: list[tuple[Path, dict[str, Any]]] = []
    for state_path in work_items_root.glob("**/work-item-state.json"):
        work_item_states.append((state_path, load_json(state_path)))

    for persona_directory in project["derived_author_persona_directories"]:
        persona_root = repository_root / persona_directory
        persona_manifest = load_json(
            persona_root / "derived-author-persona-manifest.json"
        )
        persona_id = persona_manifest["derived_author_id"]

        work_records: list[dict[str, Any]] = []
        for state_path, state in work_item_states:
            if state.get("derived_author_id") != persona_id:
                continue
            work_records.append(
                {
                    "_sample_comment": SAMPLE_MARKER,
                    "derived_author_id": persona_id,
                    "canonical_work_item_id": state["work_item_id"],
                    "lifecycle_status": state.get("lifecycle_status"),
                    "canonical_state_file": state_path.relative_to(repository_root).as_posix(),
                }
            )
        if not work_records:
            work_records = [
                {
                    "_sample_comment": SAMPLE_MARKER,
                    "derived_author_id": persona_id,
                    "index_status": "generated-empty",
                    "canonical_work_item_id": None,
                }
            ]
        write_jsonl(
            persona_root
            / persona_manifest["work_items_directory"]
            / "derived-author-work-item-index.jsonl",
            sorted(
                work_records,
                key=lambda record: record.get("canonical_work_item_id") or "",
            ),
        )

        persona_publications: list[dict[str, Any]] = []
        for publication in publication_records:
            if publication.get("derived_author_id") != persona_id:
                continue
            persona_publications.append(
                {
                    "_sample_comment": SAMPLE_MARKER,
                    "derived_author_id": persona_id,
                    "canonical_publication_id": publication["publication_id"],
                    "work_item_id": publication.get("work_item_id"),
                    "publication_status": publication.get("publication_status"),
                    "canonical_file": publication.get("canonical_file"),
                }
            )
        if not persona_publications:
            persona_publications = [
                {
                    "_sample_comment": SAMPLE_MARKER,
                    "derived_author_id": persona_id,
                    "index_status": "generated-empty",
                    "canonical_publication_id": None,
                }
            ]
        write_jsonl(
            persona_root
            / persona_manifest["publications_directory"]
            / "derived-author-publication-index.jsonl",
            sorted(
                persona_publications,
                key=lambda record: record.get("canonical_publication_id") or "",
            ),
        )


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    rebuild_indexes(repository_root)
    print("Rebuilt derived-author work-item and publication indexes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
