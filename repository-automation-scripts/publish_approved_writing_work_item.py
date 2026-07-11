#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Any, Iterator

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from atomic_repository_update import atomic_replace_text_files  # noqa: E402
from publication_gate_support import (  # noqa: E402
    ALLOWED_PUBLICATION_CATEGORIES,
    collect_publication_records,
    find_work_item,
    load_json,
    serialize_publication_manifest,
    validate_approved_work_item,
    validate_publication_record,
)
from rebuild_derived_author_indexes import (  # noqa: E402
    build_persona_index_documents,
    canonical_work_item_records,
)
from repository_mode_support import RepositoryModeContext, dump_json  # noqa: E402


def validate_publication_identifier(value: str) -> str:
    if not re.fullmatch(
        r"publication-\d{4}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*",
        value,
    ):
        raise argparse.ArgumentTypeError(
            "Publication ID must use publication-YYYY-NNN-descriptive-slug."
        )
    return value


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_json(document), encoding="utf-8")


def read_optional_text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def restore_text(path: Path, content: str | None) -> None:
    if content is None:
        path.unlink(missing_ok=True)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


@contextmanager
def publication_lock(publications_root: Path) -> Iterator[None]:
    lock_path = publications_root / ".publication-transaction.lock"
    publications_root.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError(
            f"Another publication transaction holds {lock_path}"
        ) from exc
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        os.close(descriptor)
        yield
    finally:
        try:
            os.close(descriptor)
        except OSError:
            pass
        lock_path.unlink(missing_ok=True)


def transaction_paths(
    repository_root: Path, project: dict[str, Any]
) -> tuple[Path, Path, Path]:
    publications_root = repository_root / project["approved_publications_directory"]
    return (
        publications_root,
        publications_root / ".publication-transaction.json",
        publications_root / ".publication-staging",
    )


def recover_incomplete_publication_transaction(repository_root: Path) -> None:
    project = load_json(repository_root / "author-lab-project-manifest.json")
    publications_root, journal_path, staging_parent = transaction_paths(
        repository_root, project
    )
    if not journal_path.is_file():
        if staging_parent.is_dir() and not any(staging_parent.iterdir()):
            staging_parent.rmdir()
        return
    journal = load_json(journal_path)
    target_root = repository_root / journal["target_root"]
    if target_root.exists():
        shutil.rmtree(target_root, ignore_errors=True)
    for relative_path, content in journal.get("backups", {}).items():
        restore_text(repository_root / relative_path, content)
    staging_root_value = journal.get("staging_root")
    if staging_root_value:
        shutil.rmtree(repository_root / staging_root_value, ignore_errors=True)
    journal_path.unlink(missing_ok=True)
    lock_path = publications_root / ".publication-transaction.lock"
    lock_path.unlink(missing_ok=True)
    if staging_parent.is_dir() and not any(staging_parent.iterdir()):
        staging_parent.rmdir()


def work_item_states_with_replacement(
    repository_root: Path,
    project: dict[str, Any],
    state_path: Path,
    new_state: dict[str, Any],
) -> list[tuple[Path, dict[str, Any]]]:
    states = canonical_work_item_records(repository_root, project)
    return [
        (path, new_state if path == state_path else state)
        for path, state in states
    ]


def publish_approved_work_item(
    repository_root: Path,
    work_item_id: str,
    publication_id: str,
    title: str,
    publication_category: str,
    publication_status: str,
    published_at: str | None,
) -> Path:
    if publication_category not in ALLOWED_PUBLICATION_CATEGORIES:
        raise ValueError(
            f"Unknown publication category {publication_category!r}; "
            f"allowed categories are {sorted(ALLOWED_PUBLICATION_CATEGORIES)}"
        )
    if publication_status not in {"approved", "published"}:
        raise ValueError(
            "Publication transaction accepts only approved or published status"
        )
    if publication_status == "published" and not published_at:
        raise ValueError("published status requires published_at")

    recover_incomplete_publication_transaction(repository_root)
    context = RepositoryModeContext.from_project(repository_root)
    project = context.project
    publications_root, journal_path, staging_parent = transaction_paths(
        repository_root, project
    )

    with publication_lock(publications_root):
        work_root, state = find_work_item(
            repository_root,
            project["writing_work_items_directory"],
            work_item_id,
        )
        final_file = validate_approved_work_item(
            repository_root,
            project,
            state,
            work_root,
        )
        target_root = publications_root / publication_category / publication_id
        if target_root.exists():
            raise ValueError(f"Publication target already exists: {target_root}")

        canonical_relative = (
            Path(project["approved_publications_directory"])
            / publication_category
            / publication_id
            / "article.md"
        )
        metadata = context.with_json_marker(
            {
                "publication_id": publication_id,
                "work_item_id": work_item_id,
                "derived_author_id": state["derived_author_id"],
                "derived_author_model_id": state["derived_author_model_id"],
                "derived_author_model_version": state[
                    "derived_author_model_version"
                ],
                "title": title,
                "publication_status": publication_status,
                "canonical_file": canonical_relative.as_posix(),
                "published_at": published_at,
            }
        )
        validate_publication_record(
            repository_root,
            project,
            metadata,
            require_canonical_file=False,
        )

        staging_parent.mkdir(parents=True, exist_ok=True)
        staging_root = Path(
            tempfile.mkdtemp(prefix=f"{publication_id}-", dir=staging_parent)
        )
        staged_publication_root = staging_root / publication_id
        state_path = work_root / "work-item-state.json"
        manifest_path = publications_root / "approved-publication-manifest.jsonl"
        promoted = False
        try:
            staged_publication_root.mkdir(parents=True)
            shutil.copyfile(final_file, staged_publication_root / "article.md")
            write_json(
                staged_publication_root / "publication-metadata.json", metadata
            )

            records = collect_publication_records(
                repository_root, project["approved_publications_directory"]
            )
            if any(item["publication_id"] == publication_id for item in records):
                raise ValueError(f"Duplicate publication_id: {publication_id}")
            records.append(metadata)
            records.sort(key=lambda item: item["publication_id"])

            new_state = json.loads(json.dumps(state))
            new_state["lifecycle_status"] = publication_status
            new_state["publication"] = {
                "publication_id": publication_id,
                "publication_status": publication_status,
                "canonical_file": canonical_relative.as_posix(),
                "published_at": published_at,
            }
            new_state.setdefault("stage_executions", {}).setdefault(
                "publication-preparation", {"status": "not-started"}
            )["status"] = "completed"

            work_states = work_item_states_with_replacement(
                repository_root, project, state_path, new_state
            )
            index_updates = build_persona_index_documents(
                repository_root,
                project,
                publication_records=records,
                work_item_states=work_states,
            )
            updates = {
                manifest_path: serialize_publication_manifest(records),
                state_path: dump_json(new_state),
                **index_updates,
            }
            backups = {
                path.relative_to(repository_root).as_posix(): read_optional_text(path)
                for path in updates
            }
            journal = {
                "transaction_id": publication_id,
                "status": "prepared",
                "target_root": target_root.relative_to(repository_root).as_posix(),
                "staging_root": staging_root.relative_to(repository_root).as_posix(),
                "backups": backups,
            }
            write_json(journal_path, journal)

            target_root.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged_publication_root, target_root)
            promoted = True
            atomic_replace_text_files(updates)
            journal_path.unlink(missing_ok=True)
            shutil.rmtree(staging_root, ignore_errors=True)
        except Exception:
            if promoted and target_root.exists():
                shutil.rmtree(target_root, ignore_errors=True)
            if journal_path.is_file():
                journal = load_json(journal_path)
                for relative_path, content in journal.get("backups", {}).items():
                    restore_text(repository_root / relative_path, content)
                journal_path.unlink(missing_ok=True)
            shutil.rmtree(staging_root, ignore_errors=True)
            raise
        finally:
            if staging_parent.is_dir() and not any(staging_parent.iterdir()):
                staging_parent.rmdir()
        return target_root


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Publish one approved writing work item through a recoverable transaction."
        )
    )
    parser.add_argument("work_item_id")
    parser.add_argument("publication_id", type=validate_publication_identifier)
    parser.add_argument("--title", required=True)
    parser.add_argument("--publication-category", required=True)
    parser.add_argument(
        "--publication-status",
        choices=("approved", "published"),
        default="approved",
    )
    parser.add_argument("--published-at")
    arguments = parser.parse_args()

    repository_root = Path(__file__).resolve().parents[1]
    publication_root = publish_approved_work_item(
        repository_root=repository_root,
        work_item_id=arguments.work_item_id,
        publication_id=arguments.publication_id,
        title=arguments.title,
        publication_category=arguments.publication_category,
        publication_status=arguments.publication_status,
        published_at=arguments.published_at,
    )
    print(f"Published approved writing work item to {publication_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
