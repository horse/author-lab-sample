# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import subprocess
import sys

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_sample_comment_markers.py"
SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_script_module():
    spec = spec_from_file_location("placeholder_validator", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_repository(root: Path, mode: str, policy: str, registered: list[str]) -> None:
    project = {
        "repository_mode": mode,
        "placeholder_register": "repository-placeholder-register.json",
    }
    register = {
        "repository_mode": mode,
        "placeholder_policy": policy,
        "registered_placeholder_paths": registered,
        "ignored_generated_path_patterns": [],
    }
    if mode == "reference-sample":
        project["_sample_comment"] = SAMPLE_MARKER
        register["_sample_comment"] = SAMPLE_MARKER
    write_json(root / "author-lab-project-manifest.json", project)
    write_json(root / "repository-placeholder-register.json", register)


def test_current_repository_placeholder_policy_passes():
    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_reference_sample_requires_markers_on_all_managed_text_files(tmp_path):
    module = load_script_module()
    prepare_repository(
        tmp_path,
        mode="reference-sample",
        policy="all-managed-text-files",
        registered=[],
    )
    (tmp_path / "README.md").write_text("# Missing marker\n", encoding="utf-8")

    errors = module.validate_placeholders(tmp_path)
    assert "README.md: missing required sample marker" in errors


def test_generated_python_packaging_metadata_is_ignored(tmp_path):
    module = load_script_module()
    prepare_repository(
        tmp_path,
        mode="reference-sample",
        policy="all-managed-text-files",
        registered=[],
    )
    (tmp_path / "README.md").write_text(
        f"# Sample\n\n<!-- {SAMPLE_MARKER} -->\n",
        encoding="utf-8",
    )
    package_metadata = tmp_path / "author_lab_sample_tools.egg-info/PKG-INFO"
    package_metadata.parent.mkdir(parents=True)
    package_metadata.write_text("Generated metadata without marker.\n", encoding="utf-8")

    assert module.validate_placeholders(tmp_path) == []


def test_active_author_lab_allows_markers_only_on_registered_placeholders(tmp_path):
    module = load_script_module()
    prepare_repository(
        tmp_path,
        mode="active-author-lab",
        policy="registered-placeholder-paths-only",
        registered=["unfinished.md"],
    )
    (tmp_path / "unfinished.md").write_text(
        f"# Unfinished\n\n<!-- {SAMPLE_MARKER} -->\n",
        encoding="utf-8",
    )
    (tmp_path / "completed.md").write_text("# Completed\n", encoding="utf-8")

    assert module.validate_placeholders(tmp_path) == []


def test_active_author_lab_rejects_unregistered_marker_and_missing_registered_marker(tmp_path):
    module = load_script_module()
    prepare_repository(
        tmp_path,
        mode="active-author-lab",
        policy="registered-placeholder-paths-only",
        registered=["unfinished.md"],
    )
    (tmp_path / "unfinished.md").write_text("# Marker missing\n", encoding="utf-8")
    (tmp_path / "completed.md").write_text(
        f"# Completed\n\n<!-- {SAMPLE_MARKER} -->\n",
        encoding="utf-8",
    )

    errors = module.validate_placeholders(tmp_path)
    assert "unfinished.md: registered placeholder is missing its marker" in errors
    assert any(
        error.startswith("completed.md: unregistered production file contains sample sentinel")
        for error in errors
    )
