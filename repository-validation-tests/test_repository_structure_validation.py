# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_author_lab_repository_structure.py"


def load_script_module():
    spec = spec_from_file_location("structure_validator", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_required_repository_paths_exist():
    module = load_script_module()
    assert module.find_missing_paths(REPOSITORY_ROOT) == []
