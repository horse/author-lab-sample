#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Iterable

POLICY_REFERENCE_PATTERN = re.compile(r"\bPOLICY-[A-Z]+-[0-9]{3}\b")
SKIPPED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "venv",
    "generated-site-output",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
BINARY_SUFFIXES = {
    ".epub",
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".mp3",
    ".mp4",
    ".zip",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def resolve_policy_register(repository_root: Path) -> Path:
    project_path = repository_root / "author-lab-project-manifest.json"
    if project_path.is_file():
        project = load_json(project_path)
        relative_path = project.get("policy_rule_register")
        if relative_path:
            return repository_root / relative_path
    return (
        repository_root
        / "shared-writing-harness/harness-policies/policy-rule-register.jsonl"
    )


def iter_managed_text_files(repository_root: Path):
    for path in repository_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in BINARY_SUFFIXES:
            continue
        relative_path = path.relative_to(repository_root)
        if any(
            part in SKIPPED_DIRECTORY_NAMES or part.endswith(".egg-info")
            for part in relative_path.parts
        ):
            continue
        yield path, relative_path.as_posix()


def validate_policy_references(
    repository_root: Path,
    policy_register_path: Path | None = None,
) -> list[str]:
    register_path = policy_register_path or resolve_policy_register(repository_root)
    if not register_path.is_file():
        return [
            f"{register_path.relative_to(repository_root)}: policy rule register does not exist"
        ]

    policy_ids: set[str] = set()
    errors: list[str] = []
    for record in load_jsonl(register_path):
        policy_id = record["policy_rule_id"]
        if policy_id in policy_ids:
            errors.append(f"Duplicate policy_rule_id: {policy_id}")
        policy_ids.add(policy_id)
        policy_file = repository_root / record["policy_file"]
        if not policy_file.is_file():
            errors.append(
                f"{register_path.relative_to(repository_root)}: {policy_id} references missing policy file {record['policy_file']}"
            )

    for path, relative_path in iter_managed_text_files(repository_root):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for policy_id in sorted(set(POLICY_REFERENCE_PATTERN.findall(text))):
            if policy_id not in policy_ids:
                errors.append(
                    f"{relative_path}: unknown policy rule reference {policy_id}"
                )

    return errors


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    errors = validate_policy_references(repository_root)
    if errors:
        print("Policy rule reference validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Policy rule reference validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
