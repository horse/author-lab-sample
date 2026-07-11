# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "repository-automation-scripts/create_new_derived_author_persona.py"


def load_module():
    spec = spec_from_file_location("persona_atomic_registration", SCRIPT_PATH)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_repository(root: Path, *, broken_template: bool = False) -> None:
    write_json(
        root / "author-lab-project-manifest.json",
        {
            "repository_mode": "active-author-lab",
            "default_language": "zh-Hans",
            "persona_scaffold_template_manifest": "shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json",
            "source_author_model_directories": ["source-author-models/source-model"],
            "derived_author_persona_directories": [],
            "component_status_register": "repository-component-status-register.json",
            "placeholder_register": "repository-placeholder-register.json",
        },
    )
    write_json(root / "repository-component-status-register.json", {"schema_version": "1.0.0", "components": []})
    write_json(
        root / "repository-placeholder-register.json",
        {
            "schema_version": "1.0.0",
            "repository_mode": "active-author-lab",
            "placeholder_policy": "registered-placeholder-paths-only",
            "registered_placeholder_paths": [],
            "active_author_lab_policy": "registered-placeholder-paths-only",
            "ignored_generated_path_patterns": [],
        },
    )
    write_json(
        root / "source-author-models/source-model/source-author-model-manifest.json",
        {
            "source_author_model_id": "source-model",
            "source_author_id": "source-author",
            "model_version": "1.0.0",
        },
    )
    markdown_files = [
        {"path": "README.md", "title": "{{display_name}}", "purpose": "Overview."},
        {"path": "AGENTS.md", "title": "Rules", "purpose": "Rules."},
        {"path": "derived-author-model/core-derived-author-model/identity.md", "title": "Identity", "purpose": "Identity."},
    ]
    if broken_template:
        markdown_files.append({"path": "derived-author-model/core-derived-author-model/broken.md", "title": "{{unknown_variable}}", "purpose": "Broken."})
    required_paths = [
        "README.md",
        "AGENTS.md",
        "derived-author-persona-manifest.json",
        "derived-author-lineage.json",
        "derived-author-model/VERSION",
        "derived-author-model/derived-author-model-manifest.json",
        "derived-author-model/derived-author-model-loading-map.json",
        "derived-author-model/core-derived-author-model/identity.md",
        "derived-author-model/genre-specific-writing-modes/essay-writing-mode.md",
        "derived-author-memory/publication-history.jsonl",
        "derived-author-writing-work-items/derived-author-work-item-index.jsonl",
        "derived-author-publications/derived-author-publication-index.jsonl",
    ]
    if broken_template:
        required_paths.append("derived-author-model/core-derived-author-model/broken.md")
    write_json(
        root / "shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json",
        {
            "required_directories": [
                "derived-author-model/core-derived-author-model",
                "derived-author-model/genre-specific-writing-modes",
                "derived-author-memory",
                "derived-author-writing-work-items",
                "derived-author-evaluations",
                "derived-author-publications",
            ],
            "required_paths": required_paths,
            "markdown_files": markdown_files,
            "default_genre_modes": [
                {"path": "derived-author-model/genre-specific-writing-modes/essay-writing-mode.md", "title": "Essay"}
            ],
        },
    )


def test_persona_creation_registers_manifest_and_component(tmp_path):
    module = load_module()
    prepare_repository(tmp_path)

    persona_root = module.create_persona(
        repository_root=tmp_path,
        derived_author_id="derived-author-real-b",
        display_name="Derived Author Real B",
        source_model_id="source-model",
        source_model_version="1.0.0",
    )

    project = json.loads((tmp_path / "author-lab-project-manifest.json").read_text(encoding="utf-8"))
    components = json.loads((tmp_path / "repository-component-status-register.json").read_text(encoding="utf-8"))["components"]
    assert persona_root == tmp_path / "derived-author-personas/derived-author-real-b"
    assert "derived-author-personas/derived-author-real-b" in project["derived_author_persona_directories"]
    assert any(item["path"] == "derived-author-personas/derived-author-real-b" for item in components)


def test_persona_creation_rejects_unknown_or_wrong_source_model(tmp_path):
    module = load_module()
    prepare_repository(tmp_path)

    for model_id, version in (("missing-model", "1.0.0"), ("source-model", "9.9.9")):
        try:
            module.create_persona(
                repository_root=tmp_path,
                derived_author_id=f"derived-author-{model_id.replace('model', 'test')}",
                display_name="Derived Author",
                source_model_id=model_id,
                source_model_version=version,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("Expected source-model resolution to fail")


def test_persona_render_failure_leaves_no_partial_directory_or_registration(tmp_path):
    module = load_module()
    prepare_repository(tmp_path, broken_template=True)

    try:
        module.create_persona(
            repository_root=tmp_path,
            derived_author_id="derived-author-broken",
            display_name="Derived Author Broken",
            source_model_id="source-model",
            source_model_version="1.0.0",
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected unresolved template variable to fail")

    assert not (tmp_path / "derived-author-personas/derived-author-broken").exists()
    project = json.loads((tmp_path / "author-lab-project-manifest.json").read_text(encoding="utf-8"))
    assert project["derived_author_persona_directories"] == []
