#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    publications_root = repository_root / "approved-publications"
    records: list[dict] = []
    for metadata_path in publications_root.rglob("publication-metadata.json"):
        with metadata_path.open("r", encoding="utf-8") as handle:
            record = json.load(handle)
        if record.get("publication_status") not in {"approved", "published", "withdrawn"}:
            raise SystemExit(f"Invalid publication status in {metadata_path}")
        records.append(record)

    manifest_path = publications_root / "approved-publication-manifest.jsonl"
    if records:
        lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in sorted(records, key=lambda item: item["publication_id"])]
    else:
        lines = [json.dumps({"_sample_comment": SAMPLE_MARKER, "publication_id": "SAMPLE-NOT-PUBLISHED", "publication_status": "withdrawn"}, ensure_ascii=False)]
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {len(lines)} publication manifest record(s) to {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
