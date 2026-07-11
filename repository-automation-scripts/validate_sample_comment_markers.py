#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

from fnmatch import fnmatch
import json
from pathlib import Path
import sys

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"
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
DEFAULT_IGNORED_PATTERNS = (
    ".git/**",
    ".venv/**",
    "venv/**",
    "**/__pycache__/**",
    "**/*.egg-info/**",
    ".pytest_cache/**",
    ".mypy_cache/**",
    ".ruff_cache/**",
    "generated-site-output/**",
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def path_is_generated_or_environment_metadata(relative_path: Path) -> bool:
    return any(
        part in SKIPPED_DIRECTORY_NAMES or part.endswith(".egg-info")
        for part in relative_path.parts
    )


def path_is_ignored(relative_path: str, patterns: list[str]) -> bool:
    return any(fnmatch(relative_path, pattern) for pattern in patterns)


def file_has_marker(path: Path) -> bool:
    if path.suffix == ".json":
        return load_json(path).get("_sample_comment") == SAMPLE_MARKER
    if path.suffix == ".jsonl":
        with path.open("r", encoding="utf-8") as handle:
            first_record = next((line for line in handle if line.strip()), "")
        return bool(first_record) and json.loads(first_record).get(
            "_sample_comment"
        ) == SAMPLE_MARKER
    return SAMPLE_MARKER in path.read_text(encoding="utf-8")


def iter_managed_text_files(
    repository_root: Path,
    ignored_patterns: list[str],
):
    for path in repository_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() in BINARY_SUFFIXES:
            continue
        relative_path_object = path.relative_to(repository_root)
        if path_is_generated_or_environment_metadata(relative_path_object):
            continue
        relative_path = relative_path_object.as_posix()
        if path_is_ignored(relative_path, ignored_patterns):
            continue
        yield path, relative_path


def validate_placeholders(repository_root: Path) -> list[str]:
    project_path = repository_root / "author-lab-project-manifest.json"
    if not project_path.is_file():
        return ["author-lab-project-manifest.json: required repository control file is missing"]
    project = load_json(project_path)
    register_path = repository_root / project["placeholder_register"]
    if not register_path.is_file():
        return [f"{project['placeholder_register']}: placeholder register is missing"]
    register = load_json(register_path)

    repository_mode = project.get("repository_mode")
    if register.get("repository_mode") != repository_mode:
        return ["repository placeholder register mode does not match project manifest"]

    ignored_patterns = list(DEFAULT_IGNORED_PATTERNS)
    ignored_patterns.extend(register.get("ignored_generated_path_patterns", []))
    registered_paths = register.get("registered_placeholder_paths", [])
    registered_set = set(registered_paths)
    errors: list[str] = []

    if len(registered_set) != len(registered_paths):
        errors.append("repository-placeholder-register.json: duplicate registered paths")

    if repository_mode == "reference-sample":
        if register.get("placeholder_policy") != "all-managed-text-files":
            errors.append(
                "reference-sample mode requires placeholder_policy=all-managed-text-files"
            )
        for path, relative_path in iter_managed_text_files(
            repository_root,
            ignored_patterns,
        ):
            try:
                if not file_has_marker(path):
                    errors.append(f"{relative_path}: missing required sample marker")
            except (OSError, UnicodeDecodeError, json.JSONDecodeError, StopIteration):
                errors.append(f"{relative_path}: could not validate sample marker")
        return errors

    if repository_mode == "active-author-lab":
        if register.get("placeholder_policy") != "registered-placeholder-paths-only":
            errors.append(
                "active-author-lab mode requires placeholder_policy=registered-placeholder-paths-only"
            )
        for registered_path in sorted(registered_set):
            path = repository_root / registered_path
            if not path.is_file():
                errors.append(f"{registered_path}: registered placeholder file does not exist")
                continue
            try:
                if not file_has_marker(path):
                    errors.append(
                        f"{registered_path}: registered placeholder is missing its marker"
                    )
            except (OSError, UnicodeDecodeError, json.JSONDecodeError, StopIteration):
                errors.append(f"{registered_path}: could not validate sample marker")

        for path, relative_path in iter_managed_text_files(
            repository_root,
            ignored_patterns,
        ):
            if relative_path in registered_set:
                continue
            try:
                if file_has_marker(path):
                    errors.append(
                        f"{relative_path}: unregistered production file still contains sample marker"
                    )
            except (OSError, UnicodeDecodeError, json.JSONDecodeError, StopIteration):
                errors.append(f"{relative_path}: could not validate sample marker")
        return errors

    return [f"Unknown repository_mode: {repository_mode!r}"]


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    errors = validate_placeholders(repository_root)
    if errors:
        print("Repository placeholder validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository-mode-aware placeholder validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
