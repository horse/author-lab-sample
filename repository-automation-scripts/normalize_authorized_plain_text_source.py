#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
from pathlib import Path

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def normalize_text(text: str, source_id: str) -> str:
    normalized_lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    paragraphs = [line.strip() for line in normalized_lines if line.strip()]
    output = [f"<!-- {SAMPLE_MARKER} -->", f"# Normalized Source: {source_id}", ""]
    for index, paragraph in enumerate(paragraphs, start=1):
        output.extend((f"<a id=\"{source_id}-paragraph-{index:05d}\"></a>", paragraph, ""))
    return "\n".join(output).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize an authorized plain-text source with stable paragraph IDs.")
    parser.add_argument("source_id")
    parser.add_argument("input_path", type=Path)
    parser.add_argument("output_path", type=Path)
    arguments = parser.parse_args()

    text = arguments.input_path.read_text(encoding="utf-8")
    arguments.output_path.parent.mkdir(parents=True, exist_ok=True)
    arguments.output_path.write_text(normalize_text(text, arguments.source_id), encoding="utf-8")
    print(f"Normalized source written to {arguments.output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
