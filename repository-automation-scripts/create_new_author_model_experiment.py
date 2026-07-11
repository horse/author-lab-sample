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
    if not re.fullmatch(
        r"experiment-\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", value
    ):
        raise argparse.ArgumentTypeError(
            "Experiment ID must use experiment-YYYY-NNN-descriptive-slug."
        )
    return value


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_json(document), encoding="utf-8")


def find_manifest_by_id(
    repository_root: Path,
    pattern: str,
    id_field: str,
    target_id: str,
) -> tuple[Path, dict[str, Any]]:
    matches: list[tuple[Path, dict[str, Any]]] = []
    for path in repository_root.glob(pattern):
        document = load_json(path)
        if document.get(id_field) == target_id:
            matches.append((path, document))
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one {id_field}={target_id!r}; found {len(matches)}"
        )
    return matches[0]


def validate_held_out_uri(value: str) -> str:
    if not value.startswith("evaluator-storage://"):
        raise ValueError("held_out_evaluation_pack_uri must use evaluator-storage://")
    return value


def resolve_persona_condition(
    repository_root: Path,
    role: str,
    persona_id: str,
    source_model: dict[str, Any],
) -> dict[str, Any]:
    persona_path, persona = find_manifest_by_id(
        repository_root,
        "derived-author-personas/*/derived-author-persona-manifest.json",
        "derived_author_id",
        persona_id,
    )
    persona_root = persona_path.parent
    model = load_json(
        persona_root
        / persona["author_model_directory"]
        / "derived-author-model-manifest.json"
    )
    if model.get("derived_author_id") != persona_id:
        raise ValueError(f"Persona {persona_id} model belongs to another persona")

    lineage_path = persona_root / persona.get("lineage_file", "derived-author-lineage.json")
    if lineage_path.is_file():
        lineage = load_json(lineage_path)
        matching_lineage = [
            item
            for item in lineage.get("source_models", [])
            if item.get("source_author_model_id")
            == source_model["source_author_model_id"]
            and item.get("source_author_model_version")
            == source_model["model_version"]
        ]
        if not matching_lineage:
            raise ValueError(
                f"Persona {persona_id} lineage does not pin source model "
                f"{source_model['source_author_model_id']}@{source_model['model_version']}"
            )

    return {
        "condition_id": f"condition-{role}",
        "condition_role": role,
        "persona_id": persona_id,
        "author_model_id": model["derived_author_model_id"],
        "author_model_version": model["model_version"],
        "source_author_model_id": source_model["source_author_model_id"],
        "source_author_model_version": source_model["model_version"],
    }


def render_experiment_tree(
    root: Path,
    context: RepositoryModeContext,
    manifest: dict[str, Any],
) -> None:
    (root / "controlled-inputs").mkdir(parents=True)
    (root / "runtime-run-records").mkdir(parents=True)
    (root / "failure-cases").mkdir(parents=True)
    write_json(root / "experiment-manifest.json", manifest)

    marker = context.markdown_marker()
    (root / "hypothesis.md").write_text(
        "# Experiment Hypothesis\n\n"
        f"{marker}"
        "When the brief, research pack, runbook, runtime, model parameters, "
        "context budget, tool permissions, and repetition policy are held constant, "
        "the two derived-author conditions should remain distinguishable in blinded "
        "evaluation while avoiding source-author identity, experience, authority, "
        "and distinctive-language leakage.\n",
        encoding="utf-8",
    )
    (root / "controlled-inputs/README.md").write_text(
        "# Controlled Inputs\n\n"
        f"{marker}"
        "Store the common brief, research pack, and task set. Execution controls "
        "are canonical in `experiment-manifest.json`. Do not place held-out "
        "evaluator content here.\n",
        encoding="utf-8",
    )
    (root / "runtime-run-records/README.md").write_text(
        "# Runtime Run Records\n\n"
        f"{marker}"
        "Create one immutable run record per condition and repetition, including "
        "commit SHA, condition ID, runtime and runbook versions, model identifier "
        "and parameters, loaded file hashes, timestamps, exit status, and output paths.\n",
        encoding="utf-8",
    )
    (root / "failure-cases/README.md").write_text(
        "# Failure Cases\n\n"
        f"{marker}"
        "Preserve leakage, fabrication, persona collapse, evaluator disagreement, "
        "excluded runs, and infrastructure failures with reasons.\n",
        encoding="utf-8",
    )

    raw_result = {
        "evaluation_result_id": "SAMPLE-NOT-RUN",
        "experiment_id": manifest["experiment_id"],
        "condition_blind_code": "UNASSIGNED",
        "evaluator_id": "UNASSIGNED",
        "status": "not-run",
        "scores": {},
        "notes": [],
    }
    (root / "raw-evaluation-results.jsonl").write_text(
        context.empty_jsonl(raw_result), encoding="utf-8"
    )
    write_json(
        root / "aggregate-analysis.json",
        context.with_json_marker(
            {
                "experiment_id": manifest["experiment_id"],
                "analysis_status": "not-run",
                "condition_summary": {},
                "evaluator_agreement": None,
                "excluded_run_count": 0,
                "failure_case_count": 0,
                "conclusion_supported": None,
            }
        ),
    )
    (root / "experiment-conclusion.md").write_text(
        "# Experiment Conclusion\n\n"
        f"{marker}"
        "Status: not run. Do not write a conclusion before raw evaluation results "
        "and aggregate analysis exist.\n",
        encoding="utf-8",
    )


def create_experiment(
    repository_root: Path,
    experiment_id: str,
    runtime_adapter_id: str,
    runbook_id: str,
    source_model_id: str,
    derived_author_b_id: str,
    derived_author_c_id: str,
    held_out_evaluation_pack_uri: str | None = None,
    model_parameters: dict[str, Any] | None = None,
    context_budget_tokens: int | None = None,
    tool_permissions: list[str] | None = None,
    repetition_count: int = 3,
    randomness_control: str | None = None,
) -> Path:
    if repetition_count < 1:
        raise ValueError("repetition_count must be at least 1")
    if derived_author_b_id == derived_author_c_id:
        raise ValueError("Derived Author B and C must be distinct personas")

    context = RepositoryModeContext.from_project(repository_root)
    project = context.project
    experiment_directory = project["author_model_experiments_directory"]

    _, runtime = find_manifest_by_id(
        repository_root,
        "runtime-adapters/*/runtime-adapter-configuration.json",
        "runtime_adapter_id",
        runtime_adapter_id,
    )
    _, runbook = find_manifest_by_id(
        repository_root,
        "shared-writing-harness/writing-runbooks/*/writing-runbook-manifest.json",
        "runbook_id",
        runbook_id,
    )
    _, source_model = find_manifest_by_id(
        repository_root,
        "source-author-models/*/source-author-model-manifest.json",
        "source_author_model_id",
        source_model_id,
    )

    conditions: list[dict[str, Any]] = [
        {
            "condition_id": "condition-generic-runtime-baseline",
            "condition_role": "generic-runtime-baseline",
            "persona_id": None,
            "author_model_id": None,
            "author_model_version": None,
            "source_author_model_id": None,
            "source_author_model_version": None,
        },
        {
            "condition_id": "condition-source-model-direct-baseline",
            "condition_role": "source-model-direct-baseline",
            "persona_id": None,
            "author_model_id": source_model["source_author_model_id"],
            "author_model_version": source_model["model_version"],
            "source_author_model_id": source_model["source_author_model_id"],
            "source_author_model_version": source_model["model_version"],
        },
        resolve_persona_condition(
            repository_root, "derived-author-b", derived_author_b_id, source_model
        ),
        resolve_persona_condition(
            repository_root, "derived-author-c", derived_author_c_id, source_model
        ),
    ]

    held_out_uri = validate_held_out_uri(
        held_out_evaluation_pack_uri
        or (
            f"evaluator-storage://{project.get('project_id', 'author-lab')}/"
            f"{experiment_id}/held-out-pack"
        )
    )
    controlled_execution = {
        "runtime_adapter_id": runtime["runtime_adapter_id"],
        "runtime_adapter_version": runtime["configuration_version"],
        "runbook_id": runbook["runbook_id"],
        "runbook_version": runbook["runbook_version"],
        "model_parameters": model_parameters or {},
        "context_budget_tokens": (
            context_budget_tokens
            if context_budget_tokens is not None
            else runtime.get("context_window_tokens")
        ),
        "tool_permissions": (
            tool_permissions
            if tool_permissions is not None
            else list(runtime.get("tool_capabilities", []))
        ),
        "repetition_count": repetition_count,
        "randomness_control": randomness_control,
    }
    manifest = context.with_json_marker(
        {
            "experiment_id": experiment_id,
            "experiment_status": "designed",
            "hypothesis_file": "hypothesis.md",
            "controlled_input_directory": "controlled-inputs",
            "controlled_execution": controlled_execution,
            "conditions": conditions,
            "held_out_evaluation_pack_uri": held_out_uri,
            "runtime_run_records_directory": "runtime-run-records",
            "raw_evaluation_results_file": "raw-evaluation-results.jsonl",
            "aggregate_analysis_file": "aggregate-analysis.json",
            "failure_cases_directory": "failure-cases",
            "conclusion_file": "experiment-conclusion.md",
        }
    )

    experiment_root = repository_root / experiment_directory / experiment_id
    if experiment_root.exists():
        raise ValueError(f"Experiment already exists: {experiment_root}")
    with staged_sibling_directory(experiment_root) as staging_root:
        render_experiment_tree(staging_root, context, manifest)
        promote_staged_directory(staging_root, experiment_root)
    return experiment_root


def parse_json_object(value: str) -> dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError("model parameters must be a JSON object")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a controlled author-model experiment scaffold."
    )
    parser.add_argument("experiment_id", type=validate_identifier)
    parser.add_argument("--runtime-adapter-id", required=True)
    parser.add_argument("--runbook-id", required=True)
    parser.add_argument("--source-model-id", required=True)
    parser.add_argument("--derived-author-b-id", required=True)
    parser.add_argument("--derived-author-c-id", required=True)
    parser.add_argument("--held-out-evaluation-pack-uri")
    parser.add_argument("--model-parameters", type=parse_json_object, default={})
    parser.add_argument("--context-budget-tokens", type=int)
    parser.add_argument("--tool-permission", action="append", dest="tool_permissions")
    parser.add_argument("--repetition-count", type=int, default=3)
    parser.add_argument("--randomness-control")
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    experiment_root = create_experiment(
        repository_root=repository_root,
        experiment_id=arguments.experiment_id,
        runtime_adapter_id=arguments.runtime_adapter_id,
        runbook_id=arguments.runbook_id,
        source_model_id=arguments.source_model_id,
        derived_author_b_id=arguments.derived_author_b_id,
        derived_author_c_id=arguments.derived_author_c_id,
        held_out_evaluation_pack_uri=arguments.held_out_evaluation_pack_uri,
        model_parameters=arguments.model_parameters,
        context_budget_tokens=arguments.context_budget_tokens,
        tool_permissions=arguments.tool_permissions,
        repetition_count=arguments.repetition_count,
        randomness_control=arguments.randomness_control,
    )
    print(f"Created controlled author-model experiment: {experiment_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
