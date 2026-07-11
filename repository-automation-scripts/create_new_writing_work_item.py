#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re

SAMPLE_MARKER = "这是一个 sample，文件实质完成后删掉这行注释"


def validate_identifier(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("Work-item ID must use YYYY-NNN-descriptive-slug.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new writing work-item scaffold.")
    parser.add_argument("work_item_id", type=validate_identifier)
    parser.add_argument("--derived-author-id", required=True)
    parser.add_argument("--author-model-version", required=True)
    parser.add_argument("--runbook-id", required=True)
    parser.add_argument("--runtime-adapter-id", required=True)
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    year = arguments.work_item_id[:4]
    work_root = repository_root / "writing-work-items" / f"{year}-writing-work-items" / arguments.work_item_id
    if work_root.exists():
        raise SystemExit(f"Work item already exists: {work_root}")
    work_root.mkdir(parents=True)

    state = {
        "_sample_comment": SAMPLE_MARKER,
        "work_item_id": arguments.work_item_id,
        "derived_author_id": arguments.derived_author_id,
        "status": "intake",
        "author_model_version": arguments.author_model_version,
        "runbook_id": arguments.runbook_id,
        "runtime_adapter_id": arguments.runtime_adapter_id,
        "reviews": {
            "factual_review": "not-started",
            "style_review": "not-started",
            "editor_review": "not-started",
        },
        "publication": None,
        "created_on": date.today().isoformat(),
    }
    (work_root / "work-item-state.json").write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for filename, title in (
        ("writing-brief.md", "Writing Brief"),
        ("research-pack.md", "Research Pack"),
        ("article-plan.md", "Article Plan"),
    ):
        (work_root / filename).write_text(f"# {title}\n\n<!-- {SAMPLE_MARKER} -->\n", encoding="utf-8")
    print(f"Created writing work item: {work_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
