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
    if not re.fullmatch(r"experiment-\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError(
            "Experiment ID must use experiment-YYYY-NNN-descriptive-slug."
        )
    return value


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_manifest_by_id(
    repository_root: Path,
    pattern: str,
    id_field: str,
    target_id: str,
) -> tuple[Path, dict[str, Any]]:
    for path in repository_root.glob(pattern):
        document = load_json(path)
        if document.get(id_field) == target_id:
            return path, document
    raise ValueError(f"Could not resolve {id_field}={target_id!r}")


def validate_held_out_uri(value: str) -> str:
    if not value.startswith("evaluator-storage://"):
        raise ValueError("held_out_evaluation_pack_uri must use evaluator-storage://")
    return value


def create_experiment(
    repository_root: Path,
    experiment_id: str,
    runtime_adapter_id: str,
    runbook_id: str,
    source_model_id: str,
    derived_author_b_id: str,
    derived_author_c_id: str,
    held_out_evaluation_pack_uri: str | None = None,
) -> Path:
    project = load_json(repository_root / "author-lab-project-manifest.json")
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

    persona_conditions: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for role, persona_id in (
        ("derived-author-b", derived_author_b_id),
        ("derived-author-c", derived_author_c_id),
    ):
        persona_path, persona = find_manifest_by_id(
            repository_root,
            "derived-author-personas/*/derived-author-persona-manifest.json",
            "derived_author_id",
            persona_id,
        )
        model = load_json(
            persona_path.parent
            / persona["author_model_directory"]
            / "derived-author-model-manifest.json"
        )
        persona_conditions.append((role, persona, model))

    held_out_uri = validate_held_out_uri(
        held_out_evaluation_pack_uri
        or f"evaluator-storage://{project.get('project_id', 'author-lab')}/{experiment_id}/held-out-pack"
    )

    experiment_root = repository_root / experiment_directory / experiment_id
    if experiment_root.exists():
        raise ValueError(f"Experiment already exists: {experiment_root}")

    (experiment_root / "controlled-inputs").mkdir(parents=True)
    (experiment_root / "runtime-run-records").mkdir(parents=True)
    (experiment_root / "failure-cases").mkdir(parents=True)

    runtime_id = runtime["runtime_adapter_id"]
    runbook_identifier = runbook["runbook_id"]
    conditions: list[dict[str, Any]] = [
        {
            "condition_id": "condition-generic-runtime-baseline",
            "condition_role": "generic-runtime-baseline",
            "author_condition": None,
            "runtime_adapter_id": runtime_id,
            "runbook_id": runbook_identifier,
        },
        {
            "condition_id": "condition-source-model-direct-baseline",
            "condition_role": "source-model-direct-baseline",
            "author_condition": source_model["source_author_model_id"],
            "runtime_adapter_id": runtime_id,
            "runbook_id": runbook_identifier,
        },
    ]
    for role, persona, model in persona_conditions:
        conditions.append(
            {
                "condition_id": f"condition-{role}",
                "condition_role": role,
                "author_condition": persona["derived_author_id"],
                "runtime_adapter_id": runtime_id,
                "runbook_id": runbook_identifier,
            }
        )

    manifest = {
        "_sample_comment": SAMPLE_MARKER,
        "experiment_id": experiment_id,
        "experiment_status": "designed",
        "hypothesis_file": "hypothesis.md",
        "controlled_input_directory": "controlled-inputs",
        "conditions": conditions,
        "held_out_evaluation_pack_uri": held_out_uri,
        "runtime_run_records_directory": "runtime-run-records",
        "raw_evaluation_results_file": "raw-evaluation-results.jsonl",
        "aggregate_analysis_file": "aggregate-analysis.json",
        "failure_cases_directory": "failure-cases",
        "conclusion_file": "experiment-conclusion.md",
    }
    write_json(experiment_root / "experiment-manifest.json", manifest)

    (experiment_root / "hypothesis.md").write_text(
        "# Experiment Hypothesis\n\n"
        f"<!-- {SAMPLE_MARKER} -->\n\n"
        "When the brief, research pack, runbook, runtime, model parameters, context budget, and tool permissions are held constant, the two derived-author conditions should remain distinguishable in blinded evaluation while avoiding source-author identity, experience, authority, and distinctive-language leakage.\n",
        encoding="utf-8",
    )
    (experiment_root / "controlled-inputs/README.md").write_text(
        "# Controlled Inputs\n\n"
        f"<!-- {SAMPLE_MARKER} -->\n\n"
        "Record the common brief, research pack, runtime parameters, context budget, tool permissions, and repetition count. Do not place held-out evaluator content here.\n",
        encoding="utf-8",
    )
    (experiment_root / "runtime-run-records/README.md").write_text(
        "# Runtime Run Records\n\n"
        f"<!-- {SAMPLE_MARKER} -->\n\n"
        "Create one immutable run record per condition and repetition, including commit SHA, runtime and runbook versions, model identifier and parameters, loaded file hashes, timestamps, and output paths.\n",
        encoding="utf-8",
    )
    (experiment_root / "failure-cases/README.md").write_text(
        "# Failure Cases\n\n"
        f"<!-- {SAMPLE_MARKER} -->\n\n"
        "Preserve leakage, fabrication, persona collapse, evaluator disagreement, excluded runs, and infrastructure failures with reasons.\n",
        encoding="utf-8",
    )
    (experiment_root / "raw-evaluation-results.jsonl").write_text(
        json.dumps(
            {
                "_sample_comment": SAMPLE_MARKER,
                "evaluation_result_id": "SAMPLE-NOT-RUN",
                "experiment_id": experiment_id,
                "condition_blind_code": "UNASSIGNED",
                "evaluator_id": "UNASSIGNED",
                "status": "not-run",
                "scores": {},
                "notes": [],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    write_json(
        experiment_root / "aggregate-analysis.json",
        {
            "_sample_comment": SAMPLE_MARKER,
            "experiment_id": experiment_id,
            "analysis_status": "not-run",
            "condition_summary": {},
            "evaluator_agreement": None,
            "excluded_run_count": 0,
            "failure_case_count": 0,
            "conclusion_supported": None,
        },
    )
    (experiment_root / "experiment-conclusion.md").write_text(
        "# Experiment Conclusion\n\n"
        f"<!-- {SAMPLE_MARKER} -->\n\n"
        "Status: not run. Do not write a conclusion before raw evaluation results and aggregate analysis exist.\n",
        encoding="utf-8",
    )
    return experiment_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a controlled author-model experiment scaffold.")
    parser.add_argument("experiment_id", type=validate_identifier)
    parser.add_argument("--runtime-adapter-id", required=True)
    parser.add_argument("--runbook-id", required=True)
    parser.add_argument("--source-model-id", required=True)
    parser.add_argument("--derived-author-b-id", required=True)
    parser.add_argument("--derived-author-c-id", required=True)
    parser.add_argument("--held-out-evaluation-pack-uri")
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
    )
    print(f"Created controlled author-model experiment: {experiment_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
