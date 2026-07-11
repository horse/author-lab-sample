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


def test_normalization_adds_stable_paragraph_identifiers():
    module = load_script_module()
    result = module.normalize_text("First paragraph.\n\nSecond paragraph.\n", "SOURCE-TEST-0001")
    assert "SOURCE-TEST-0001-paragraph-00001" in result
    assert "SOURCE-TEST-0001-paragraph-00002" in result
