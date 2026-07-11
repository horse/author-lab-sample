#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

from pathlib import Path
import sys

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from atomic_repository_update import atomic_replace_text_files  # noqa: E402
from publication_gate_support import (  # noqa: E402
    collect_publication_records,
    load_json,
    serialize_publication_manifest,
)
from rebuild_derived_author_indexes import (  # noqa: E402
    build_persona_index_documents,
)


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    project = load_json(repository_root / "author-lab-project-manifest.json")
    publications_directory = project["approved_publications_directory"]
    publications_root = repository_root / publications_directory
    records = collect_publication_records(repository_root, publications_directory)

    manifest_path = publications_root / "approved-publication-manifest.jsonl"
    updates = {
        manifest_path: serialize_publication_manifest(records),
        **build_persona_index_documents(
            repository_root, project, publication_records=records
        ),
    }
    atomic_replace_text_files(updates)
    print(
        f"Validated and wrote {len(records)} publication manifest record(s) "
        f"to {manifest_path}; rebuilt persona publication indexes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
