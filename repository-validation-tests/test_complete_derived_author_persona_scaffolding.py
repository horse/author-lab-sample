# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts" / "create_new_derived_author_persona.py"
SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_script_module():
    spec = spec_from_file_location("persona_scaffolder", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_repository(root: Path) -> list[str]:
    required_paths = [
        "README.md",
        "AGENTS.md",
        "derived-author-persona-manifest.json",
        "derived-author-lineage.json",
        "derivation-profile/inherited-source-author-traits.md",
        "derived-author-model/VERSION",
        "derived-author-model/derived-author-model-manifest.json",
        "derived-author-model/derived-author-model-loading-map.json",
        "derived-author-model/core-derived-author-model/derived-author-identity-and-public-role.md",
        "derived-author-model/genre-specific-writing-modes/README.md",
        "derived-author-model/genre-specific-writing-modes/essay-writing-mode.md",
        "author-specific-writing-harness/derived-author-writing-overlays.md",
        "derived-author-memory/publication-history.jsonl",
        "derived-author-writing-work-items/derived-author-work-item-index.jsonl",
        "derived-author-publications/derived-author-publication-index.jsonl",
    ]
    write_json(
        root / "author-lab-project-manifest.json",
        {
            "repository_mode": "reference-sample",
            "default_language": "zh-Hans",
            "source_author_model_directories": ["source-author-models/source-author-test-model"],
            "derived_author_persona_directories": [],
            "component_status_register": "repository-component-status-register.json",
            "persona_scaffold_template_manifest": "shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json",
        },
    )
    write_json(
        root / "repository-component-status-register.json",
        {"_sample_comment": SAMPLE_MARKER, "schema_version": "1.0.0", "components": []},
    )
    write_json(
        root / "source-author-models/source-author-test-model/source-author-model-manifest.json",
        {
            "source_author_model_id": "source-author-test-model",
            "source_author_id": "source-author-test",
            "model_version": "1.0.0",
        },
    )
    write_json(
        root / "shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json",
        {
            "required_directories": [
                "derivation-profile",
                "derived-author-model/core-derived-author-model",
                "derived-author-model/genre-specific-writing-modes",
                "author-specific-writing-harness",
                "derived-author-memory",
                "derived-author-writing-work-items",
                "derived-author-evaluations",
                "derived-author-publications",
            ],
            "required_paths": required_paths,
            "markdown_files": [
                {"path": "README.md", "title": "{{display_name}}", "purpose": "Overview."},
                {"path": "AGENTS.md", "title": "{{display_name}} Agent Rules", "purpose": "Rules."},
                {"path": "derivation-profile/inherited-source-author-traits.md", "title": "Inherited", "purpose": "Inheritance."},
                {"path": "derived-author-model/core-derived-author-model/derived-author-identity-and-public-role.md", "title": "Identity", "purpose": "Identity."},
                {"path": "derived-author-model/genre-specific-writing-modes/README.md", "title": "Genre Modes", "purpose": "Index."},
                {"path": "author-specific-writing-harness/derived-author-writing-overlays.md", "title": "Overlay", "purpose": "Overlay."},
            ],
            "default_genre_modes": [
                {"path": "derived-author-model/genre-specific-writing-modes/essay-writing-mode.md", "title": "Essay Writing Mode"}
            ],
        },
    )
    return required_paths


def test_persona_scaffolder_renders_every_template_required_path(tmp_path):
    module = load_script_module()
    required_paths = prepare_repository(tmp_path)

    persona_root = module.create_persona(
        repository_root=tmp_path,
        derived_author_id="derived-author-test-b",
        display_name="Derived Author Test B",
        source_model_id="source-author-test-model",
        source_model_version="1.0.0",
    )

    missing = [path for path in required_paths if not (persona_root / path).exists()]
    assert missing == []
    manifest = json.loads((persona_root / "derived-author-persona-manifest.json").read_text(encoding="utf-8"))
    lineage = json.loads((persona_root / "derived-author-lineage.json").read_text(encoding="utf-8"))
    model = json.loads((persona_root / "derived-author-model/derived-author-model-manifest.json").read_text(encoding="utf-8"))
    project = json.loads((tmp_path / "author-lab-project-manifest.json").read_text(encoding="utf-8"))
    assert manifest["derived_author_id"] == "derived-author-test-b"
    assert manifest["primary_language"] == "zh-Hans"
    assert lineage["source_models"][0]["source_author_model_id"] == "source-author-test-model"
    assert lineage["may_claim_source_author_identity"] is False
    assert model["derived_author_model_id"] == "derived-author-test-b-model"
    assert "derived-author-personas/derived-author-test-b" in project["derived_author_persona_directories"]
    assert (persona_root / "derived-author-model/VERSION").read_text(encoding="utf-8").endswith("0.1.0\n")


def test_persona_scaffolder_uses_template_manifest_instead_of_fixed_sample_names(tmp_path):
    module = load_script_module()
    required_paths = prepare_repository(tmp_path)
    template_path = tmp_path / "shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json"
    template = json.loads(template_path.read_text(encoding="utf-8"))
    template["required_paths"].append("derived-author-model/core-derived-author-model/custom-template-field.md")
    template["markdown_files"].append(
        {"path": "derived-author-model/core-derived-author-model/custom-template-field.md", "title": "Custom Field", "purpose": "Custom template-defined field."}
    )
    write_json(template_path, template)

    persona_root = module.create_persona(
        repository_root=tmp_path,
        derived_author_id="derived-author-test-c",
        display_name="Derived Author Test C",
        source_model_id="source-author-test-model",
        source_model_version="1.0.0",
    )

    assert (persona_root / "derived-author-model/core-derived-author-model/custom-template-field.md").is_file()
    assert all((persona_root / path).exists() for path in required_paths)
