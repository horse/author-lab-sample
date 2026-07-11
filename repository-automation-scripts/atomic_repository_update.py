#!/usr/bin/env python3
# 这是一个 sample，文件实质完成后删掉这行注释

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import shutil
import tempfile
from typing import Iterator


@contextmanager
def staged_sibling_directory(target: Path) -> Iterator[Path]:
    """Create a temporary sibling directory and always remove it if not promoted."""
    target.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{target.name}.staging-", dir=target.parent)
    )
    try:
        yield staging
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


def promote_staged_directory(staging: Path, target: Path) -> None:
    if target.exists():
        raise ValueError(f"Target already exists: {target}")
    os.replace(staging, target)


def atomic_replace_text_files(updates: dict[Path, str]) -> None:
    """Replace multiple text files and restore every prior value on failure."""
    old_values: dict[Path, str | None] = {}
    temporary_paths: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        for path, content in updates.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            old_values[path] = path.read_text(encoding="utf-8") if path.exists() else None
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
            )
            os.close(descriptor)
            temporary = Path(temporary_name)
            temporary.write_text(content, encoding="utf-8")
            temporary_paths[path] = temporary
        for path, temporary in temporary_paths.items():
            os.replace(temporary, path)
            replaced.append(path)
    except Exception:
        for temporary in temporary_paths.values():
            if temporary.exists():
                temporary.unlink()
        for path in reversed(replaced):
            old = old_values[path]
            if old is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(old, encoding="utf-8")
        raise


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink()
