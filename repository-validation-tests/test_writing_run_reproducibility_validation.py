# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import hashlib
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_writing_run_reproducibility.py"


def load_script_module():
    spec = spec_from_file_location("run_validator", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_run(root: Path, *, recorded_hash: str, model_version: str = "1.0.0") -> None:
    loaded_file = root / "derived-author-personas/derived-b/model.md"
    loaded_file.parent.mkdir(parents=True, exist_ok=True)
    loaded_file.write_text("# Loaded model\n", encoding="utf-8")
    output_file = root / "writing-work-items/2026/2026-001-test/draft-01.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("# Draft\n", encoding="utf-8")
    write_json(
        output_file.parent / "work-item-state.json",
        {
            "work_item_id": "2026-001-test",
            "derived_author_model_id": "derived-b-model",
            "derived_author_model_version": "1.0.0",
            "runbook_id": "test-runbook",
            "runbook_version": "1.0.0",
            "runtime_adapter_id": "test-runtime",
            "runtime_adapter_version": "1.0.0",
        },
    )
    write_json(
        output_file.parent / "writing-run-manifest.json",
        {
            "run_id": "RUN-001",
            "run_status": "completed",
            "work_item_id": "2026-001-test",
            "repository_commit_sha": "a" * 40,
            "derived_author_model_id": "derived-b-model",
            "derived_author_model_version": model_version,
            "runbook_id": "test-runbook",
            "runbook_version": "1.0.0",
            "runtime_adapter_id": "test-runtime",
            "runtime_adapter_version": "1.0.0",
            "model_identifier": "test-model",
            "model_parameters": {"temperature": 0.2},
            "context_budget_tokens": 16000,
            "tool_permissions": ["repository-read"],
            "started_at": "2026-07-11T10:00:00+09:00",
            "completed_at": "2026-07-11T10:01:00+09:00",
            "loaded_file_records": [
                {
                    "path": "derived-author-personas/derived-b/model.md",
                    "sha256": recorded_hash,
                }
            ],
            "output_artifacts": ["draft-01.md"],
            "exit_status": 0,
        },
    )


def test_completed_run_with_matching_hash_and_versions_passes(tmp_path):
    module = load_script_module()
    content_hash = hashlib.sha256(b"# Loaded model\n").hexdigest()
    prepare_run(tmp_path, recorded_hash=content_hash)
    assert module.validate_writing_runs(tmp_path) == []


def test_completed_run_rejects_hash_and_model_version_drift(tmp_path):
    module = load_script_module()
    prepare_run(tmp_path, recorded_hash="0" * 64, model_version="2.0.0")
    errors = module.validate_writing_runs(tmp_path)
    assert any("loaded file hash mismatch" in error for error in errors)
    assert any("derived author model version does not match work-item state" in error for error in errors)
