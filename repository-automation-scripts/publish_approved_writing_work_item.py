#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any

from publication_gate_support import (
    ALLOWED_PUBLICATION_CATEGORIES,
    collect_publication_records,
    find_work_item,
    load_json,
    serialize_publication_manifest,
    validate_approved_work_item,
    validate_publication_record,
)

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def validate_publication_identifier(value: str) -> str:
    if not re.fullmatch(
        r"publication-\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*",
        value,
    ):
        raise argparse.ArgumentTypeError(
            "Publication ID must use publication-YYYY-NNN-descriptive-slug."
        )
    return value


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def publish_approved_work_item(
    repository_root: Path,
    work_item_id: str,
    publication_id: str,
    title: str,
    publication_category: str,
    publication_status: str,
    published_at: str | None,
) -> Path:
    if publication_category not in ALLOWED_PUBLICATION_CATEGORIES:
        raise ValueError(
            f"Unknown publication category {publication_category!r}; "
            f"allowed categories are {sorted(ALLOWED_PUBLICATION_CATEGORIES)}"
        )
    if publication_status not in {"approved", "published"}:
        raise ValueError(
            "Publication transaction accepts only approved or published status"
        )
    if publication_status == "published" and not published_at:
        raise ValueError("published status requires published_at")

    project = load_json(repository_root / "author-lab-project-manifest.json")
    work_root, state = find_work_item(
        repository_root,
        project["writing_work_items_directory"],
        work_item_id,
    )
    final_file = validate_approved_work_item(
        repository_root,
        project,
        state,
        work_root,
    )

    publications_root = repository_root / project["approved_publications_directory"]
    target_root = publications_root / publication_category / publication_id
    if target_root.exists():
        raise ValueError(f"Publication target already exists: {target_root}")

    canonical_relative = (
        Path(project["approved_publications_directory"])
        / publication_category
        / publication_id
        / "article.md"
    )
    metadata = {
        "_sample_comment": SAMPLE_MARKER,
        "publication_id": publication_id,
        "work_item_id": work_item_id,
        "derived_author_id": state["derived_author_id"],
        "derived_author_model_id": state["derived_author_model_id"],
        "derived_author_model_version": state["derived_author_model_version"],
        "title": title,
        "publication_status": publication_status,
        "canonical_file": canonical_relative.as_posix(),
        "published_at": published_at,
    }
    validate_publication_record(
        repository_root,
        project,
        metadata,
        require_canonical_file=False,
    )

    publications_root.mkdir(parents=True, exist_ok=True)
    manifest_path = publications_root / "approved-publication-manifest.jsonl"
    old_manifest = (
        manifest_path.read_text(encoding="utf-8") if manifest_path.exists() else ""
    )
    state_path = work_root / "work-item-state.json"
    old_state = state_path.read_text(encoding="utf-8")

    staging_parent = publications_root / ".publication-staging"
    staging_parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(
        tempfile.mkdtemp(prefix=f"{publication_id}-", dir=staging_parent)
    )
    staged_publication_root = staging_root / publication_id
    staged_publication_root.mkdir(parents=True)
    shutil.copyfile(final_file, staged_publication_root / "article.md")
    write_json(staged_publication_root / "publication-metadata.json", metadata)

    try:
        target_root.parent.mkdir(parents=True, exist_ok=True)
        os.replace(staged_publication_root, target_root)
        shutil.rmtree(staging_root, ignore_errors=True)

        records = collect_publication_records(
            repository_root,
            project["approved_publications_directory"],
        )
        manifest_temporary = manifest_path.with_suffix(".jsonl.tmp")
        manifest_temporary.write_text(
            serialize_publication_manifest(records),
            encoding="utf-8",
        )
        os.replace(manifest_temporary, manifest_path)

        state["lifecycle_status"] = publication_status
        state["publication"] = {
            "publication_id": publication_id,
            "publication_status": publication_status,
            "canonical_file": canonical_relative.as_posix(),
            "published_at": published_at,
        }
        state.setdefault("stage_executions", {}).setdefault(
            "publication-preparation",
            {"status": "not-started"},
        )["status"] = "completed"
        state_temporary = state_path.with_suffix(".json.tmp")
        write_json(state_temporary, state)
        os.replace(state_temporary, state_path)
    except Exception:
        if target_root.exists():
            shutil.rmtree(target_root)
        manifest_path.write_text(old_manifest, encoding="utf-8")
        state_path.write_text(old_state, encoding="utf-8")
        shutil.rmtree(staging_root, ignore_errors=True)
        raise

    return target_root


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Publish one approved writing work item through an atomic publication gate."
        )
    )
    parser.add_argument("work_item_id")
    parser.add_argument("publication_id", type=validate_publication_identifier)
    parser.add_argument("--title", required=True)
    parser.add_argument("--publication-category", required=True)
    parser.add_argument(
        "--publication-status",
        choices=("approved", "published"),
        default="approved",
    )
    parser.add_argument("--published-at")
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    publication_root = publish_approved_work_item(
        repository_root=repository_root,
        work_item_id=arguments.work_item_id,
        publication_id=arguments.publication_id,
        title=arguments.title,
        publication_category=arguments.publication_category,
        publication_status=arguments.publication_status,
        published_at=arguments.published_at,
    )
    print(f"Published approved writing work item to {publication_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
