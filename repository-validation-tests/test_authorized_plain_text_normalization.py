# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "normalize_authorized_plain_text_source.py"


def load_script_module():
    spec = spec_from_file_location("text_normalizer", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_normalization_adds_versioned_segment_identifiers_and_fingerprints():
    module = load_script_module()
    normalized_text, location_records = module.normalize_text(
        "First paragraph.\n\nSecond paragraph.\n",
        source_id="SOURCE-TEST-0001",
        edition_id="edition-01",
        segmentation_version="segmentation-01",
    )

    assert "SOURCE-TEST-0001.edition-01.segmentation-01.segment-00001" in normalized_text
    assert "SOURCE-TEST-0001.edition-01.segmentation-01.segment-00002" in normalized_text
    assert len(location_records) == 2
    assert location_records[0]["edition_id"] == "edition-01"
    assert location_records[0]["segmentation_version"] == "segmentation-01"
    assert len(location_records[0]["content_sha256"]) == 64
    assert location_records[0]["segment_id"] in normalized_text


def test_resegmentation_uses_a_new_namespace_even_for_unchanged_content():
    module = load_script_module()
    _, first_records = module.normalize_text(
        "Same paragraph.",
        source_id="SOURCE-TEST-0001",
        edition_id="edition-01",
        segmentation_version="segmentation-01",
    )
    _, second_records = module.normalize_text(
        "Same paragraph.",
        source_id="SOURCE-TEST-0001",
        edition_id="edition-01",
        segmentation_version="segmentation-02",
    )

    assert first_records[0]["content_sha256"] == second_records[0]["content_sha256"]
    assert first_records[0]["segment_id"] != second_records[0]["segment_id"]
