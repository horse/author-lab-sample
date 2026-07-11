#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT_REQUIRED_PATHS = (
    "README.md",
    "AGENTS.md",
    "author-lab-project-manifest.json",
    "repository-component-status-register.json",
    "repository-placeholder-register.json",
    "source-material-storage-and-ingestion-register.jsonl",
    "repository-automation-scripts",
    "repository-validation-tests",
)

SOURCE_AUTHOR_REQUIRED_PATHS = (
    "AGENTS.md",
    "source-author-profile.json",
    "source-rights-register.jsonl",
    "source-corpus/source-corpus-manifest.jsonl",
)

SOURCE_MODEL_REQUIRED_PATHS = (
    "AGENTS.md",
    "VERSION",
    "source-author-model-manifest.json",
    "author-model-loading-map.json",
    "source-author-model-provenance-register.jsonl",
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def persona_required_paths(repository_root: Path, manifest: dict) -> list[str]:
    template_path = repository_root / manifest["persona_scaffold_template_manifest"]
    if template_path.is_file():
        template = load_json(template_path)
        return list(template.get("required_paths", []))
    return [
        "README.md",
        "AGENTS.md",
        "derived-author-persona-manifest.json",
        "derived-author-lineage.json",
        "derived-author-model/VERSION",
        "derived-author-model/derived-author-model-manifest.json",
        "derived-author-model/derived-author-model-loading-map.json",
    ]


def find_missing_paths(repository_root: Path) -> list[str]:
    manifest_path = repository_root / "author-lab-project-manifest.json"
    if not manifest_path.is_file():
        return ["author-lab-project-manifest.json"]
    manifest = load_json(manifest_path)

    required_paths = list(ROOT_REQUIRED_PATHS)
    for field in (
        "shared_writing_harness_directory",
        "runtime_adapters_directory",
        "writing_work_items_directory",
        "author_model_evaluations_directory",
        "author_model_experiments_directory",
        "approved_publications_directory",
        "component_status_register",
        "placeholder_register",
        "source_material_storage_register",
        "document_schema_registry",
        "persona_scaffold_template_manifest",
        "policy_rule_register",
        "rights_policy",
        "ethics_policy",
    ):
        required_paths.append(manifest[field])

    for directory in manifest.get("source_author_directories", []):
        required_paths.append(directory)
        required_paths.extend(f"{directory}/{relative}" for relative in SOURCE_AUTHOR_REQUIRED_PATHS)

    for directory in manifest.get("source_author_model_directories", []):
        required_paths.append(directory)
        required_paths.extend(f"{directory}/{relative}" for relative in SOURCE_MODEL_REQUIRED_PATHS)

    persona_paths = persona_required_paths(repository_root, manifest)
    for directory in manifest.get("derived_author_persona_directories", []):
        required_paths.append(directory)
        required_paths.extend(f"{directory}/{relative}" for relative in persona_paths)

    return sorted({path for path in required_paths if not (repository_root / path).exists()})


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    missing = find_missing_paths(repository_root)
    if missing:
        print("Missing manifest-declared repository paths:")
        for path in missing:
            print(f"- {path}")
        return 1
    print("Manifest-driven repository structure validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
