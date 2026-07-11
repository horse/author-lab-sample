#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def validate_identifier(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Work-item ID must use YYYY-NNN-descriptive-slug.")
    return value


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_manifest_by_id(repository_root: Path, pattern: str, id_field: str, target_id: str) -> tuple[Path, dict[str, Any]]:
    for path in repository_root.glob(pattern):
        document = load_json(path)
        if document.get(id_field) == target_id:
            return path, document
    raise SystemExit(f"Could not resolve {id_field}={target_id!r} using {pattern}")


def render_template(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = re.findall(r"\{\{[a-zA-Z0-9_-]+\}\}", text)
    if unresolved:
        raise SystemExit(f"Unresolved template variables: {sorted(set(unresolved))}")
    return text


def create_work_item(
    repository_root: Path,
    work_item_id: str,
    derived_author_id: str,
    runbook_id: str,
    runtime_adapter_id: str,
) -> Path:
    project = load_json(repository_root / "author-lab-project-manifest.json")

    persona_path, persona_manifest = find_manifest_by_id(
        repository_root,
        "derived-author-personas/*/derived-author-persona-manifest.json",
        "derived_author_id",
        derived_author_id,
    )
    persona_root = persona_path.parent
    model_manifest = load_json(
        persona_root
        / persona_manifest["author_model_directory"]
        / "derived-author-model-manifest.json"
    )

    _, runbook_manifest = find_manifest_by_id(
        repository_root,
        "shared-writing-harness/writing-runbooks/*/writing-runbook-manifest.json",
        "runbook_id",
        runbook_id,
    )
    _, runtime_configuration = find_manifest_by_id(
        repository_root,
        "runtime-adapters/*/runtime-adapter-configuration.json",
        "runtime_adapter_id",
        runtime_adapter_id,
    )

    required_artifacts = runbook_manifest["required_artifacts"]
    artifact_templates = runbook_manifest["artifact_templates"]
    missing_templates = sorted(set(required_artifacts) - set(artifact_templates))
    if missing_templates:
        raise SystemExit(f"Runbook {runbook_id} has no templates for: {missing_templates}")

    year = work_item_id[:4]
    work_root = (
        repository_root
        / project["writing_work_items_directory"]
        / f"{year}-writing-work-items"
        / work_item_id
    )
    if work_root.exists():
        raise SystemExit(f"Work item already exists: {work_root}")
    work_root.mkdir(parents=True)

    replacements = {
        "sample_marker": SAMPLE_MARKER,
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
            raise SystemExit(f"Artifact template does not exist: {template_path}")
        rendered = render_template(template_path.read_text(encoding="utf-8"), replacements)
        (work_root / artifact_name).write_text(rendered, encoding="utf-8")

    stage_executions = {
        stage: {"status": "not-started"}
        for stage in [*runbook_manifest["required_stages"], *runbook_manifest["optional_stages"]]
    }
    stage_executions["intake"] = {"status": "in-progress"}

    state = {
        "_sample_comment": SAMPLE_MARKER,
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
    }
    (work_root / "work-item-state.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return work_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a runbook-driven writing work item.")
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
