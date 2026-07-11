# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "validate_machine_readable_contracts.py"


def load_script_module():
    spec = spec_from_file_location("contract_validator", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_registry(root: Path) -> None:
    write_json(
        root / "shared-writing-harness/machine-readable-contracts/test.schema.json",
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["required_field"],
            "properties": {"required_field": {"type": "string"}},
            "additionalProperties": False,
        },
    )
    write_json(
        root / "shared-writing-harness/machine-readable-contracts/document-schema-registry.json",
        {
            "entries": [
                {
                    "path_pattern": "registered.json",
                    "document_format": "json",
                    "schema_path": "shared-writing-harness/machine-readable-contracts/test.schema.json",
                    "required_match": True,
                }
            ],
            "excluded_path_patterns": [
                {
                    "path_pattern": "shared-writing-harness/machine-readable-contracts/*.schema.json",
                    "classification": "schema-definition",
                    "reason": "Schemas validate other documents.",
                },
                {
                    "path_pattern": "shared-writing-harness/machine-readable-contracts/document-schema-registry.json",
                    "classification": "schema-registry",
                    "reason": "The registry controls validation coverage.",
                },
            ],
        },
    )


def test_registered_document_missing_required_field_is_rejected(tmp_path):
    module = load_script_module()
    prepare_registry(tmp_path)
    write_json(tmp_path / "registered.json", {})

    _, errors = module.validate_registered_documents(tmp_path)
    assert any("'required_field' is a required property" in error for error in errors)


def test_unregistered_machine_document_is_rejected(tmp_path):
    module = load_script_module()
    prepare_registry(tmp_path)
    write_json(tmp_path / "registered.json", {"required_field": "valid"})
    write_json(tmp_path / "unregistered.json", {"free_form": True})

    _, errors = module.validate_registered_documents(tmp_path)
    assert "Machine-readable document has no schema registration or explicit classification: unregistered.json" in errors


def test_explicitly_classified_template_document_is_not_treated_as_runtime_contract(tmp_path):
    module = load_script_module()
    prepare_registry(tmp_path)
    registry_path = tmp_path / "shared-writing-harness/machine-readable-contracts/document-schema-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["excluded_path_patterns"].append(
        {
            "path_pattern": "templates/*.json",
            "classification": "artifact-template",
            "reason": "Template variables are not runtime records.",
        }
    )
    write_json(registry_path, registry)
    write_json(tmp_path / "registered.json", {"required_field": "valid"})
    write_json(tmp_path / "templates/template.json", {"placeholder": "{{value}}"})

    _, errors = module.validate_registered_documents(tmp_path)
    assert errors == []
