#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import os
from pathlib import Path

from publication_gate_support import (
    collect_publication_records,
    load_json,
    serialize_publication_manifest,
)


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    project = load_json(repository_root / "author-lab-project-manifest.json")
    publications_directory = project["approved_publications_directory"]
    publications_root = repository_root / publications_directory
    records = collect_publication_records(repository_root, publications_directory)

    manifest_path = publications_root / "approved-publication-manifest.jsonl"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = manifest_path.with_suffix(".jsonl.tmp")
    temporary_path.write_text(
        serialize_publication_manifest(records),
        encoding="utf-8",
    )
    os.replace(temporary_path, manifest_path)
    print(
        f"Validated and wrote {max(len(records), 1)} publication manifest record(s) "
        f"to {manifest_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
