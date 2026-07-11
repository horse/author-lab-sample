#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from publication_gate_support import (  # noqa: E402
    collect_publication_records,
    load_json,
    serialize_publication_manifest,
)
from rebuild_derived_author_indexes import (  # noqa: E402
    build_persona_index_documents,
)


def validate_publication_integrity(repository_root: Path) -> list[str]:
    errors: list[str] = []
    project = load_json(repository_root / "author-lab-project-manifest.json")
    publications_root = repository_root / project["approved_publications_directory"]
    journal = publications_root / ".publication-transaction.json"
    lock = publications_root / ".publication-transaction.lock"
    staging = publications_root / ".publication-staging"
    if journal.exists():
        errors.append("Incomplete publication transaction journal exists")
    if lock.exists():
        errors.append("Stale publication transaction lock exists")
    if staging.is_dir() and any(staging.iterdir()):
        errors.append("Publication staging directory contains uncommitted data")

    try:
        records = collect_publication_records(
            repository_root, project["approved_publications_directory"]
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"Publication record validation failed: {exc}"]

    manifest_path = publications_root / "approved-publication-manifest.jsonl"
    actual_manifest = (
        manifest_path.read_text(encoding="utf-8") if manifest_path.is_file() else None
    )
    expected_manifest = serialize_publication_manifest(records)
    if actual_manifest is None:
        errors.append("Approved publication manifest is missing")
    elif actual_manifest != expected_manifest:
        errors.append(
            "Approved publication manifest does not exactly match canonical metadata"
        )

    expected_indexes = build_persona_index_documents(
        repository_root, project, publication_records=records
    )
    for path, expected in expected_indexes.items():
        actual = path.read_text(encoding="utf-8") if path.is_file() else None
        if actual != expected:
            errors.append(
                f"Generated persona index does not match canonical records: "
                f"{path.relative_to(repository_root)}"
            )
    return errors


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    errors = validate_publication_integrity(repository_root)
    if errors:
        print("Publication integrity validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Publication integrity validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
