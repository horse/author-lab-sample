#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker


REGISTRY_PATH = Path("shared-writing-harness/machine-readable-contracts/document-schema-registry.json")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_jsonl_records(path: Path) -> Iterable[tuple[int, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.strip():
                yield line_number, json.loads(line)


def format_error_location(error) -> str:
    if not error.absolute_path:
        return "$"
    return "$" + "".join(f"[{item!r}]" if isinstance(item, str) else f"[{item}]" for item in error.absolute_path)


def validate_document(path: Path, document_format: str, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    if document_format == "json":
        records = [(None, load_json(path))]
    elif document_format == "jsonl":
        records = list(iter_jsonl_records(path))
    else:
        return [f"{path}: unsupported document format {document_format!r}"]

    for line_number, record in records:
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
            line_suffix = f":{line_number}" if line_number is not None else ""
            errors.append(
                f"{path}{line_suffix} {format_error_location(error)}: {error.message}"
            )
    return errors


def validate_registered_documents(repository_root: Path) -> tuple[int, list[str]]:
    registry = load_json(repository_root / REGISTRY_PATH)
    validated_paths: set[Path] = set()
    errors: list[str] = []

    for entry in registry.get("entries", []):
        pattern = entry["path_pattern"]
        matches = sorted(path for path in repository_root.glob(pattern) if path.is_file())
        if entry.get("required_match", False) and not matches:
            errors.append(f"Schema registry pattern matched no files: {pattern}")
            continue

        schema_path = repository_root / entry["schema_path"]
        if not schema_path.is_file():
            errors.append(f"Schema file does not exist: {entry['schema_path']}")
            continue
        schema = load_json(schema_path)
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"Invalid schema {entry['schema_path']}: {exc}")
            continue

        for path in matches:
            try:
                errors.extend(validate_document(path, entry["document_format"], schema))
                validated_paths.add(path.resolve())
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{path}: {exc}")

    return len(validated_paths), errors


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    validated_count, errors = validate_registered_documents(repository_root)
    if errors:
        print("Machine-readable contract schema validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Machine-readable contract schema validation passed: {validated_count} files validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
