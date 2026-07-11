#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import json
from pathlib import Path
import sys

ALLOWED_LIFECYCLE_STATUSES = (
    "intake",
    "in-progress",
    "under-review",
    "approved",
    "published",
    "archived",
)


def validate_state_document(document: dict) -> list[str]:
    errors: list[str] = []
    lifecycle_status = document.get("lifecycle_status")
    stage_executions = document.get("stage_executions", {})
    quality_gates = document.get("quality_gates", {})

    if lifecycle_status not in ALLOWED_LIFECYCLE_STATUSES:
        errors.append(f"Unknown lifecycle_status: {lifecycle_status!r}")
        return errors

    factual_gate = quality_gates.get("factual_accuracy")
    style_gate = quality_gates.get("persona_and_style")
    editorial_gate = quality_gates.get("editorial_approval")

    if factual_gate == "passed" and stage_executions.get("factual-review", {}).get("status") != "completed":
        errors.append("factual_accuracy=passed requires factual-review stage status=completed.")
    if style_gate == "passed" and stage_executions.get("style-review", {}).get("status") != "completed":
        errors.append("persona_and_style=passed requires style-review stage status=completed.")

    if lifecycle_status in {"under-review", "approved", "published", "archived"}:
        if factual_gate != "passed":
            errors.append(f"{lifecycle_status} requires factual_accuracy=passed.")
        if style_gate != "passed":
            errors.append(f"{lifecycle_status} requires persona_and_style=passed.")

    if lifecycle_status in {"approved", "published", "archived"} and editorial_gate != "approved":
        errors.append(f"{lifecycle_status} requires editorial_approval=approved.")

    if lifecycle_status == "published" and not document.get("publication"):
        errors.append("published lifecycle_status requires publication metadata.")

    if editorial_gate == "approved" and stage_executions.get("editor-review", {}).get("status") != "completed":
        errors.append("editorial_approval=approved requires editor-review stage status=completed.")

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
