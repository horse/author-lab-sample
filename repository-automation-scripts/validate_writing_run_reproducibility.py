#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def repository_mode(repository_root: Path) -> str:
    manifest = repository_root / "author-lab-project-manifest.json"
    if not manifest.is_file():
        return "reference-sample"
    return load_json(manifest).get("repository_mode", "reference-sample")


def path_has_traversal(value: str) -> bool:
    path = PurePosixPath(value)
    return path.is_absolute() or ".." in path.parts or value.startswith("/")


def git_commit_exists(repository_root: Path, commit_sha: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit_sha}^{{commit}}"],
        cwd=repository_root,
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def git_blob(repository_root: Path, commit_sha: str, path: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"{commit_sha}:{path}"],
        cwd=repository_root,
        capture_output=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def validate_writing_runs(repository_root: Path) -> list[str]:
    errors: list[str] = []
    seen_run_ids: dict[str, Path] = {}
    mode = repository_mode(repository_root)
    run_paths = sorted(
        repository_root.glob("writing-work-items/**/writing-runs/run-*.json")
    )
    legacy_paths = sorted(
        repository_root.glob("writing-work-items/**/writing-run-manifest.json")
    )
    for path in legacy_paths:
        errors.append(
            f"{path}: legacy single writing-run-manifest.json is no longer allowed"
        )

    for run_path in run_paths:
        run = load_json(run_path)
        work_root = run_path.parent.parent
        state_path = work_root / "work-item-state.json"
        if not state_path.is_file():
            errors.append(f"{run_path}: missing work-item-state.json")
            continue
        state = load_json(state_path)
        run_id = run["run_id"]
        if run_id in seen_run_ids:
            errors.append(
                f"Duplicate run_id {run_id!r}: {seen_run_ids[run_id]} and {run_path}"
            )
        else:
            seen_run_ids[run_id] = run_path

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
            if mode != "reference-sample":
                errors.append(
                    f"Run {run_id} uses not-run sample scaffolding in active-author-lab mode"
                )
            if run.get("repository_commit_sha") is not None:
                errors.append(
                    f"Run {run_id} is not-run but records a repository commit"
                )
            if run.get("started_at") is not None or run.get("completed_at") is not None:
                errors.append(f"Run {run_id} is not-run but records execution timestamps")
            if run.get("exit_status") is not None:
                errors.append(f"Run {run_id} is not-run but records an exit status")
            if run.get("loaded_file_records"):
                errors.append(f"Run {run_id} is not-run but records loaded files")
            if run.get("output_artifacts"):
                errors.append(f"Run {run_id} is not-run but records output artifacts")
            continue

        if run_status not in {"running", "completed", "failed", "cancelled"}:
            errors.append(f"Run {run_id} has unknown run_status {run_status!r}")
            continue
        commit_sha = run.get("repository_commit_sha")
        if not isinstance(commit_sha, str) or not git_commit_exists(
            repository_root, commit_sha
        ):
            errors.append(f"Run {run_id} references unknown repository commit {commit_sha!r}")
            commit_available = False
        else:
            commit_available = True

        for record in run.get("loaded_file_records", []):
            loaded_path = record["path"]
            if path_has_traversal(loaded_path):
                errors.append(
                    f"Run {run_id} loaded path traversal is forbidden: {loaded_path}"
                )
                continue
            if not commit_available:
                continue
            content = git_blob(repository_root, commit_sha, loaded_path)
            if content is None:
                errors.append(
                    f"Run {run_id} loaded file is absent from recorded commit: {loaded_path}"
                )
                continue
            actual_hash = hashlib.sha256(content).hexdigest()
            if record.get("sha256") != actual_hash:
                errors.append(
                    f"Run {run_id} loaded file hash mismatch at recorded commit: "
                    f"{loaded_path}"
                )

        required_prefix = PurePosixPath("writing-runs") / run_id
        for artifact in run.get("output_artifacts", []):
            if path_has_traversal(artifact):
                errors.append(
                    f"Run {run_id} output path traversal is forbidden: {artifact}"
                )
                continue
            artifact_posix = PurePosixPath(artifact)
            if artifact_posix.parts[:2] != required_prefix.parts[:2]:
                errors.append(
                    f"Run {run_id} output artifact must be run-scoped under "
                    f"writing-runs/{run_id}/: {artifact}"
                )
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
    print(
        "Writing run reproducibility validation passed: immutable run history checked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
