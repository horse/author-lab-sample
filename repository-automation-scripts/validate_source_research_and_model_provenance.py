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
    segment_owner: dict[str, str] = {}
    segments_by_author: dict[str, set[str]] = {}
    for directory in project["source_author_directories"]:
        author_root = repository_root / directory
        profile = load_json(author_root / "source-author-profile.json")
        source_author_id = profile["source_author_id"]
        if source_author_id in source_authors:
            errors.append(f"Duplicate source_author_id: {source_author_id}")
        source_authors[source_author_id] = (author_root, profile)
        author_segments = segments_by_author.setdefault(source_author_id, set())
        for location_map in author_root.glob(
            "source-corpus/normalized-source-materials/structured-metadata/*-segment-location-map.jsonl"
        ):
            for record in load_jsonl(location_map):
                segment_id = record["segment_id"]
                declared_author = record.get("source_author_id")
                if declared_author is not None and declared_author != source_author_id:
                    errors.append(
                        f"Segment {segment_id} declares source author {declared_author} "
                        f"but is stored under {source_author_id}"
                    )
                if segment_id in segment_owner:
                    errors.append(f"Duplicate segment ID across source corpus: {segment_id}")
                segment_owner[segment_id] = source_author_id
                author_segments.add(segment_id)

    claims_by_author: dict[str, dict[str, dict]] = {}
    claim_owner: dict[str, str] = {}
    for source_author_id, (author_root, profile) in source_authors.items():
        research_root = (author_root / profile["research_directory"]).resolve()
        register_paths = list(
            research_root.glob("**/research-claim-evidence-register.jsonl")
        )
        if len(register_paths) != 1:
            errors.append(
                f"Source author {source_author_id} requires exactly one research claim "
                f"register; found {len(register_paths)}"
            )
            continue
        author_claims = claims_by_author.setdefault(source_author_id, {})
        for claim in load_jsonl(register_paths[0]):
            claim_id = claim["research_claim_id"]
            declared_author = claim.get("source_author_id")
            if declared_author != source_author_id:
                errors.append(
                    f"Research claim {claim_id} declares source author {declared_author!r} "
                    f"but is stored under {source_author_id}"
                )
            if claim_id in claim_owner:
                errors.append(f"Duplicate research_claim_id: {claim_id}")
            claim_owner[claim_id] = source_author_id
            author_claims[claim_id] = claim
            for segment_id in [
                *claim.get("supporting_segments", []),
                *claim.get("counterexample_segments", []),
            ]:
                owner = segment_owner.get(segment_id)
                if owner is None:
                    errors.append(
                        f"Research claim {claim_id} references unknown segment {segment_id}"
                    )
                elif owner != source_author_id:
                    errors.append(
                        f"Research claim {claim_id} references cross-author segment "
                        f"{segment_id} owned by {owner}"
                    )

    model_rule_ids: set[str] = set()
    for directory in project["source_author_model_directories"]:
        model_root = repository_root / directory
        manifest = load_json(model_root / "source-author-model-manifest.json")
        source_author_id = manifest["source_author_id"]
        model_id = manifest["source_author_model_id"]
        if source_author_id not in source_authors:
            errors.append(
                f"Source model {model_id} references unknown source author {source_author_id}"
            )
        provenance_path = model_root / manifest["provenance_register"]
        if not provenance_path.is_file():
            errors.append(
                f"Source model {model_id} has no provenance register at "
                f"{manifest['provenance_register']}"
            )
            continue
        author_claims = claims_by_author.get(source_author_id, {})
        for record in load_jsonl(provenance_path):
            model_rule_id = record["model_rule_id"]
            if model_rule_id in model_rule_ids:
                errors.append(f"Duplicate model_rule_id: {model_rule_id}")
            model_rule_ids.add(model_rule_id)
            if record.get("source_author_id") != source_author_id:
                errors.append(
                    f"Model rule {model_rule_id} declares the wrong source_author_id"
                )
            if record.get("source_author_model_id") != model_id:
                errors.append(
                    f"Model rule {model_rule_id} declares the wrong source_author_model_id"
                )
            for claim_id in record["research_claim_ids"]:
                claim = author_claims.get(claim_id)
                if claim is None:
                    owner = claim_owner.get(claim_id)
                    if owner is None:
                        errors.append(
                            f"Model rule {model_rule_id} references unknown research claim "
                            f"{claim_id}"
                        )
                    else:
                        errors.append(
                            f"Model rule {model_rule_id} references cross-author research "
                            f"claim {claim_id} owned by {owner}"
                        )
                    continue
                if record.get("status") == "approved" and claim.get("status") != "accepted":
                    errors.append(
                        f"Approved model rule {model_rule_id} requires accepted research "
                        f"claim {claim_id}; found {claim.get('status')!r}"
                    )
            model_file = model_root / record["model_file"]
            if not model_file.is_file():
                errors.append(
                    f"Model rule {model_rule_id} references missing model file "
                    f"{record['model_file']}"
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
