#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def validate_identifier(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Identifier must use descriptive kebab-case.")
    return value


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def render_text(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_persona(
    repository_root: Path,
    derived_author_id: str,
    display_name: str,
    source_model_id: str,
    source_model_version: str,
) -> Path:
    project = load_json(repository_root / "author-lab-project-manifest.json")
    template_path = repository_root / project["persona_scaffold_template_manifest"]
    if template_path.name != "template-manifest.json":
        raise SystemExit("Persona scaffold template must resolve to template-manifest.json")
    template = load_json(template_path)

    persona_root = repository_root / "derived-author-personas" / derived_author_id
    if persona_root.exists():
        raise SystemExit(f"Persona already exists: {persona_root}")

    replacements = {
        "derived_author_id": derived_author_id,
        "display_name": display_name,
        "source_model_id": source_model_id,
        "source_model_version": source_model_version,
    }

    for directory in template["required_directories"]:
        (persona_root / directory).mkdir(parents=True, exist_ok=True)

    for file_specification in template["markdown_files"]:
        path = persona_root / file_specification["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        title = render_text(file_specification["title"], replacements)
        purpose = render_text(file_specification["purpose"], replacements)
        body = (
            f"# {title}\n\n"
            f"<!-- {SAMPLE_MARKER} -->\n\n"
            f"{purpose}\n\n"
            "Replace this sample guidance with reviewed persona-specific content before production use.\n"
        )
        path.write_text(body, encoding="utf-8")

    for genre_mode in template["default_genre_modes"]:
        path = persona_root / genre_mode["path"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# {genre_mode['title']}\n\n<!-- {SAMPLE_MARKER} -->\n\n"
            "Define this persona's reviewed genre-specific overlay without duplicating the core model.\n",
            encoding="utf-8",
        )

    persona_manifest = {
        "_sample_comment": SAMPLE_MARKER,
        "schema_version": "1.0.0",
        "derived_author_id": derived_author_id,
        "display_name": display_name,
        "persona_type": "derived-pseudonymous-author",
        "status": "sample-development",
        "primary_language": project["default_language"],
        "lineage_file": "derived-author-lineage.json",
        "derivation_directory": "derivation-profile",
        "author_model_directory": "derived-author-model",
        "harness_overlay_directory": "author-specific-writing-harness",
        "memory_directory": "derived-author-memory",
        "work_items_directory": "derived-author-writing-work-items",
        "evaluations_directory": "derived-author-evaluations",
        "publications_directory": "derived-author-publications",
    }
    lineage = {
        "_sample_comment": SAMPLE_MARKER,
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
    model_id = f"{derived_author_id}-model"
    model_manifest = {
        "_sample_comment": SAMPLE_MARKER,
        "schema_version": "1.0.0",
        "derived_author_model_id": model_id,
        "derived_author_id": derived_author_id,
        "model_version": "0.1.0",
        "status": "sample-unreviewed",
        "core_model_directory": "core-derived-author-model",
        "genre_modes_directory": "genre-specific-writing-modes",
        "loading_map": "derived-author-model-loading-map.json",
    }
    default_core = [
        path.removeprefix("derived-author-model/")
        for path in template["required_paths"]
        if path.startswith("derived-author-model/core-derived-author-model/")
    ]
    genre_modes = {
        Path(item["path"]).stem.removesuffix("-writing-mode"): item["path"].removeprefix("derived-author-model/")
        for item in template["default_genre_modes"]
    }
    loading_map = {
        "_sample_comment": SAMPLE_MARKER,
        "default_core": default_core,
        "genre_modes": genre_modes,
    }

    write_json(persona_root / "derived-author-persona-manifest.json", persona_manifest)
    write_json(persona_root / "derived-author-lineage.json", lineage)
    (persona_root / "derived-author-model/VERSION").write_text(
        f"# {SAMPLE_MARKER}\n0.1.0\n",
        encoding="utf-8",
    )
    write_json(persona_root / "derived-author-model/derived-author-model-manifest.json", model_manifest)
    write_json(persona_root / "derived-author-model/derived-author-model-loading-map.json", loading_map)

    (persona_root / "derived-author-memory/publication-history.jsonl").write_text(
        json.dumps(
            {
                "_sample_comment": SAMPLE_MARKER,
                "publication_id": None,
                "work_item_id": None,
                "status": "generated-empty",
                "publication_path": None,
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (persona_root / "derived-author-writing-work-items/derived-author-work-item-index.jsonl").write_text(
        json.dumps(
            {
                "_sample_comment": SAMPLE_MARKER,
                "derived_author_id": derived_author_id,
                "index_status": "generated-empty",
                "canonical_work_item_id": None,
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (persona_root / "derived-author-publications/derived-author-publication-index.jsonl").write_text(
        json.dumps(
            {
                "_sample_comment": SAMPLE_MARKER,
                "derived_author_id": derived_author_id,
                "index_status": "generated-empty",
                "canonical_publication_id": None,
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    missing = [path for path in template["required_paths"] if not (persona_root / path).exists()]
    if missing:
        raise SystemExit(f"Persona template rendering missed required paths: {missing}")
    return persona_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a complete template-driven derived-author persona.")
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
