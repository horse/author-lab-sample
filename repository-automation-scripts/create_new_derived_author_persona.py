#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def validate_identifier(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Identifier must use descriptive kebab-case.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new derived-author persona scaffold.")
    parser.add_argument("derived_author_id", type=validate_identifier)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--source-model-id", required=True)
    parser.add_argument("--source-model-version", required=True)
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    persona_root = repository_root / "derived-author-personas" / arguments.derived_author_id
    if persona_root.exists():
        raise SystemExit(f"Persona already exists: {persona_root}")

    directories = (
        "derivation-profile",
        "derived-author-model/core-derived-author-model",
        "derived-author-model/genre-specific-writing-modes",
        "author-specific-writing-harness",
        "derived-author-memory",
        "derived-author-writing-work-items",
        "derived-author-evaluations",
        "derived-author-publications",
    )
    for directory in directories:
        (persona_root / directory).mkdir(parents=True, exist_ok=True)

    manifest = {
        "_sample_comment": SAMPLE_MARKER,
        "schema_version": "1.0.0",
        "derived_author_id": arguments.derived_author_id,
        "display_name": arguments.display_name,
        "persona_type": "derived-pseudonymous-author",
        "status": "sample-development",
        "lineage_file": "derived-author-lineage.json",
        "author_model_directory": "derived-author-model",
    }
    lineage = {
        "_sample_comment": SAMPLE_MARKER,
        "schema_version": "1.0.0",
        "derived_author_id": arguments.derived_author_id,
        "source_models": [{
            "source_author_model_id": arguments.source_model_id,
            "source_author_model_version": arguments.source_model_version,
            "role": "primary-influence",
            "declared_design_weight": 1.0,
        }],
        "may_claim_source_author_identity": False,
        "may_claim_source_author_experience": False,
        "may_quote_source_author_without_citation": False,
    }
    (persona_root / "derived-author-persona-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (persona_root / "derived-author-lineage.json").write_text(json.dumps(lineage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (persona_root / "README.md").write_text(f"# {arguments.display_name}\n\n<!-- {SAMPLE_MARKER} -->\n", encoding="utf-8")
    print(f"Created derived-author persona scaffold: {persona_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
