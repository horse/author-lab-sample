# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts/create_new_author_model_experiment.py"
SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_module():
    spec = spec_from_file_location("experiment_condition_pinning", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_repository(root: Path) -> None:
    write_json(
        root / "author-lab-project-manifest.json",
        {
            "project_id": "author-lab-test",
            "repository_mode": "active-author-lab",
            "author_model_experiments_directory": "author-model-experiments",
        },
    )
    write_json(
        root / "runtime-adapters/runtime/runtime-adapter-configuration.json",
        {
            "runtime_adapter_id": "runtime",
            "configuration_version": "1.0.0",
            "context_window_tokens": 10000,
            "tool_capabilities": ["filesystem-read"],
        },
    )
    write_json(
        root / "shared-writing-harness/writing-runbooks/runbook/writing-runbook-manifest.json",
        {"runbook_id": "runbook", "runbook_version": "1.0.0"},
    )
    write_json(
        root / "source-author-models/source-model/source-author-model-manifest.json",
        {
            "source_author_model_id": "source-model",
            "source_author_id": "source-author",
            "model_version": "2.0.0",
        },
    )
    for persona_id, model_id, version in (
        ("derived-b", "derived-b-model", "1.2.0"),
        ("derived-c", "derived-c-model", "3.4.0"),
    ):
        write_json(
            root / f"derived-author-personas/{persona_id}/derived-author-persona-manifest.json",
            {
                "derived_author_id": persona_id,
                "author_model_directory": "derived-author-model",
            },
        )
        write_json(
            root / f"derived-author-personas/{persona_id}/derived-author-model/derived-author-model-manifest.json",
            {
                "derived_author_model_id": model_id,
                "derived_author_id": persona_id,
                "model_version": version,
            },
        )


def test_experiment_conditions_pin_exact_model_ids_and_versions(tmp_path):
    module = load_module()
    prepare_repository(tmp_path)

    experiment_root = module.create_experiment(
        repository_root=tmp_path,
        experiment_id="experiment-2026-001-pinning",
        runtime_adapter_id="runtime",
        runbook_id="runbook",
        source_model_id="source-model",
        derived_author_b_id="derived-b",
        derived_author_c_id="derived-c",
        context_budget_tokens=8000,
        randomness_control="seed-42",
    )

    manifest = json.loads((experiment_root / "experiment-manifest.json").read_text(encoding="utf-8"))
    by_role = {condition["condition_role"]: condition for condition in manifest["conditions"]}
    assert by_role["source-model-direct-baseline"]["author_model_id"] == "source-model"
    assert by_role["source-model-direct-baseline"]["author_model_version"] == "2.0.0"
    assert by_role["derived-author-b"]["persona_id"] == "derived-b"
    assert by_role["derived-author-b"]["author_model_id"] == "derived-b-model"
    assert by_role["derived-author-b"]["author_model_version"] == "1.2.0"
    assert by_role["derived-author-b"]["source_author_model_id"] == "source-model"
    assert by_role["derived-author-b"]["source_author_model_version"] == "2.0.0"
    assert by_role["derived-author-c"]["author_model_id"] == "derived-c-model"
    assert by_role["derived-author-c"]["author_model_version"] == "3.4.0"
    for path in experiment_root.rglob("*"):
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            assert SAMPLE_MARKER not in text
            assert "SAMPLE-NOT-RUN" not in text
    assert (experiment_root / "raw-evaluation-results.jsonl").read_text(encoding="utf-8") == ""


def test_experiment_rejects_same_persona_for_b_and_c(tmp_path):
    module = load_module()
    prepare_repository(tmp_path)

    try:
        module.create_experiment(
            repository_root=tmp_path,
            experiment_id="experiment-2026-002-same-persona",
            runtime_adapter_id="runtime",
            runbook_id="runbook",
            source_model_id="source-model",
            derived_author_b_id="derived-b",
            derived_author_c_id="derived-b",
            context_budget_tokens=8000,
            randomness_control="seed-42",
        )
    except ValueError as exc:
        assert "distinct" in str(exc)
    else:
        raise AssertionError("Expected identical B/C personas to be rejected")
