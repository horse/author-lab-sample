#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys

ALLOWED_STATES = (
    "intake",
    "research",
    "planned",
    "drafted",
    "fact-checked",
    "style-reviewed",
    "editor-review",
    "approved",
    "published",
    "archived",
)


def validate_state_document(document: dict) -> list[str]:
    errors: list[str] = []
    status = document.get("status")
    reviews = document.get("reviews", {})
    if status not in ALLOWED_STATES:
        errors.append(f"Unknown work-item status: {status!r}")
        return errors

    status_index = ALLOWED_STATES.index(status)
    if status_index >= ALLOWED_STATES.index("fact-checked") and reviews.get("factual_review") != "passed":
        errors.append("Status requires factual_review=passed.")
    if status_index >= ALLOWED_STATES.index("style-reviewed") and reviews.get("style_review") != "passed":
        errors.append("Status requires style_review=passed.")
    if status_index >= ALLOWED_STATES.index("approved") and reviews.get("editor_review") != "approved":
        errors.append("Approved or later status requires editor_review=approved.")
    if status == "published" and not document.get("publication"):
        errors.append("Published status requires publication metadata.")
    return errors


def main(argv: list[str] | None = None) -> int:
    arguments = argv if argv is not None else sys.argv[1:]
    if arguments:
        state_paths = [Path(value) for value in arguments]
    else:
        repository_root = Path(__file__).resolve().parents[1]
        state_paths = list(repository_root.glob("writing-work-items/**/work-item-state.json"))

    errors: list[str] = []
    for path in state_paths:
        with path.open("r", encoding="utf-8") as handle:
            document = json.load(handle)
        errors.extend(f"{path}: {error}" for error in validate_state_document(document))

    if errors:
        print("Work-item state validation failed:")
        print("\n".join(errors))
        return 1
    print(f"Work-item state validation passed: {len(state_paths)} state files checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
