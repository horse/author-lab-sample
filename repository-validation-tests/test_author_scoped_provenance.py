# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts/validate_source_research_and_model_provenance.py"


def load_module():
    spec = spec_from_file_location("author_scoped_provenance", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records), encoding="utf-8")


def prepare_two_author_repository(root: Path) -> None:
    write_json(
        root / "author-lab-project-manifest.json",
        {
            "source_author_directories": [
                "source-authors/source-a",
                "source-authors/source-b",
            ],
            "source_author_model_directories": [
                "source-author-models/model-a",
                "source-author-models/model-b",
            ],
        },
    )
    for author_id, model_id in (("source-a", "model-a"), ("source-b", "model-b")):
        author_root = root / "source-authors" / author_id
        research_root = root / "source-author-research" / f"{author_id}-research"
        write_json(
            author_root / "source-author-profile.json",
            {
                "source_author_id": author_id,
                "research_directory": f"../../source-author-research/{author_id}-research",
            },
        )
        segment_id = f"SEGMENT-{author_id.upper()}-0001"
        write_jsonl(
            author_root / "source-corpus/normalized-source-materials/structured-metadata/source-segment-location-map.jsonl",
            [
                {
                    "source_author_id": author_id,
                    "source_id": f"SOURCE-{author_id.upper()}-0001",
                    "segment_id": segment_id,
                }
            ],
        )
        write_jsonl(
            research_root / "evidence-and-confidence/research-claim-evidence-register.jsonl",
            [
                {
                    "source_author_id": author_id,
                    "research_claim_id": f"CLAIM-{author_id.upper()}-0001",
                    "status": "accepted",
                    "supporting_segments": [segment_id],
                    "counterexample_segments": [],
                }
            ],
        )
        model_root = root / "source-author-models" / model_id
        write_json(
            model_root / "source-author-model-manifest.json",
            {
                "source_author_model_id": model_id,
                "source_author_id": author_id,
                "model_version": "1.0.0",
                "provenance_register": "source-author-model-provenance-register.jsonl",
            },
        )
        (model_root / "core-author-model").mkdir(parents=True, exist_ok=True)
        (model_root / "core-author-model/rule.md").write_text("# Rule\n", encoding="utf-8")
        write_jsonl(
            model_root / "source-author-model-provenance-register.jsonl",
            [
                {
                    "source_author_id": author_id,
                    "source_author_model_id": model_id,
                    "model_rule_id": f"RULE-{model_id.upper()}-0001",
                    "research_claim_ids": [f"CLAIM-{author_id.upper()}-0001"],
                    "model_file": "core-author-model/rule.md",
                    "status": "approved",
                }
            ],
        )


def test_research_claim_cannot_reference_another_authors_segment(tmp_path):
    module = load_module()
    prepare_two_author_repository(tmp_path)
    claim_path = tmp_path / "source-author-research/source-a-research/evidence-and-confidence/research-claim-evidence-register.jsonl"
    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    claim["supporting_segments"] = ["SEGMENT-SOURCE-B-0001"]
    write_jsonl(claim_path, [claim])

    errors = module.validate_provenance_chain(tmp_path)

    assert any("cross-author segment" in error for error in errors)


def test_source_model_cannot_reference_another_authors_claim(tmp_path):
    module = load_module()
    prepare_two_author_repository(tmp_path)
    provenance_path = tmp_path / "source-author-models/model-a/source-author-model-provenance-register.jsonl"
    record = json.loads(provenance_path.read_text(encoding="utf-8"))
    record["research_claim_ids"] = ["CLAIM-SOURCE-B-0001"]
    write_jsonl(provenance_path, [record])

    errors = module.validate_provenance_chain(tmp_path)

    assert any("cross-author research claim" in error for error in errors)


def test_approved_model_rule_requires_accepted_claim(tmp_path):
    module = load_module()
    prepare_two_author_repository(tmp_path)
    claim_path = tmp_path / "source-author-research/source-a-research/evidence-and-confidence/research-claim-evidence-register.jsonl"
    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    claim["status"] = "proposed"
    write_jsonl(claim_path, [claim])

    errors = module.validate_provenance_chain(tmp_path)

    assert any("requires accepted research claim" in error for error in errors)
