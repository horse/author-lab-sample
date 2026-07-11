#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Iterable

REQUIRED_EXPERIMENT_ROLES = {
    "generic-runtime-baseline",
    "source-model-direct-baseline",
    "derived-author-b",
    "derived-author-c",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    if not path.is_file():
        return
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def validate_source_layers(
    repository_root: Path,
    project: dict[str, Any],
    errors: list[str],
) -> tuple[dict[str, Path], dict[str, tuple[str, dict[str, Any]]]]:
    source_authors: dict[str, Path] = {}
    source_records: dict[str, tuple[str, dict[str, Any]]] = {}
    rights_records: dict[str, dict[str, Any]] = {}

    for directory in project.get("source_author_directories", []):
        author_root = repository_root / directory
        profile_path = author_root / "source-author-profile.json"
        if not profile_path.is_file():
            errors.append(f"Source author directory lacks profile: {directory}")
            continue
        profile = load_json(profile_path)
        source_author_id = profile["source_author_id"]
        if source_author_id in source_authors:
            errors.append(f"Duplicate source_author_id: {source_author_id}")
        source_authors[source_author_id] = author_root

        corpus_manifest_path = author_root / profile["corpus_manifest"]
        corpus_root = corpus_manifest_path.parent
        for record in load_jsonl(corpus_manifest_path):
            source_id = record["source_id"]
            if source_id in source_records:
                errors.append(f"Duplicate source_id: {source_id}")
            source_records[source_id] = (source_author_id, record)
            normalized_path = corpus_root / record["normalized_text"]
            location_map_path = corpus_root / record["segment_location_map"]
            if not normalized_path.is_file():
                errors.append(f"Source {source_id} normalized text does not exist")
            if not location_map_path.is_file():
                errors.append(f"Source {source_id} segment location map does not exist")
            else:
                normalized_text = (
                    normalized_path.read_text(encoding="utf-8")
                    if normalized_path.is_file()
                    else ""
                )
                seen_segment_ids: set[str] = set()
                for segment in load_jsonl(location_map_path):
                    segment_id = segment["segment_id"]
                    if segment_id in seen_segment_ids:
                        errors.append(
                            f"Duplicate segment_id in {location_map_path}: {segment_id}"
                        )
                    seen_segment_ids.add(segment_id)
                    if segment["source_id"] != source_id:
                        errors.append(f"Segment {segment_id} references wrong source_id")
                    if segment["edition_id"] != record["edition_id"]:
                        errors.append(f"Segment {segment_id} references wrong edition_id")
                    if segment["segmentation_version"] != record["segmentation_version"]:
                        errors.append(
                            f"Segment {segment_id} references wrong segmentation_version"
                        )
                    if segment_id not in normalized_text:
                        errors.append(f"Segment ID absent from normalized text: {segment_id}")

        for record in load_jsonl(author_root / profile["rights_register"]):
            source_id = record["source_id"]
            if source_id in rights_records:
                errors.append(f"Duplicate rights record for source_id: {source_id}")
            rights_records[source_id] = record

    storage_records: dict[str, dict[str, Any]] = {}
    for record in load_jsonl(
        repository_root / project["source_material_storage_register"]
    ):
        source_id = record["source_id"]
        if source_id in storage_records:
            errors.append(f"Duplicate storage record for source_id: {source_id}")
        storage_records[source_id] = record
        if record["source_author_id"] not in source_authors:
            errors.append(f"Storage record {source_id} references unknown source author")
        if source_id not in source_records:
            errors.append(f"Storage record references unknown source_id: {source_id}")

    for source_id, (source_author_id, corpus_record) in source_records.items():
        rights_record = rights_records.get(source_id)
        storage_record = storage_records.get(source_id)
        if rights_record is None:
            errors.append(f"Source {source_id} has no rights record")
        if storage_record is None:
            errors.append(f"Source {source_id} has no storage and ingestion record")
            continue
        if storage_record["source_author_id"] != source_author_id:
            errors.append(f"Source {source_id} storage record has wrong source author")
        for field in ("storage_uri", "rights_status", "segmentation_version"):
            if storage_record.get(field) != corpus_record.get(field):
                errors.append(f"Source {source_id} corpus and storage {field} do not match")
        if rights_record is not None:
            for field in ("storage_uri", "rights_status"):
                if rights_record.get(field) != corpus_record.get(field):
                    errors.append(f"Source {source_id} rights and corpus {field} do not match")

    return source_authors, source_records


def validate_models_and_personas(
    repository_root: Path,
    project: dict[str, Any],
    source_authors: dict[str, Path],
    errors: list[str],
) -> tuple[
    dict[str, tuple[str, str, Path]],
    dict[str, tuple[dict[str, Any], dict[str, Any], Path]],
    dict[str, tuple[str, str]],
]:
    source_models: dict[str, tuple[str, str, Path]] = {}
    for directory in project.get("source_author_model_directories", []):
        model_root = repository_root / directory
        manifest = load_json(model_root / "source-author-model-manifest.json")
        model_id = manifest["source_author_model_id"]
        if model_id in source_models:
            errors.append(f"Duplicate source_author_model_id: {model_id}")
        source_author_id = manifest["source_author_id"]
        if source_author_id not in source_authors:
            errors.append(f"Source model {model_id} references unknown source author")
        source_models[model_id] = (
            manifest["model_version"],
            source_author_id,
            model_root,
        )

    personas: dict[str, tuple[dict[str, Any], dict[str, Any], Path]] = {}
    persona_models: dict[str, tuple[str, str]] = {}
    declared_persona_paths: set[str] = set()
    for directory in project.get("derived_author_persona_directories", []):
        if directory in declared_persona_paths:
            errors.append(f"Duplicate persona directory in project manifest: {directory}")
        declared_persona_paths.add(directory)
        persona_root = repository_root / directory
        manifest_path = persona_root / "derived-author-persona-manifest.json"
        if not manifest_path.is_file():
            errors.append(f"Declared persona directory has no manifest: {directory}")
            continue
        persona_manifest = load_json(manifest_path)
        persona_id = persona_manifest["derived_author_id"]
        if persona_id in personas:
            errors.append(f"Duplicate derived_author_id: {persona_id}")
        lineage = load_json(persona_root / persona_manifest["lineage_file"])
        if lineage["derived_author_id"] != persona_id:
            errors.append(f"Persona {persona_id} lineage uses the wrong derived_author_id")
        for source_model in lineage.get("source_models", []):
            model_id = source_model["source_author_model_id"]
            if model_id == "editorial-original-design":
                continue
            if model_id not in source_models:
                errors.append(f"Persona {persona_id} references unknown source model {model_id}")
                continue
            if source_model["source_author_model_version"] != source_models[model_id][0]:
                errors.append(f"Persona {persona_id} references wrong source model version")

        model_root = persona_root / persona_manifest["author_model_directory"]
        model_manifest = load_json(model_root / "derived-author-model-manifest.json")
        model_id = model_manifest["derived_author_model_id"]
        if model_manifest["derived_author_id"] != persona_id:
            errors.append(f"Persona model {model_id} references wrong persona")
        if model_id in persona_models:
            errors.append(f"Duplicate derived_author_model_id: {model_id}")
        personas[persona_id] = (persona_manifest, model_manifest, persona_root)
        persona_models[model_id] = (model_manifest["model_version"], persona_id)

    for manifest_path in repository_root.glob(
        "derived-author-personas/*/derived-author-persona-manifest.json"
    ):
        relative_root = manifest_path.parent.relative_to(repository_root).as_posix()
        if relative_root not in declared_persona_paths:
            errors.append(
                f"Persona exists but is not registered in project manifest: {relative_root}"
            )

    return source_models, personas, persona_models


def validate_policies_runbooks_and_runtimes(
    repository_root: Path,
    project: dict[str, Any],
    errors: list[str],
) -> tuple[
    set[str],
    dict[str, tuple[str, dict[str, Any]]],
    dict[str, tuple[str, dict[str, Any]]],
]:
    policy_ids: set[str] = set()
    for rule in load_jsonl(repository_root / project["policy_rule_register"]):
        policy_id = rule["policy_rule_id"]
        if policy_id in policy_ids:
            errors.append(f"Duplicate policy_rule_id: {policy_id}")
        policy_ids.add(policy_id)
        if not (repository_root / rule["policy_file"]).is_file():
            errors.append(f"Policy rule {policy_id} references a missing policy file")

    runbooks: dict[str, tuple[str, dict[str, Any]]] = {}
    for path in repository_root.glob(
        "shared-writing-harness/writing-runbooks/*/writing-runbook-manifest.json"
    ):
        manifest = load_json(path)
        runbook_id = manifest["runbook_id"]
        if runbook_id in runbooks:
            errors.append(f"Duplicate runbook_id: {runbook_id}")
        runbooks[runbook_id] = (manifest["runbook_version"], manifest)
        if set(manifest["required_artifacts"]) != set(manifest["artifact_templates"]):
            errors.append(f"Runbook {runbook_id} artifacts and templates differ")
        for template_path in manifest["artifact_templates"].values():
            if not (repository_root / template_path).is_file():
                errors.append(
                    f"Runbook {runbook_id} references missing template {template_path}"
                )
        for policy_id in manifest["required_policy_rule_ids"]:
            if policy_id not in policy_ids:
                errors.append(f"Runbook {runbook_id} references unknown policy {policy_id}")

    runtimes: dict[str, tuple[str, dict[str, Any]]] = {}
    for path in repository_root.glob(
        "runtime-adapters/*/runtime-adapter-configuration.json"
    ):
        configuration = load_json(path)
        runtime_id = configuration["runtime_adapter_id"]
        if runtime_id in runtimes:
            errors.append(f"Duplicate runtime_adapter_id: {runtime_id}")
        runtimes[runtime_id] = (configuration["configuration_version"], configuration)
    return policy_ids, runbooks, runtimes


def validate_work_items(
    repository_root: Path,
    personas: dict[str, tuple[dict[str, Any], dict[str, Any], Path]],
    persona_models: dict[str, tuple[str, str]],
    runbooks: dict[str, tuple[str, dict[str, Any]]],
    runtimes: dict[str, tuple[str, dict[str, Any]]],
    errors: list[str],
) -> dict[str, tuple[dict[str, Any], Path]]:
    work_items: dict[str, tuple[dict[str, Any], Path]] = {}
    for path in repository_root.glob("writing-work-items/**/work-item-state.json"):
        state = load_json(path)
        work_item_id = state["work_item_id"]
        if work_item_id in work_items:
            errors.append(f"Duplicate work_item_id: {work_item_id}")
        work_items[work_item_id] = (state, path.parent)
        persona_id = state["derived_author_id"]
        if persona_id not in personas:
            errors.append(f"Work item {work_item_id} references unknown persona")
        model_id = state["derived_author_model_id"]
        if model_id not in persona_models:
            errors.append(f"Work item {work_item_id} references unknown persona model")
        else:
            version, model_persona_id = persona_models[model_id]
            if model_persona_id != persona_id:
                errors.append(f"Work item {work_item_id} model belongs to another persona")
            if state["derived_author_model_version"] != version:
                errors.append(f"Work item {work_item_id} references wrong model version")

        runbook_id = state["runbook_id"]
        if runbook_id not in runbooks:
            errors.append(f"Work item {work_item_id} references unknown runbook")
        else:
            runbook_version, runbook_manifest = runbooks[runbook_id]
            if state["runbook_version"] != runbook_version:
                errors.append(f"Work item {work_item_id} references wrong runbook version")
            for artifact in runbook_manifest["required_artifacts"]:
                if not (path.parent / artifact).is_file():
                    errors.append(f"Work item {work_item_id} is missing artifact {artifact}")
            expected_stages = set(runbook_manifest["required_stages"]) | set(
                runbook_manifest["optional_stages"]
            )
            missing_stages = expected_stages - set(state["stage_executions"])
            if missing_stages:
                errors.append(
                    f"Work item {work_item_id} is missing stages {sorted(missing_stages)}"
                )

        runtime_id = state["runtime_adapter_id"]
        if runtime_id not in runtimes:
            errors.append(f"Work item {work_item_id} references unknown runtime")
        elif state["runtime_adapter_version"] != runtimes[runtime_id][0]:
            errors.append(f"Work item {work_item_id} references wrong runtime version")
        if not (path.parent / "writing-runs").is_dir():
            errors.append(f"Work item {work_item_id} has no writing-runs directory")
    return work_items


def validate_components(
    repository_root: Path,
    project: dict[str, Any],
    errors: list[str],
) -> None:
    register = load_json(repository_root / project["component_status_register"])
    component_ids: set[str] = set()
    component_paths: set[str] = set()
    for component in register["components"]:
        component_id = component["component_id"]
        component_path = component["path"]
        if component_id in component_ids:
            errors.append(f"Duplicate component_id: {component_id}")
        component_ids.add(component_id)
        if component_path in component_paths and component["component_class"] != "example":
            errors.append(f"Duplicate non-example component path: {component_path}")
        component_paths.add(component_path)
        if not (repository_root / component_path).exists():
            errors.append(f"Component path does not exist: {component_path}")
    for persona_directory in project.get("derived_author_persona_directories", []):
        if persona_directory not in component_paths and not any(
            path == "derived-author-personas" for path in component_paths
        ):
            errors.append(
                f"Persona directory has no component registration: {persona_directory}"
            )


def validate_publications(
    repository_root: Path,
    project: dict[str, Any],
    work_items: dict[str, tuple[dict[str, Any], Path]],
    errors: list[str],
) -> list[dict[str, Any]]:
    manifest_path = (
        repository_root
        / project["approved_publications_directory"]
        / "approved-publication-manifest.jsonl"
    )
    publication_ids: set[str] = set()
    publications: list[dict[str, Any]] = []
    for publication in load_jsonl(manifest_path):
        publications.append(publication)
        publication_id = publication["publication_id"]
        if publication_id in publication_ids:
            errors.append(f"Duplicate publication_id: {publication_id}")
        publication_ids.add(publication_id)
        work_item_id = publication["work_item_id"]
        if work_item_id not in work_items:
            errors.append(f"Publication {publication_id} references unknown work item")
            continue
        state, _ = work_items[work_item_id]
        for field in (
            "derived_author_id",
            "derived_author_model_id",
            "derived_author_model_version",
        ):
            if publication[field] != state[field]:
                errors.append(f"Publication {publication_id} has mismatched {field}")
        if publication["publication_status"] in {"approved", "published"}:
            canonical_file = publication["canonical_file"]
            if not canonical_file or not (repository_root / canonical_file).is_file():
                errors.append(f"Publication {publication_id} has no valid canonical file")
    return publications


def expected_persona_indexes(
    persona_id: str,
    work_items: dict[str, tuple[dict[str, Any], Path]],
    publications: list[dict[str, Any]],
    repository_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    work_records: list[dict[str, Any]] = []
    for work_item_id, (state, work_root) in work_items.items():
        if state["derived_author_id"] == persona_id:
            work_records.append(
                {
                    "derived_author_id": persona_id,
                    "canonical_work_item_id": work_item_id,
                    "lifecycle_status": state["lifecycle_status"],
                    "canonical_state_file": (
                        work_root / "work-item-state.json"
                    ).relative_to(repository_root).as_posix(),
                }
            )
    publication_records: list[dict[str, Any]] = []
    for publication in publications:
        if publication["derived_author_id"] == persona_id:
            publication_records.append(
                {
                    "derived_author_id": persona_id,
                    "canonical_publication_id": publication["publication_id"],
                    "work_item_id": publication["work_item_id"],
                    "publication_status": publication["publication_status"],
                    "canonical_file": publication["canonical_file"],
                }
            )
    return (
        sorted(work_records, key=lambda item: item["canonical_work_item_id"]),
        sorted(publication_records, key=lambda item: item["canonical_publication_id"]),
    )


def strip_sample_fields(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in record.items() if key != "_sample_comment"}
        for record in records
        if record.get("index_status") != "generated-empty"
    ]


def validate_persona_indexes(
    repository_root: Path,
    personas: dict[str, tuple[dict[str, Any], dict[str, Any], Path]],
    work_items: dict[str, tuple[dict[str, Any], Path]],
    publications: list[dict[str, Any]],
    errors: list[str],
) -> None:
    for persona_id, (manifest, _, persona_root) in personas.items():
        expected_work, expected_publications = expected_persona_indexes(
            persona_id, work_items, publications, repository_root
        )
        work_index_path = (
            persona_root
            / manifest["work_items_directory"]
            / "derived-author-work-item-index.jsonl"
        )
        publication_index_path = (
            persona_root
            / manifest["publications_directory"]
            / "derived-author-publication-index.jsonl"
        )
        actual_work = strip_sample_fields(load_jsonl(work_index_path))
        actual_publications = strip_sample_fields(load_jsonl(publication_index_path))
        if actual_work != expected_work:
            errors.append(f"Persona {persona_id} work-item index is stale")
        if actual_publications != expected_publications:
            errors.append(f"Persona {persona_id} publication index is stale")


def validate_experiments(
    repository_root: Path,
    source_models: dict[str, tuple[str, str, Path]],
    personas: dict[str, tuple[dict[str, Any], dict[str, Any], Path]],
    runbooks: dict[str, tuple[str, dict[str, Any]]],
    runtimes: dict[str, tuple[str, dict[str, Any]]],
    errors: list[str],
) -> None:
    experiment_ids: set[str] = set()
    for path in repository_root.glob(
        "author-model-experiments/**/experiment-manifest.json"
    ):
        experiment = load_json(path)
        experiment_id = experiment["experiment_id"]
        if experiment_id in experiment_ids:
            errors.append(f"Duplicate experiment_id: {experiment_id}")
        experiment_ids.add(experiment_id)
        controlled = experiment["controlled_execution"]
        runtime_id = controlled["runtime_adapter_id"]
        runbook_id = controlled["runbook_id"]
        if runtime_id not in runtimes:
            errors.append(f"Experiment {experiment_id} references unknown runtime")
        elif controlled["runtime_adapter_version"] != runtimes[runtime_id][0]:
            errors.append(f"Experiment {experiment_id} references wrong runtime version")
        if runbook_id not in runbooks:
            errors.append(f"Experiment {experiment_id} references unknown runbook")
        elif controlled["runbook_version"] != runbooks[runbook_id][0]:
            errors.append(f"Experiment {experiment_id} references wrong runbook version")

        roles: list[str] = []
        condition_ids: list[str] = []
        derived_personas: dict[str, str] = {}
        for condition in experiment["conditions"]:
            role = condition["condition_role"]
            condition_id = condition["condition_id"]
            roles.append(role)
            condition_ids.append(condition_id)
            persona_id = condition["persona_id"]
            model_id = condition["author_model_id"]
            model_version = condition["author_model_version"]
            source_model_id = condition["source_author_model_id"]
            source_model_version = condition["source_author_model_version"]
            if role == "generic-runtime-baseline":
                if any(
                    value is not None
                    for value in (
                        persona_id,
                        model_id,
                        model_version,
                        source_model_id,
                        source_model_version,
                    )
                ):
                    errors.append(
                        f"Experiment {experiment_id} generic baseline loads author data"
                    )
            elif role == "source-model-direct-baseline":
                if persona_id is not None or model_id not in source_models:
                    errors.append(
                        f"Experiment {experiment_id} has invalid source-model baseline"
                    )
                elif (
                    model_version != source_models[model_id][0]
                    or source_model_id != model_id
                    or source_model_version != source_models[model_id][0]
                ):
                    errors.append(
                        f"Experiment {experiment_id} source-model baseline version drift"
                    )
            elif role in {"derived-author-b", "derived-author-c"}:
                if persona_id not in personas:
                    errors.append(
                        f"Experiment {experiment_id} references unknown persona {persona_id}"
                    )
                    continue
                _, persona_model, _ = personas[persona_id]
                if (
                    model_id != persona_model["derived_author_model_id"]
                    or model_version != persona_model["model_version"]
                ):
                    errors.append(
                        f"Experiment {experiment_id} {role} model version drift"
                    )
                if source_model_id not in source_models:
                    errors.append(
                        f"Experiment {experiment_id} {role} references unknown source model"
                    )
                elif source_model_version != source_models[source_model_id][0]:
                    errors.append(
                        f"Experiment {experiment_id} {role} source-model version drift"
                    )
                derived_personas[role] = persona_id
        if len(roles) != len(set(roles)):
            errors.append(f"Experiment {experiment_id} has duplicate condition roles")
        if len(condition_ids) != len(set(condition_ids)):
            errors.append(f"Experiment {experiment_id} has duplicate condition IDs")
        missing_roles = REQUIRED_EXPERIMENT_ROLES - set(roles)
        if missing_roles:
            errors.append(
                f"Experiment {experiment_id} is missing conditions {sorted(missing_roles)}"
            )
        if (
            derived_personas.get("derived-author-b")
            == derived_personas.get("derived-author-c")
        ):
            errors.append(f"Experiment {experiment_id} B and C must be distinct personas")
        if not experiment["held_out_evaluation_pack_uri"].startswith(
            "evaluator-storage://"
        ):
            errors.append(f"Experiment {experiment_id} uses writer-readable held-out storage")

        experiment_root = path.parent
        for field in (
            "hypothesis_file",
            "raw_evaluation_results_file",
            "aggregate_analysis_file",
            "conclusion_file",
        ):
            if not (experiment_root / experiment[field]).is_file():
                errors.append(f"Experiment {experiment_id} missing file declared by {field}")
        for field in (
            "controlled_input_directory",
            "runtime_run_records_directory",
            "failure_cases_directory",
        ):
            if not (experiment_root / experiment[field]).is_dir():
                errors.append(
                    f"Experiment {experiment_id} missing directory declared by {field}"
                )


def validate_repository_cross_references(repository_root: Path) -> list[str]:
    project = load_json(repository_root / "author-lab-project-manifest.json")
    errors: list[str] = []
    source_authors, _ = validate_source_layers(repository_root, project, errors)
    source_models, personas, persona_models = validate_models_and_personas(
        repository_root, project, source_authors, errors
    )
    _, runbooks, runtimes = validate_policies_runbooks_and_runtimes(
        repository_root, project, errors
    )
    work_items = validate_work_items(
        repository_root,
        personas,
        persona_models,
        runbooks,
        runtimes,
        errors,
    )
    validate_components(repository_root, project, errors)
    publications = validate_publications(
        repository_root, project, work_items, errors
    )
    validate_persona_indexes(
        repository_root, personas, work_items, publications, errors
    )
    validate_experiments(
        repository_root,
        source_models,
        personas,
        runbooks,
        runtimes,
        errors,
    )
    return errors


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    errors = validate_repository_cross_references(repository_root)
    if errors:
        print("Repository cross-reference validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Repository cross-reference validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
