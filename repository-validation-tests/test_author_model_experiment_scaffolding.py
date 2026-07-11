# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "create_new_author_model_experiment.py"


def load_script_module():
    spec = spec_from_file_location("experiment_scaffolder", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_minimal_repository(root: Path) -> None:
    write_json(
        root / "author-lab-project-manifest.json",
        {
            "project_id": "test-author-lab",
            "author_model_experiments_directory": "author-model-experiments",
        },
    )
    write_json(
        root / "runtime-adapters/test-runtime/runtime-adapter-configuration.json",
        {
            "runtime_adapter_id": "test-runtime",
            "configuration_version": "1.0.0",
            "context_window_tokens": 32000,
            "tool_capabilities": ["repository-read", "web-search"],
        },
    )
    write_json(
        root / "shared-writing-harness/writing-runbooks/test-runbook/writing-runbook-manifest.json",
        {
            "runbook_id": "test-runbook",
            "runbook_version": "1.0.0",
        },
    )
    write_json(
        root / "source-author-models/source-model/source-author-model-manifest.json",
        {
            "source_author_model_id": "source-model",
            "model_version": "1.0.0",
        },
    )
    for persona_id in ("derived-b", "derived-c"):
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
                "derived_author_model_id": f"{persona_id}-model",
                "derived_author_id": persona_id,
                "model_version": "1.0.0",
            },
        )


def test_experiment_scaffolder_creates_four_controlled_conditions(tmp_path):
    module = load_script_module()
    prepare_minimal_repository(tmp_path)

    experiment_root = module.create_experiment(
        repository_root=tmp_path,
        experiment_id="experiment-2026-001-b-c-distinction",
        runtime_adapter_id="test-runtime",
        runbook_id="test-runbook",
        source_model_id="source-model",
        derived_author_b_id="derived-b",
        derived_author_c_id="derived-c",
    )

    manifest = json.loads((experiment_root / "experiment-manifest.json").read_text(encoding="utf-8"))
    roles = {condition["condition_role"] for condition in manifest["conditions"]}
    assert roles == {
        "generic-runtime-baseline",
        "source-model-direct-baseline",
        "derived-author-b",
        "derived-author-c",
    }
    assert manifest["controlled_execution"] == {
        "runtime_adapter_id": "test-runtime",
        "runtime_adapter_version": "1.0.0",
        "runbook_id": "test-runbook",
        "runbook_version": "1.0.0",
        "model_parameters": {},
        "context_budget_tokens": 32000,
        "tool_permissions": ["repository-read", "web-search"],
        "repetition_count": 3,
        "randomness_control": None,
    }
    assert all("runtime_adapter_id" not in condition for condition in manifest["conditions"])
    assert all("runbook_id" not in condition for condition in manifest["conditions"])
    assert manifest["held_out_evaluation_pack_uri"].startswith("evaluator-storage://")
    assert (experiment_root / "controlled-inputs/README.md").is_file()
    assert (experiment_root / "runtime-run-records/README.md").is_file()
    assert (experiment_root / "failure-cases/README.md").is_file()
    assert (experiment_root / "raw-evaluation-results.jsonl").is_file()
    assert (experiment_root / "aggregate-analysis.json").is_file()
    assert (experiment_root / "experiment-conclusion.md").is_file()


def test_experiment_scaffolder_rejects_writer_readable_held_out_uri(tmp_path):
    module = load_script_module()
    prepare_minimal_repository(tmp_path)

    try:
        module.create_experiment(
            repository_root=tmp_path,
            experiment_id="experiment-2026-002-invalid-held-out",
            runtime_adapter_id="test-runtime",
            runbook_id="test-runbook",
            source_model_id="source-model",
            derived_author_b_id="derived-b",
            derived_author_c_id="derived-c",
            held_out_evaluation_pack_uri="author-model-experiments/local-held-out",
        )
    except ValueError as exc:
        assert "evaluator-storage://" in str(exc)
    else:
        raise AssertionError("Expected writer-readable held-out URI to be rejected")
