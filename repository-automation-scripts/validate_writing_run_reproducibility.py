#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_writing_runs(repository_root: Path) -> list[str]:
    errors: list[str] = []
    for run_path in repository_root.glob(
        "writing-work-items/**/writing-run-manifest.json"
    ):
        run = load_json(run_path)
        work_root = run_path.parent
        state_path = work_root / "work-item-state.json"
        if not state_path.is_file():
            errors.append(f"{run_path}: missing work-item-state.json")
            continue
        state = load_json(state_path)
        run_id = run["run_id"]

        expected_pairs = (
            ("work_item_id", "work item ID"),
            ("derived_author_model_id", "derived author model ID"),
            ("derived_author_model_version", "derived author model version"),
            ("runbook_id", "runbook ID"),
            ("runbook_version", "runbook version"),
            ("runtime_adapter_id", "runtime adapter ID"),
            ("runtime_adapter_version", "runtime adapter version"),
        )
        for field, description in expected_pairs:
            if run.get(field) != state.get(field):
                errors.append(
                    f"Run {run_id} {description} does not match work-item state"
                )

        run_status = run["run_status"]
        if run_status == "not-run":
            if run.get("repository_commit_sha") is not None:
                errors.append(
                    f"Run {run_id} is not-run but records a repository commit"
                )
            if run.get("started_at") is not None or run.get("completed_at") is not None:
                errors.append(f"Run {run_id} is not-run but records execution timestamps")
            if run.get("exit_status") is not None:
                errors.append(f"Run {run_id} is not-run but records an exit status")
            continue

        if run_status in {"completed", "failed", "cancelled"}:
            for record in run["loaded_file_records"]:
                loaded_path = repository_root / record["path"]
                if not loaded_path.is_file():
                    errors.append(
                        f"Run {run_id} loaded file does not exist: {record['path']}"
                    )
                    continue
                actual_hash = sha256_file(loaded_path)
                if record["sha256"] != actual_hash:
                    errors.append(
                        f"Run {run_id} loaded file hash mismatch: {record['path']}"
                    )
            for artifact in run["output_artifacts"]:
                artifact_path = work_root / artifact
                if not artifact_path.is_file():
                    errors.append(
                        f"Run {run_id} output artifact does not exist: {artifact}"
                    )

    return errors


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    errors = validate_writing_runs(repository_root)
    if errors:
        print("Writing run reproducibility validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Writing run reproducibility validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
