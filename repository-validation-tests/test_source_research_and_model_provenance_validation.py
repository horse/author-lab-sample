# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_source_research_and_model_provenance.py"


def load_script_module():
    spec = spec_from_file_location("provenance_validator", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
        encoding="utf-8",
    )


def prepare_repository(root: Path, segment_id: str, claim_segment_id: str, provenance_claim_id: str) -> None:
    write_json(
        root / "author-lab-project-manifest.json",
        {
            "source_author_directories": ["source-authors/source-a"],
            "source_author_model_directories": ["source-author-models/source-a-model"],
        },
    )
    write_json(
        root / "source-authors/source-a/source-author-profile.json",
        {
            "source_author_id": "source-a",
            "research_directory": "../../source-author-research/source-a-research",
        },
    )
    write_jsonl(
        root / "source-authors/source-a/source-corpus/normalized-source-materials/structured-metadata/SOURCE-A-segment-location-map.jsonl",
        [{"source_author_id": "source-a", "segment_id": segment_id}],
    )
    write_jsonl(
        root / "source-author-research/source-a-research/evidence-and-confidence/research-claim-evidence-register.jsonl",
        [
            {
                "source_author_id": "source-a",
                "research_claim_id": "RESEARCH-CLAIM-0001",
                "status": "accepted",
                "supporting_segments": [claim_segment_id],
                "counterexample_segments": [],
            }
        ],
    )
    write_json(
        root / "source-author-models/source-a-model/source-author-model-manifest.json",
        {
            "source_author_model_id": "source-a-model",
            "source_author_id": "source-a",
            "model_version": "1.0.0",
            "provenance_register": "source-author-model-provenance-register.jsonl",
        },
    )
    model_file = root / "source-author-models/source-a-model/core-author-model/reasoning-patterns.md"
    model_file.parent.mkdir(parents=True, exist_ok=True)
    model_file.write_text("# Model rule\n", encoding="utf-8")
    write_jsonl(
        root / "source-author-models/source-a-model/source-author-model-provenance-register.jsonl",
        [
            {
                "source_author_id": "source-a",
                "source_author_model_id": "source-a-model",
                "model_rule_id": "SOURCE-MODEL-RULE-0001",
                "research_claim_ids": [provenance_claim_id],
                "model_file": "core-author-model/reasoning-patterns.md",
                "status": "approved",
            }
        ],
    )


def test_valid_segment_claim_and_model_provenance_chain_passes(tmp_path):
    module = load_script_module()
    segment_id = "SOURCE-A.edition-01.segmentation-01.segment-00001-abcdef123456"
    prepare_repository(tmp_path, segment_id, segment_id, "RESEARCH-CLAIM-0001")
    assert module.validate_provenance_chain(tmp_path) == []


def test_missing_segment_and_unknown_claim_are_rejected(tmp_path):
    module = load_script_module()
    segment_id = "SOURCE-A.edition-01.segmentation-01.segment-00001-abcdef123456"
    prepare_repository(
        tmp_path,
        segment_id,
        "SOURCE-A.edition-01.segmentation-01.segment-99999-missing00000",
        "RESEARCH-CLAIM-9999",
    )
    errors = module.validate_provenance_chain(tmp_path)
    assert any("unknown segment" in error for error in errors)
    assert any("unknown research claim RESEARCH-CLAIM-9999" in error for error in errors)
