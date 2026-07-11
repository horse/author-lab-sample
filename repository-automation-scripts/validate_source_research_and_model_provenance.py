#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Iterable


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def validate_provenance_chain(repository_root: Path) -> list[str]:
    project = load_json(repository_root / "author-lab-project-manifest.json")
    errors: list[str] = []

    source_authors: dict[str, tuple[Path, dict]] = {}
    segment_ids: set[str] = set()
    for directory in project["source_author_directories"]:
        author_root = repository_root / directory
        profile = load_json(author_root / "source-author-profile.json")
        source_author_id = profile["source_author_id"]
        source_authors[source_author_id] = (author_root, profile)
        for location_map in author_root.glob(
            "source-corpus/normalized-source-materials/structured-metadata/*-segment-location-map.jsonl"
        ):
            for record in load_jsonl(location_map):
                segment_id = record["segment_id"]
                if segment_id in segment_ids:
                    errors.append(f"Duplicate segment ID across source corpus: {segment_id}")
                segment_ids.add(segment_id)

    research_claims: dict[str, dict] = {}
    for source_author_id, (author_root, profile) in source_authors.items():
        research_root = (author_root / profile["research_directory"]).resolve()
        register_paths = list(
            research_root.glob("**/research-claim-evidence-register.jsonl")
        )
        if len(register_paths) != 1:
            errors.append(
                f"Source author {source_author_id} requires exactly one research claim register; found {len(register_paths)}"
            )
            continue
        register_path = register_paths[0]
        for claim in load_jsonl(register_path):
            claim_id = claim["research_claim_id"]
            if claim_id in research_claims:
                errors.append(f"Duplicate research_claim_id: {claim_id}")
            research_claims[claim_id] = claim
            for segment_id in [
                *claim.get("supporting_segments", []),
                *claim.get("counterexample_segments", []),
            ]:
                if segment_id not in segment_ids:
                    errors.append(
                        f"Research claim {claim_id} references unknown segment {segment_id}"
                    )

    model_rule_ids: set[str] = set()
    for directory in project["source_author_model_directories"]:
        model_root = repository_root / directory
        manifest = load_json(model_root / "source-author-model-manifest.json")
        source_author_id = manifest["source_author_id"]
        if source_author_id not in source_authors:
            errors.append(
                f"Source model {manifest['source_author_model_id']} references unknown source author {source_author_id}"
            )
        provenance_path = model_root / manifest["provenance_register"]
        if not provenance_path.is_file():
            errors.append(
                f"Source model {manifest['source_author_model_id']} has no provenance register at {manifest['provenance_register']}"
            )
            continue
        for record in load_jsonl(provenance_path):
            model_rule_id = record["model_rule_id"]
            if model_rule_id in model_rule_ids:
                errors.append(f"Duplicate model_rule_id: {model_rule_id}")
            model_rule_ids.add(model_rule_id)
            for claim_id in record["research_claim_ids"]:
                if claim_id not in research_claims:
                    errors.append(
                        f"Model rule {model_rule_id} references unknown research claim {claim_id}"
                    )
            model_file = model_root / record["model_file"]
            if not model_file.is_file():
                errors.append(
                    f"Model rule {model_rule_id} references missing model file {record['model_file']}"
                )

    return errors


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    errors = validate_provenance_chain(repository_root)
    if errors:
        print("Source research and model provenance validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Source research and model provenance validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
