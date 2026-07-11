#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def normalize_text(
    text: str,
    source_id: str,
    edition_id: str,
    segmentation_version: str,
) -> tuple[str, list[dict[str, Any]]]:
    normalized_lines = [
        line.rstrip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ]
    paragraphs = [line.strip() for line in normalized_lines if line.strip()]
    output = [
        f"<!-- {SAMPLE_MARKER} -->",
        f"# Normalized Source: {source_id}",
        "",
        f"Edition: `{edition_id}`",
        f"Segmentation version: `{segmentation_version}`",
        "",
    ]
    location_records: list[dict[str, Any]] = []

    for index, paragraph in enumerate(paragraphs, start=1):
        content_sha256 = hashlib.sha256(paragraph.encode("utf-8")).hexdigest()
        segment_id = (
            f"{source_id}.{edition_id}.{segmentation_version}."
            f"segment-{index:05d}-{content_sha256[:12]}"
        )
        output.extend((f'<a id="{segment_id}"></a>', paragraph, ""))
        location_records.append(
            {
                "_sample_comment": SAMPLE_MARKER,
                "source_id": source_id,
                "edition_id": edition_id,
                "segmentation_version": segmentation_version,
                "segment_id": segment_id,
                "segment_ordinal": index,
                "content_sha256": content_sha256,
                "character_count": len(paragraph),
            }
        )

    return "\n".join(output).rstrip() + "\n", location_records


def write_location_map(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Normalize an authorized plain-text source using versioned segment anchors."
    )
    parser.add_argument("source_id")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument("location_map_path", type=Path)
    parser.add_argument("--edition-id", required=True)
    parser.add_argument("--segmentation-version", required=True)
    arguments = parser.parse_args()

    text = arguments.input_path.read_text(encoding="utf-8")
    normalized_text, location_records = normalize_text(
        text,
        source_id=arguments.source_id,
        edition_id=arguments.edition_id,
        segmentation_version=arguments.segmentation_version,
    )
    arguments.output_path.parent.mkdir(parents=True, exist_ok=True)
    arguments.output_path.write_text(normalized_text, encoding="utf-8")
    write_location_map(arguments.location_map_path, location_records)
    print(
        "Normalized source and location map written to "
        f"{arguments.output_path} and {arguments.location_map_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
