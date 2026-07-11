#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"
SKIPPED_DIRECTORIES = {".git", ".venv", "venv", "generated-site-output"}
BINARY_SUFFIXES = {".epub", ".pdf", ".jpg", ".jpeg", ".png", ".webp", ".mp3", ".mp4"}


def file_has_marker(path: Path) -> bool:
    if path.suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle).get("_sample_comment") == SAMPLE_MARKER
    if path.suffix == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            first_record = next((line for line in handle if line.strip()), "")
        return bool(first_record) and json.loads(first_record).get("_sample_comment") == SAMPLE_MARKER
    return SAMPLE_MARKER in path.read_text(encoding="utf-8")


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    missing: list[str] = []
    checked = 0
    for path in repository_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in BINARY_SUFFIXES:
            continue
        if any(part in SKIPPED_DIRECTORIES for part in path.parts):
            continue
        checked += 1
        try:
            if not file_has_marker(path):
                missing.append(str(path.relative_to(repository_root)))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, StopIteration):
            missing.append(str(path.relative_to(repository_root)))
    if missing:
        print("Files missing the required sample marker:")
        for path in missing:
            print(f"- {path}")
        return 1
    print(f"Sample marker validation passed: {checked} files checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
