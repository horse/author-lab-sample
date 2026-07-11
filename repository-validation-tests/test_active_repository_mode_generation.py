# 这是一个 sample，文件实质完成后删掉这行注释

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPOSITORY_ROOT / "repository-automation-scripts"
SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def load_module(name: str, filename: str):
    spec = spec_from_file_location(name, SCRIPTS / filename)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare_persona_repository(root: Path, mode: str) -> None:
    write_json(
        root / "author-lab-project-manifest.json",
        {
            "repository_mode": mode,
            "default_language": "zh-Hans",
            "persona_scaffold_template_manifest": "shared-writing-harness/scaffold-templates/derived-author-persona-template/template-manifest.json",
            "source_author_model_directories": ["source-author-models/source-model"],
            "derived_author_persona_directories": [],
            "component_status_register": "repository-component-status-register.json",
            "placeholder_register": "repository-placeholder-register.json",
        },
    )
    write_json(
        root / "repository-component-status-register.json",
        {"schema_version": "1.0.0", "components": []},
    )
    write_json(
        root / "repository-placeholder-register.json",
        {
            "schema_version": "1.0.0",
            "repository_mode": mode,
            "placeholder_policy": (
                "all-managed-text-files"
                if mode == "reference-sample"
                else "registered-placeholder-paths-only"
            ),
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
            "markdown_files": [
                {"path": "README.md", "title": "{{display_name}}", "purpose": "Overview."},
                {"path": "AGENTS.md", "title": "Rules", "purpose": "Rules."},
                {"path": "derived-author-model/core-derived-author-model/identity.md", "title": "Identity", "purpose": "Identity."},
            ],
            "default_genre_modes": [
                {"path": "derived-author-model/genre-specific-writing-modes/essay-writing-mode.md", "title": "Essay"}
            ],
        },
    )


def test_active_persona_generation_contains_no_sample_markers_or_sample_statuses(tmp_path):
    module = load_module("persona_active_mode", "create_new_derived_author_persona.py")
    prepare_persona_repository(tmp_path, "active-author-lab")

    persona_root = module.create_persona(
        repository_root=tmp_path,
        derived_author_id="derived-author-real-b",
        display_name="Derived Author Real B",
        source_model_id="source-model",
        source_model_version="1.0.0",
    )

    for path in persona_root.rglob("*"):
        if path.is_file():
            assert SAMPLE_MARKER not in path.read_text(encoding="utf-8")
    manifest = json.loads((persona_root / "derived-author-persona-manifest.json").read_text(encoding="utf-8"))
    model = json.loads((persona_root / "derived-author-model/derived-author-model-manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "draft"
    assert model["status"] == "unreviewed"


def test_reference_persona_generation_retains_sample_marker(tmp_path):
    module = load_module("persona_reference_mode", "create_new_derived_author_persona.py")
    prepare_persona_repository(tmp_path, "reference-sample")

    persona_root = module.create_persona(
        repository_root=tmp_path,
        derived_author_id="derived-author-sample-d",
        display_name="Derived Author Sample D",
        source_model_id="source-model",
        source_model_version="1.0.0",
    )

    assert SAMPLE_MARKER in (persona_root / "README.md").read_text(encoding="utf-8")
    manifest = json.loads((persona_root / "derived-author-persona-manifest.json").read_text(encoding="utf-8"))
    assert manifest["_sample_comment"] == SAMPLE_MARKER
