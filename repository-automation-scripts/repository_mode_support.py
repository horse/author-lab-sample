#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"
REFERENCE_SAMPLE_MODE = "reference-sample"
ACTIVE_AUTHOR_LAB_MODE = "active-author-lab"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(document: dict[str, Any]) -> str:
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


@dataclass(frozen=True)
class RepositoryModeContext:
    repository_root: Path
    project: dict[str, Any]

    @classmethod
    def from_project(cls, repository_root: Path) -> "RepositoryModeContext":
        project = load_json(repository_root / "author-lab-project-manifest.json")
        mode = project.get("repository_mode", REFERENCE_SAMPLE_MODE)
        if mode not in {REFERENCE_SAMPLE_MODE, ACTIVE_AUTHOR_LAB_MODE}:
            raise ValueError(f"Unknown repository_mode: {mode!r}")
        return cls(repository_root=repository_root, project=project)

    @property
    def mode(self) -> str:
        return self.project.get("repository_mode", REFERENCE_SAMPLE_MODE)

    @property
    def is_reference_sample(self) -> bool:
        return self.mode == REFERENCE_SAMPLE_MODE

    def json_marker_fields(self) -> dict[str, str]:
        return {"_sample_comment": SAMPLE_MARKER} if self.is_reference_sample else {}

    def with_json_marker(self, document: dict[str, Any]) -> dict[str, Any]:
        return {**self.json_marker_fields(), **document}

    def markdown_marker(self) -> str:
        return f"<!-- {SAMPLE_MARKER} -->\n\n" if self.is_reference_sample else ""

    def python_marker(self) -> str:
        return f"# {SAMPLE_MARKER}\n" if self.is_reference_sample else ""

    def initial_status(self, sample_status: str, active_status: str) -> str:
        return sample_status if self.is_reference_sample else active_status

    def render_text(self, text: str, replacements: dict[str, str] | None = None) -> str:
        rendered = text
        for key, value in (replacements or {}).items():
            rendered = rendered.replace("{{" + key + "}}", value)
        unresolved = sorted(set(re.findall(r"\{\{[a-zA-Z0-9_-]+\}\}", rendered)))
        if unresolved:
            raise ValueError(f"Unresolved template variables: {unresolved}")
        if not self.is_reference_sample:
            rendered = rendered.replace(f"<!-- {SAMPLE_MARKER} -->\n\n", "")
            rendered = rendered.replace(f"<!-- {SAMPLE_MARKER} -->\n", "")
            rendered = rendered.replace(f"# {SAMPLE_MARKER}\n", "")
            if rendered.lstrip().startswith("{"):
                try:
                    document = json.loads(rendered)
                except json.JSONDecodeError:
                    pass
                else:
                    document.pop("_sample_comment", None)
                    rendered = dump_json(document)
        return rendered

    def empty_jsonl(self, sample_record: dict[str, Any]) -> str:
        if not self.is_reference_sample:
            return ""
        return json.dumps(self.with_json_marker(sample_record), ensure_ascii=False) + "\n"


def reject_sample_sentinels(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return errors
    text = path.read_text(encoding="utf-8")
    for sentinel in (
        SAMPLE_MARKER,
        "SAMPLE-NOT-RUN",
        "SAMPLE-NOT-PUBLISHED",
        "replace-with-real-checksum",
        "sample-placeholder",
        "sample-unreviewed",
        "sample-development",
    ):
        if sentinel in text:
            errors.append(f"{path}: active production file contains sample sentinel {sentinel!r}")
    return errors
