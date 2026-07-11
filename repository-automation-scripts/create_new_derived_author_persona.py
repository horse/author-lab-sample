#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
from pathlib import Path
import re
import shutil
import sys
from typing import Any

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from atomic_repository_update import (  # noqa: E402
    atomic_replace_text_files,
    promote_staged_directory,
    staged_sibling_directory,
)
from repository_mode_support import (  # noqa: E402
    RepositoryModeContext,
    dump_json,
    load_json,
)


def validate_identifier(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Identifier must use descriptive kebab-case.")
    return value


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_json(document), encoding="utf-8")


def resolve_source_model(
    repository_root: Path,
    project: dict[str, Any],
    source_model_id: str,
    source_model_version: str,
) -> tuple[Path, dict[str, Any]]:
    matches: list[tuple[Path, dict[str, Any]]] = []
    for directory in project.get("source_author_model_directories", []):
        manifest_path = repository_root / directory / "source-author-model-manifest.json"
        if not manifest_path.is_file():
            continue
        manifest = load_json(manifest_path)
        if manifest.get("source_author_model_id") == source_model_id:
            matches.append((manifest_path.parent, manifest))
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one source model {source_model_id!r}; found {len(matches)}"
        )
    model_root, manifest = matches[0]
    if manifest.get("model_version") != source_model_version:
        raise ValueError(
            f"Source model {source_model_id!r} version mismatch: "
            f"expected {manifest.get('model_version')!r}, received {source_model_version!r}"
        )
    return model_root, manifest


def render_persona_tree(
    staging_root: Path,
    context: RepositoryModeContext,
    template: dict[str, Any],
    replacements: dict[str, str],
    derived_author_id: str,
    display_name: str,
    source_model_id: str,
    source_model_version: str,
) -> None:
    for directory in template["required_directories"]:
        (staging_root / directory).mkdir(parents=True, exist_ok=True)

    guidance = (
        "Replace this sample guidance with reviewed persona-specific content before production use."
        if context.is_reference_sample
        else "Complete this scaffold with reviewed persona-specific content before production use."
    )
    for specification in template["markdown_files"]:
        path = staging_root / specification["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        title = context.render_text(specification["title"], replacements)
        purpose = context.render_text(specification["purpose"], replacements)
        path.write_text(
            f"# {title}\n\n{context.markdown_marker()}{purpose}\n\n{guidance}\n",
            encoding="utf-8",
        )

    for genre_mode in template["default_genre_modes"]:
        path = staging_root / genre_mode["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        title = context.render_text(genre_mode["title"], replacements)
        path.write_text(
            f"# {title}\n\n{context.markdown_marker()}"
            "Define this persona's reviewed genre-specific overlay without duplicating the core model.\n",
            encoding="utf-8",
        )

    persona_manifest = context.with_json_marker(
        {
            "schema_version": "1.0.0",
            "derived_author_id": derived_author_id,
            "display_name": display_name,
            "persona_type": "derived-pseudonymous-author",
            "status": context.initial_status("sample-development", "draft"),
            "primary_language": context.project["default_language"],
            "lineage_file": "derived-author-lineage.json",
            "derivation_directory": "derivation-profile",
            "author_model_directory": "derived-author-model",
            "harness_overlay_directory": "author-specific-writing-harness",
            "memory_directory": "derived-author-memory",
            "work_items_directory": "derived-author-writing-work-items",
            "evaluations_directory": "derived-author-evaluations",
            "publications_directory": "derived-author-publications",
        }
    )
    lineage = context.with_json_marker(
        {
            "schema_version": "1.0.0",
            "derived_author_id": derived_author_id,
            "source_models": [
                {
                    "source_author_model_id": source_model_id,
                    "source_author_model_version": source_model_version,
                    "role": "primary-influence",
                    "declared_design_weight": 1.0,
                }
            ],
            "may_claim_source_author_identity": False,
            "may_claim_source_author_experience": False,
            "may_quote_source_author_without_citation": False,
            "independent_since": None,
        }
    )
    model_id = f"{derived_author_id}-model"
    model_manifest = context.with_json_marker(
        {
            "schema_version": "1.0.0",
            "derived_author_model_id": model_id,
            "derived_author_id": derived_author_id,
            "model_version": "0.1.0",
            "status": context.initial_status("sample-unreviewed", "unreviewed"),
            "core_model_directory": "core-derived-author-model",
            "genre_modes_directory": "genre-specific-writing-modes",
            "loading_map": "derived-author-model-loading-map.json",
        }
    )
    default_core = [
        path.removeprefix("derived-author-model/")
        for path in template["required_paths"]
        if path.startswith("derived-author-model/core-derived-author-model/")
    ]
    genre_modes = {
        Path(item["path"]).stem.removesuffix("-writing-mode"): item[
            "path"
        ].removeprefix("derived-author-model/")
        for item in template["default_genre_modes"]
    }
    loading_map = context.with_json_marker(
        {"default_core": default_core, "genre_modes": genre_modes}
    )

    write_json(staging_root / "derived-author-persona-manifest.json", persona_manifest)
    write_json(staging_root / "derived-author-lineage.json", lineage)
    (staging_root / "derived-author-model/VERSION").write_text(
        f"{context.python_marker()}0.1.0\n", encoding="utf-8"
    )
    write_json(
        staging_root / "derived-author-model/derived-author-model-manifest.json",
        model_manifest,
    )
    write_json(
        staging_root / "derived-author-model/derived-author-model-loading-map.json",
        loading_map,
    )

    (staging_root / "derived-author-memory/publication-history.jsonl").write_text(
        context.empty_jsonl(
            {
                "publication_id": None,
                "work_item_id": None,
                "status": "generated-empty",
                "publication_path": None,
            }
        ),
        encoding="utf-8",
    )
    (
        staging_root
        / "derived-author-writing-work-items/derived-author-work-item-index.jsonl"
    ).write_text(
        context.empty_jsonl(
            {
                "derived_author_id": derived_author_id,
                "index_status": "generated-empty",
                "canonical_work_item_id": None,
            }
        ),
        encoding="utf-8",
    )
    (
        staging_root
        / "derived-author-publications/derived-author-publication-index.jsonl"
    ).write_text(
        context.empty_jsonl(
            {
                "derived_author_id": derived_author_id,
                "index_status": "generated-empty",
                "canonical_publication_id": None,
            }
        ),
        encoding="utf-8",
    )

    missing = [
        path for path in template["required_paths"] if not (staging_root / path).exists()
    ]
    if missing:
        raise ValueError(f"Persona template rendering missed required paths: {missing}")


def updated_component_register(
    context: RepositoryModeContext,
    register: dict[str, Any],
    derived_author_id: str,
    relative_path: str,
) -> dict[str, Any]:
    components = list(register.get("components", []))
    if any(item.get("path") == relative_path for item in components):
        raise ValueError(f"Component path is already registered: {relative_path}")
    components.append(
        {
            "component_id": derived_author_id,
            "path": relative_path,
            "component_class": "example" if context.is_reference_sample else "core",
            "implementation_status": "scaffolded",
            "validation_status": "template-generated-unreviewed",
            "production_ready": False,
            "real_content_status": (
                "sample-only" if context.is_reference_sample else "not-started"
            ),
            "experimentally_validated": False,
        }
    )
    return {
        **register,
        "components": sorted(components, key=lambda item: item["component_id"]),
    }


def create_persona(
    repository_root: Path,
    derived_author_id: str,
    display_name: str,
    source_model_id: str,
    source_model_version: str,
) -> Path:
    context = RepositoryModeContext.from_project(repository_root)
    project = dict(context.project)
    resolve_source_model(
        repository_root, project, source_model_id, source_model_version
    )

    template_path = repository_root / project["persona_scaffold_template_manifest"]
    if template_path.name != "template-manifest.json" or not template_path.is_file():
        raise ValueError("Persona scaffold template must resolve to template-manifest.json")
    template = load_json(template_path)

    persona_relative = f"derived-author-personas/{derived_author_id}"
    persona_root = repository_root / persona_relative
    if persona_root.exists():
        raise ValueError(f"Persona already exists: {persona_root}")
    if persona_relative in project.get("derived_author_persona_directories", []):
        raise ValueError(f"Persona is already registered: {persona_relative}")

    replacements = {
        "derived_author_id": derived_author_id,
        "display_name": display_name,
        "source_model_id": source_model_id,
        "source_model_version": source_model_version,
    }

    component_path = repository_root / project["component_status_register"]
    component_register = load_json(component_path)
    updated_project = {
        **project,
        "derived_author_persona_directories": sorted(
            [*project.get("derived_author_persona_directories", []), persona_relative]
        ),
    }
    updated_components = updated_component_register(
        context, component_register, derived_author_id, persona_relative
    )

    with staged_sibling_directory(persona_root) as staging_root:
        render_persona_tree(
            staging_root,
            context,
            template,
            replacements,
            derived_author_id,
            display_name,
            source_model_id,
            source_model_version,
        )
        promote_staged_directory(staging_root, persona_root)
        try:
            atomic_replace_text_files(
                {
                    repository_root / "author-lab-project-manifest.json": dump_json(
                        updated_project
                    ),
                    component_path: dump_json(updated_components),
                }
            )
        except Exception:
            shutil.rmtree(persona_root, ignore_errors=True)
            raise
    return persona_root


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a complete template-driven derived-author persona."
    )
    parser.add_argument("derived_author_id", type=validate_identifier)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--source-model-id", required=True)
    parser.add_argument("--source-model-version", required=True)
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    persona_root = create_persona(
        repository_root,
        arguments.derived_author_id,
        arguments.display_name,
        arguments.source_model_id,
        arguments.source_model_version,
    )
    print(f"Created complete template-driven persona: {persona_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
