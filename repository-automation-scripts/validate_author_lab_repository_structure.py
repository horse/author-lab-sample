#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

from pathlib import Path
import sys

REQUIRED_PATHS = (
    "README.md",
    "AGENTS.md",
    "author-lab-project-manifest.json",
    "source-authors/source-author-sample/source-author-profile.json",
    "source-author-research/source-author-sample-research",
    "source-author-models/source-author-sample-model/source-author-model-manifest.json",
    "derived-author-personas/derived-author-sample-b/derived-author-persona-manifest.json",
    "derived-author-personas/derived-author-sample-c/derived-author-persona-manifest.json",
    "shared-writing-harness/machine-readable-contracts",
    "shared-writing-harness/writing-runbooks",
    "agent-skills",
    "runtime-adapters",
    "writing-work-items",
    "author-model-evaluations",
    "approved-publications/approved-publication-manifest.jsonl",
    "repository-automation-scripts",
    "repository-validation-tests",
)


def find_missing_paths(repository_root: Path) -> list[str]:
    return [path for path in REQUIRED_PATHS if not (repository_root / path).exists()]


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    missing = find_missing_paths(repository_root)
    if missing:
        print("Missing required repository paths:")
        for path in missing:
            print(f"- {path}")
        return 1
    print(f"Repository structure validation passed: {len(REQUIRED_PATHS)} required paths found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
