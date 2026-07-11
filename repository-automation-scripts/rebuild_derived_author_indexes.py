#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from atomic_repository_update import atomic_replace_text_files  # noqa: E402
from repository_mode_support import (  # noqa: E402
    RepositoryModeContext,
    dump_json,
    load_json,
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def serialize_jsonl(records: list[dict[str, Any]]) -> str:
    return "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        for record in records
    )


def canonical_work_item_records(
    repository_root: Path,
    project: dict[str, Any],
) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    root = repository_root / project["writing_work_items_directory"]
    for state_path in sorted(root.glob("**/work-item-state.json")):
        records.append((state_path, load_json(state_path)))
    return records


def canonical_publication_records(
    repository_root: Path,
    project: dict[str, Any],
) -> list[dict[str, Any]]:
    manifest = (
        repository_root
        / project["approved_publications_directory"]
        / "approved-publication-manifest.jsonl"
    )
    return load_jsonl(manifest)


def build_persona_index_documents(
    repository_root: Path,
    project: dict[str, Any],
    *,
    publication_records: list[dict[str, Any]] | None = None,
    work_item_states: list[tuple[Path, dict[str, Any]]] | None = None,
) -> dict[Path, str]:
    context = RepositoryModeContext(repository_root, project)
    publications = (
        publication_records
        if publication_records is not None
        else canonical_publication_records(repository_root, project)
    )
    work_items = (
        work_item_states
        if work_item_states is not None
        else canonical_work_item_records(repository_root, project)
    )
    updates: dict[Path, str] = {}

    for persona_directory in project["derived_author_persona_directories"]:
        persona_root = repository_root / persona_directory
        persona_manifest = load_json(
            persona_root / "derived-author-persona-manifest.json"
        )
        persona_id = persona_manifest["derived_author_id"]

        work_records: list[dict[str, Any]] = []
        for state_path, state in work_items:
            if state.get("derived_author_id") != persona_id:
                continue
            work_records.append(
                context.with_json_marker(
                    {
                        "derived_author_id": persona_id,
                        "canonical_work_item_id": state["work_item_id"],
                        "lifecycle_status": state["lifecycle_status"],
                        "canonical_state_file": state_path.relative_to(
                            repository_root
                        ).as_posix(),
                    }
                )
            )
        if not work_records and context.is_reference_sample:
            work_records = [
                context.with_json_marker(
                    {
                        "derived_author_id": persona_id,
                        "index_status": "generated-empty",
                        "canonical_work_item_id": None,
                    }
                )
            ]

        persona_publications: list[dict[str, Any]] = []
        for publication in publications:
            if publication.get("derived_author_id") != persona_id:
                continue
            persona_publications.append(
                context.with_json_marker(
                    {
                        "derived_author_id": persona_id,
                        "canonical_publication_id": publication["publication_id"],
                        "work_item_id": publication["work_item_id"],
                        "publication_status": publication["publication_status"],
                        "canonical_file": publication["canonical_file"],
                    }
                )
            )
        if not persona_publications and context.is_reference_sample:
            persona_publications = [
                context.with_json_marker(
                    {
                        "derived_author_id": persona_id,
                        "index_status": "generated-empty",
                        "canonical_publication_id": None,
                    }
                )
            ]

        work_path = (
            persona_root
            / persona_manifest["work_items_directory"]
            / "derived-author-work-item-index.jsonl"
        )
        publication_path = (
            persona_root
            / persona_manifest["publications_directory"]
            / "derived-author-publication-index.jsonl"
        )
        updates[work_path] = serialize_jsonl(
            sorted(
                work_records,
                key=lambda record: record.get("canonical_work_item_id") or "",
            )
        )
        updates[publication_path] = serialize_jsonl(
            sorted(
                persona_publications,
                key=lambda record: record.get("canonical_publication_id") or "",
            )
        )
    return updates


def rebuild_indexes(repository_root: Path) -> None:
    project = load_json(repository_root / "author-lab-project-manifest.json")
    atomic_replace_text_files(build_persona_index_documents(repository_root, project))


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    rebuild_indexes(repository_root)
    print("Rebuilt derived-author work-item and publication indexes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
