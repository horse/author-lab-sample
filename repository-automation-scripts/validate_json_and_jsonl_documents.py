#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys

SKIPPED_DIRECTORIES = {".git", ".venv", "venv", "generated-site-output"}


def iter_machine_documents(repository_root: Path):
    for path in repository_root.rglob("*"):
        if any(part in SKIPPED_DIRECTORIES for part in path.parts):
            continue
        if path.is_file() and path.suffix in {".json", ".jsonl"}:
            yield path


def validate_path(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        if path.suffix == ".json":
            with path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        else:
            with path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if line.strip():
                        json.loads(line)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: {exc}")
    return errors


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    documents = list(iter_machine_documents(repository_root))
    errors = [error for path in documents for error in validate_path(path)]
    if errors:
        print("Machine-readable document validation failed:")
        print("\n".join(errors))
        return 1
    print(f"JSON and JSONL validation passed: {len(documents)} files parsed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
