#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from atomic_repository_update import (  # noqa: E402
    promote_staged_directory,
    staged_sibling_directory,
)
from repository_mode_support import (  # noqa: E402
    RepositoryModeContext,
    dump_json,
    load_json,
)


def validate_identifier(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError(
            "Work-item ID must use YYYY-NNN-descriptive-slug."
        )
    return value


def find_manifest_by_id(
    repository_root: Path,
    paths: list[Path],
    id_field: str,
    target_id: str,
) -> tuple[Path, dict[str, Any]]:
    matches: list[tuple[Path, dict[str, Any]]] = []
    for path in paths:
        if not path.is_file():
            continue
        document = load_json(path)
        if document.get(id_field) == target_id:
            matches.append((path, document))
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one {id_field}={target_id!r}; found {len(matches)}"
        )
    return matches[0]


def render_work_item_tree(
    staging_root: Path,
    repository_root: Path,
    context: RepositoryModeContext,
    work_item_id: str,
    derived_author_id: str,
    model_manifest: dict[str, Any],
    runbook_manifest: dict[str, Any],
    runtime_configuration: dict[str, Any],
) -> None:
    required_artifacts = runbook_manifest["required_artifacts"]
    artifact_templates = runbook_manifest["artifact_templates"]
    missing_templates = sorted(set(required_artifacts) - set(artifact_templates))
    if missing_templates:
        raise ValueError(
            f"Runbook {runbook_manifest['runbook_id']} has no templates for: "
            f"{missing_templates}"
        )

    replacements = {
        "sample_marker": (
            "这是一个 sample，文件实质完成后删掉这行注释"
            if context.is_reference_sample
            else ""
        ),
        "work_item_id": work_item_id,
        "derived_author_id": derived_author_id,
        "derived_author_model_id": model_manifest["derived_author_model_id"],
        "derived_author_model_version": model_manifest["model_version"],
        "runbook_id": runbook_manifest["runbook_id"],
        "runbook_version": runbook_manifest["runbook_version"],
        "runtime_adapter_id": runtime_configuration["runtime_adapter_id"],
        "runtime_adapter_version": runtime_configuration["configuration_version"],
    }
    for artifact_name in required_artifacts:
        template_path = repository_root / artifact_templates[artifact_name]
        if not template_path.is_file():
            raise ValueError(f"Artifact template does not exist: {template_path}")
        rendered = context.render_text(
            template_path.read_text(encoding="utf-8"), replacements
        )
        artifact_path = staging_root / artifact_name
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(rendered, encoding="utf-8")

    stage_executions = {
        stage: {"status": "not-started"}
        for stage in [
            *runbook_manifest["required_stages"],
            *runbook_manifest["optional_stages"],
        ]
    }
    stage_executions["intake"] = {"status": "in-progress"}
    state = context.with_json_marker(
        {
            "schema_version": "1.0.0",
            "work_item_id": work_item_id,
            "derived_author_id": derived_author_id,
            "derived_author_model_id": model_manifest["derived_author_model_id"],
            "derived_author_model_version": model_manifest["model_version"],
            "runbook_id": runbook_manifest["runbook_id"],
            "runbook_version": runbook_manifest["runbook_version"],
            "runtime_adapter_id": runtime_configuration["runtime_adapter_id"],
            "runtime_adapter_version": runtime_configuration["configuration_version"],
            "lifecycle_status": "intake",
            "stage_executions": stage_executions,
            "quality_gates": {
                "factual_accuracy": "not-evaluated",
                "persona_and_style": "not-evaluated",
                "editorial_approval": "not-evaluated",
            },
            "publication": None,
            "archive_reason": None,
        }
    )
    (staging_root / "work-item-state.json").write_text(
        dump_json(state), encoding="utf-8"
    )

    runs_root = staging_root / "writing-runs"
    runs_root.mkdir(parents=True, exist_ok=True)
    (runs_root / "README.md").write_text(
        "# Writing Runs\n\n"
        f"{context.markdown_marker()}"
        "Store one immutable `run-*.json` record per execution. Run outputs live "
        "under `writing-runs/<run-id>/`; never overwrite a prior record or output.\n",
        encoding="utf-8",
    )
    if context.is_reference_sample:
        sample_run = context.with_json_marker(
            {
                "run_id": "run-sample-not-run",
                "run_status": "not-run",
                "work_item_id": work_item_id,
                "repository_commit_sha": None,
                "derived_author_model_id": model_manifest[
                    "derived_author_model_id"
                ],
                "derived_author_model_version": model_manifest["model_version"],
                "runbook_id": runbook_manifest["runbook_id"],
                "runbook_version": runbook_manifest["runbook_version"],
                "runtime_adapter_id": runtime_configuration["runtime_adapter_id"],
                "runtime_adapter_version": runtime_configuration[
                    "configuration_version"
                ],
                "model_identifier": None,
                "model_parameters": {},
                "context_budget_tokens": None,
                "tool_permissions": [],
                "started_at": None,
                "completed_at": None,
                "loaded_file_records": [],
                "output_artifacts": [],
                "exit_status": None,
            }
        )
        (runs_root / "run-sample-not-run.json").write_text(
            dump_json(sample_run), encoding="utf-8"
        )


def create_work_item(
    repository_root: Path,
    work_item_id: str,
    derived_author_id: str,
    runbook_id: str,
    runtime_adapter_id: str,
) -> Path:
    context = RepositoryModeContext.from_project(repository_root)
    project = context.project

    persona_paths = [
        repository_root / directory / "derived-author-persona-manifest.json"
        for directory in project.get("derived_author_persona_directories", [])
    ]
    persona_path, persona_manifest = find_manifest_by_id(
        repository_root,
        persona_paths,
        "derived_author_id",
        derived_author_id,
    )
    persona_root = persona_path.parent
    model_manifest = load_json(
        persona_root
        / persona_manifest["author_model_directory"]
        / "derived-author-model-manifest.json"
    )
    if model_manifest.get("derived_author_id") != derived_author_id:
        raise ValueError("Persona model belongs to another derived author")

    runbook_paths = list(
        repository_root.glob(
            "shared-writing-harness/writing-runbooks/*/writing-runbook-manifest.json"
        )
    )
    _, runbook_manifest = find_manifest_by_id(
        repository_root, runbook_paths, "runbook_id", runbook_id
    )
    runtime_paths = list(
        repository_root.glob("runtime-adapters/*/runtime-adapter-configuration.json")
    )
    _, runtime_configuration = find_manifest_by_id(
        repository_root,
        runtime_paths,
        "runtime_adapter_id",
        runtime_adapter_id,
    )

    year = work_item_id[:4]
    work_root = (
        repository_root
        / project["writing_work_items_directory"]
        / f"{year}-writing-work-items"
        / work_item_id
    )
    if work_root.exists():
        raise ValueError(f"Work item already exists: {work_root}")

    with staged_sibling_directory(work_root) as staging_root:
        render_work_item_tree(
            staging_root,
            repository_root,
            context,
            work_item_id,
            derived_author_id,
            model_manifest,
            runbook_manifest,
            runtime_configuration,
        )
        promote_staged_directory(staging_root, work_root)
    return work_root


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a runbook-driven writing work item."
    )
    parser.add_argument("work_item_id", type=validate_identifier)
    parser.add_argument("--derived-author-id", required=True)
    parser.add_argument("--runbook-id", required=True)
    parser.add_argument("--runtime-adapter-id", required=True)
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    work_root = create_work_item(
        repository_root,
        arguments.work_item_id,
        arguments.derived_author_id,
        arguments.runbook_id,
        arguments.runtime_adapter_id,
    )
    print(f"Created runbook-driven writing work item: {work_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
