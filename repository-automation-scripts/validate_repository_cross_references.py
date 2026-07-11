#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Iterable


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def validate_repository_cross_references(repository_root: Path) -> list[str]:
    errors: list[str] = []
    project = load_json(repository_root / "author-lab-project-manifest.json")

    source_authors: dict[str, Path] = {}
    source_ids: set[str] = set()
    for directory in project["source_author_directories"]:
        root = repository_root / directory
        profile = load_json(root / "source-author-profile.json")
        source_author_id = profile["source_author_id"]
        if source_author_id in source_authors:
            errors.append(f"Duplicate source_author_id: {source_author_id}")
        source_authors[source_author_id] = root
        for record in load_jsonl(root / profile["corpus_manifest"]):
            source_ids.add(record["source_id"])

    source_models: dict[str, tuple[str, str, Path]] = {}
    for directory in project["source_author_model_directories"]:
        root = repository_root / directory
        manifest = load_json(root / "source-author-model-manifest.json")
        model_id = manifest["source_author_model_id"]
        version = manifest["model_version"]
        source_author_id = manifest["source_author_id"]
        if source_author_id not in source_authors:
            errors.append(f"Source model {model_id} references unknown source author {source_author_id}")
        source_models[model_id] = (version, source_author_id, root)

    personas: dict[str, tuple[dict[str, Any], dict[str, Any], Path]] = {}
    persona_models: dict[str, tuple[str, str]] = {}
    for directory in project["derived_author_persona_directories"]:
        root = repository_root / directory
        persona_manifest = load_json(root / "derived-author-persona-manifest.json")
        persona_id = persona_manifest["derived_author_id"]
        lineage = load_json(root / persona_manifest["lineage_file"])
        if lineage["derived_author_id"] != persona_id:
            errors.append(f"Persona {persona_id} lineage uses derived_author_id={lineage['derived_author_id']}")
        for source_model in lineage.get("source_models", []):
            model_id = source_model["source_author_model_id"]
            if model_id == "editorial-original-design":
                continue
            if model_id not in source_models:
                errors.append(f"Persona {persona_id} references unknown source model {model_id}")
                continue
            expected_version = source_models[model_id][0]
            if source_model["source_author_model_version"] != expected_version:
                errors.append(
                    f"Persona {persona_id} references {model_id} version {source_model['source_author_model_version']} but repository declares {expected_version}"
                )
        model_root = root / persona_manifest["author_model_directory"]
        model_manifest = load_json(model_root / "derived-author-model-manifest.json")
        if model_manifest["derived_author_id"] != persona_id:
            errors.append(f"Persona model {model_manifest['derived_author_model_id']} references wrong persona")
        personas[persona_id] = (persona_manifest, model_manifest, root)
        persona_models[model_manifest["derived_author_model_id"]] = (
            model_manifest["model_version"],
            persona_id,
        )

    runbooks: dict[str, str] = {}
    for path in repository_root.glob("shared-writing-harness/writing-runbooks/*/writing-runbook-manifest.json"):
        manifest = load_json(path)
        runbooks[manifest["runbook_id"]] = manifest["runbook_version"]

    runtimes: dict[str, str] = {}
    for path in repository_root.glob("runtime-adapters/*/runtime-adapter-configuration.json"):
        configuration = load_json(path)
        runtimes[configuration["runtime_adapter_id"]] = configuration["configuration_version"]

    work_items: dict[str, tuple[dict[str, Any], Path]] = {}
    for path in repository_root.glob("writing-work-items/**/work-item-state.json"):
        state = load_json(path)
        work_item_id = state["work_item_id"]
        work_items[work_item_id] = (state, path.parent)
        persona_id = state["derived_author_id"]
        if persona_id not in personas:
            errors.append(f"Work item {work_item_id} references unknown persona {persona_id}")
        model_id = state["derived_author_model_id"]
        if model_id not in persona_models:
            errors.append(f"Work item {work_item_id} references unknown persona model {model_id}")
        else:
            version, model_persona_id = persona_models[model_id]
            if model_persona_id != persona_id:
                errors.append(f"Work item {work_item_id} model {model_id} belongs to {model_persona_id}")
            if state["derived_author_model_version"] != version:
                errors.append(f"Work item {work_item_id} references wrong model version for {model_id}")
        runbook_id = state["runbook_id"]
        if runbook_id not in runbooks:
            errors.append(f"Work item {work_item_id} references unknown runbook {runbook_id}")
        elif state["runbook_version"] != runbooks[runbook_id]:
            errors.append(f"Work item {work_item_id} references wrong runbook version for {runbook_id}")
        runtime_id = state["runtime_adapter_id"]
        if runtime_id not in runtimes:
            errors.append(f"Work item {work_item_id} references unknown runtime {runtime_id}")
        elif state["runtime_adapter_version"] != runtimes[runtime_id]:
            errors.append(f"Work item {work_item_id} references wrong runtime version for {runtime_id}")

    storage_register = repository_root / project["source_material_storage_register"]
    for record in load_jsonl(storage_register):
        if record["source_author_id"] not in source_authors:
            errors.append(f"Storage record {record['source_id']} references unknown source author")
        if record["source_id"] not in source_ids:
            errors.append(f"Storage record references source_id absent from corpus manifests: {record['source_id']}")

    component_register = load_json(repository_root / project["component_status_register"])
    component_ids: set[str] = set()
    for component in component_register["components"]:
        if component["component_id"] in component_ids:
            errors.append(f"Duplicate component_id: {component['component_id']}")
        component_ids.add(component["component_id"])
        if not (repository_root / component["path"]).exists():
            errors.append(f"Component path does not exist: {component['path']}")

    policy_ids: set[str] = set()
    for rule in load_jsonl(repository_root / project["policy_rule_register"]):
        policy_ids.add(rule["policy_rule_id"])
        if not (repository_root / rule["policy_file"]).is_file():
            errors.append(f"Policy rule {rule['policy_rule_id']} references missing file {rule['policy_file']}")

    publication_manifest = repository_root / project["approved_publications_directory"] / "approved-publication-manifest.jsonl"
    for publication in load_jsonl(publication_manifest):
        status = publication["publication_status"]
        if publication.get("work_item_id") not in work_items:
            errors.append(f"Publication {publication['publication_id']} references unknown work item")
        if publication.get("derived_author_id") not in personas:
            errors.append(f"Publication {publication['publication_id']} references unknown persona")
        if status in {"approved", "published"}:
            canonical_file = publication.get("canonical_file", "")
            if not canonical_file or not (repository_root / canonical_file).is_file():
                errors.append(f"Publication {publication['publication_id']} has no valid canonical file")

    for path in repository_root.glob("author-model-experiments/**/experiment-manifest.json"):
        experiment = load_json(path)
        for condition in experiment["conditions"]:
            if condition["runbook_id"] not in runbooks:
                errors.append(f"Experiment {experiment['experiment_id']} references unknown runbook")
            if condition["runtime_adapter_id"] not in runtimes:
                errors.append(f"Experiment {experiment['experiment_id']} references unknown runtime")
        if not experiment["held_out_evaluation_pack_uri"].startswith("evaluator-storage://"):
            errors.append(f"Experiment {experiment['experiment_id']} uses writer-readable held-out storage")

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
