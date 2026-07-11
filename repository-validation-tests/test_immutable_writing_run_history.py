# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import hashlib
import json
from pathlib import Path
import subprocess

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts/validate_writing_run_reproducibility.py"


def load_module():
    spec = spec_from_file_location("immutable_run_history", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def state_document() -> dict:
    return {
        "work_item_id": "2026-001-test",
        "derived_author_model_id": "derived-model",
        "derived_author_model_version": "1.0.0",
        "runbook_id": "runbook",
        "runbook_version": "1.0.0",
        "runtime_adapter_id": "runtime",
        "runtime_adapter_version": "1.0.0",
    }


def run_document(run_id: str, commit_sha: str, path: str, digest: str) -> dict:
    return {
        "run_id": run_id,
        "work_item_id": "2026-001-test",
        "derived_author_model_id": "derived-model",
        "derived_author_model_version": "1.0.0",
        "runbook_id": "runbook",
        "runbook_version": "1.0.0",
        "runtime_adapter_id": "runtime",
        "runtime_adapter_version": "1.0.0",
        "run_status": "completed",
        "repository_commit_sha": commit_sha,
        "loaded_file_records": [{"path": path, "sha256": digest}],
        "output_artifacts": [f"writing-runs/{run_id}/draft.md"],
        "started_at": "2026-07-11T12:00:00+09:00",
        "completed_at": "2026-07-11T12:01:00+09:00",
        "exit_status": 0,
    }


def initialize_git_repository(root: Path) -> str:
    subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-m", "baseline"], cwd=root, check=True, capture_output=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def test_multiple_run_files_are_discovered_and_duplicate_ids_fail(tmp_path):
    module = load_module()
    work_root = tmp_path / "writing-work-items/2026-writing-work-items/2026-001-test"
    write_json(work_root / "work-item-state.json", state_document())
    for filename in ("run-001.json", "run-duplicate.json"):
        write_json(
            work_root / "writing-runs" / filename,
            {
                **run_document("run-001", "0" * 40, "README.md", "0" * 64),
                "run_status": "not-run",
                "repository_commit_sha": None,
                "loaded_file_records": [],
                "output_artifacts": [],
                "started_at": None,
                "completed_at": None,
                "exit_status": None,
            },
        )

    errors = module.validate_writing_runs(tmp_path)

    assert any("Duplicate run_id" in error for error in errors)


def test_historical_hash_is_checked_against_recorded_commit_not_current_head(tmp_path):
    module = load_module()
    (tmp_path / "README.md").write_text("old content\n", encoding="utf-8")
    work_root = tmp_path / "writing-work-items/2026-writing-work-items/2026-001-test"
    write_json(work_root / "work-item-state.json", state_document())
    output = work_root / "writing-runs/run-001/draft.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("draft\n", encoding="utf-8")
    commit_sha = initialize_git_repository(tmp_path)
    digest = hashlib.sha256(b"old content\n").hexdigest()
    (tmp_path / "README.md").write_text("new content\n", encoding="utf-8")
    write_json(work_root / "writing-runs/run-001.json", run_document("run-001", commit_sha, "README.md", digest))

    errors = module.validate_writing_runs(tmp_path)

    assert errors == []


def test_unknown_commit_and_path_traversal_are_rejected(tmp_path):
    module = load_module()
    work_root = tmp_path / "writing-work-items/2026-writing-work-items/2026-001-test"
    write_json(work_root / "work-item-state.json", state_document())
    output = work_root / "writing-runs/run-001/draft.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("draft\n", encoding="utf-8")
    write_json(
        work_root / "writing-runs/run-001.json",
        run_document("run-001", "f" * 40, "../secret.txt", "0" * 64),
    )

    errors = module.validate_writing_runs(tmp_path)

    assert any("unknown repository commit" in error for error in errors)
    assert any("path traversal" in error for error in errors)
