#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"
ALLOWED_PUBLICATION_CATEGORIES = {
    "researched-essays",
    "short-public-commentaries",
    "authorized-life-writing",
    "book-length-projects",
    "editorial-collections",
}
ALLOWED_PUBLICATION_STATUSES = {"approved", "published", "withdrawn"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.is_file():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def find_work_item(
    repository_root: Path,
    work_items_directory: str,
    work_item_id: str,
) -> tuple[Path, dict[str, Any]]:
    matches = list(
        (repository_root / work_items_directory).glob(
            f"**/{work_item_id}/work-item-state.json"
        )
    )
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one work item {work_item_id!r}, found {len(matches)}"
        )
    state_path = matches[0]
    return state_path.parent, load_json(state_path)


def validate_approved_work_item(
    repository_root: Path,
    project: dict[str, Any],
    state: dict[str, Any],
    work_root: Path,
) -> Path:
    gates = state.get("quality_gates", {})
    if gates.get("factual_accuracy") != "passed":
        raise ValueError("Publication requires factual_accuracy=passed")
    if gates.get("persona_and_style") != "passed":
        raise ValueError("Publication requires persona_and_style=passed")
    if gates.get("editorial_approval") != "approved":
        raise ValueError("Publication requires editorial_approval=approved")
    if state.get("lifecycle_status") not in {"approved", "published"}:
        raise ValueError("Publication requires lifecycle_status=approved or published")

    stages = state.get("stage_executions", {})
    for stage in ("factual-review", "style-review", "editor-review"):
        if stages.get(stage, {}).get("status") != "completed":
            raise ValueError(f"Publication requires {stage} stage status=completed")

    final_file = work_root / "final-approved-article.md"
    if not final_file.is_file() or not final_file.read_text(encoding="utf-8").strip():
        raise ValueError(
            f"Missing or empty final-approved-article.md for {state['work_item_id']}"
        )

    persona_id = state["derived_author_id"]
    persona_directories = project.get("derived_author_persona_directories", [])
    persona_roots: list[Path] = []
    for directory in persona_directories:
        manifest_path = (
            repository_root / directory / "derived-author-persona-manifest.json"
        )
        if manifest_path.is_file() and load_json(manifest_path).get(
            "derived_author_id"
        ) == persona_id:
            persona_roots.append(manifest_path.parent)
    if len(persona_roots) != 1:
        raise ValueError(f"Could not resolve exactly one persona for {persona_id}")

    persona_manifest = load_json(
        persona_roots[0] / "derived-author-persona-manifest.json"
    )
    model_manifest = load_json(
        persona_roots[0]
        / persona_manifest["author_model_directory"]
        / "derived-author-model-manifest.json"
    )
    if model_manifest["derived_author_model_id"] != state[
        "derived_author_model_id"
    ]:
        raise ValueError("Work-item model ID does not match the persona model")
    if model_manifest["model_version"] != state["derived_author_model_version"]:
        raise ValueError("Work-item model version does not match the persona model")
    return final_file


def validate_publication_record(
    repository_root: Path,
    project: dict[str, Any],
    record: dict[str, Any],
    *,
    require_canonical_file: bool = True,
) -> None:
    required = {
        "publication_id",
        "work_item_id",
        "derived_author_id",
        "derived_author_model_id",
        "derived_author_model_version",
        "title",
        "publication_status",
        "canonical_file",
        "published_at",
    }
    missing = sorted(required - set(record))
    if missing:
        raise ValueError(
            f"Publication {record.get('publication_id', '<unknown>')} missing fields: {missing}"
        )
    if record["publication_status"] not in ALLOWED_PUBLICATION_STATUSES:
        raise ValueError(
            f"Invalid publication status for {record['publication_id']}: "
            f"{record['publication_status']}"
        )
    if record["publication_status"] == "published" and not record["published_at"]:
        raise ValueError(
            f"Published record {record['publication_id']} requires published_at"
        )

    work_root, state = find_work_item(
        repository_root,
        project["writing_work_items_directory"],
        record["work_item_id"],
    )
    if record["publication_status"] in {"approved", "published"}:
        validate_approved_work_item(repository_root, project, state, work_root)
    if state["derived_author_id"] != record["derived_author_id"]:
        raise ValueError(
            f"Publication {record['publication_id']} has the wrong derived author"
        )
    if state["derived_author_model_id"] != record["derived_author_model_id"]:
        raise ValueError(f"Publication {record['publication_id']} has the wrong model ID")
    if state["derived_author_model_version"] != record[
        "derived_author_model_version"
    ]:
        raise ValueError(
            f"Publication {record['publication_id']} has the wrong model version"
        )

    if require_canonical_file and record["publication_status"] in {
        "approved",
        "published",
    }:
        canonical_path = repository_root / record["canonical_file"]
        if not canonical_path.is_file():
            raise ValueError(
                f"Publication {record['publication_id']} canonical file does not exist: "
                f"{record['canonical_file']}"
            )


def collect_publication_records(
    repository_root: Path,
    publications_directory: str,
) -> list[dict[str, Any]]:
    project = load_json(repository_root / "author-lab-project-manifest.json")
    publication_root = repository_root / publications_directory
    records: list[dict[str, Any]] = []
    publication_ids: set[str] = set()
    for metadata_path in publication_root.glob("**/publication-metadata.json"):
        record = load_json(metadata_path)
        validate_publication_record(repository_root, project, record)
        publication_id = record["publication_id"]
        if publication_id in publication_ids:
            raise ValueError(f"Duplicate publication_id: {publication_id}")
        publication_ids.add(publication_id)
        records.append(record)
    return sorted(records, key=lambda item: item["publication_id"])


def serialize_publication_manifest(records: list[dict[str, Any]]) -> str:
    if not records:
        return json.dumps(
            {
                "_sample_comment": SAMPLE_MARKER,
                "publication_id": "SAMPLE-NOT-PUBLISHED",
                "work_item_id": "2026-001-sample-article",
                "derived_author_id": "derived-author-sample-b",
                "derived_author_model_id": "derived-author-sample-b-model",
                "derived_author_model_version": "0.1.0",
                "title": "Sample Not Published",
                "publication_status": "withdrawn",
                "canonical_file": "",
                "published_at": None,
            },
            ensure_ascii=False,
            sort_keys=True,
        ) + "\n"
    return "".join(
        json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        for record in records
    )
