from __future__ import annotations

import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .config import AppPaths


class StorageError(RuntimeError):
    pass


class LocalStorage:
    """All document operations stay inside the selected local workspace."""

    def __init__(self, paths: AppPaths):
        self.paths = paths
        self.paths.ensure()

    def safe(self, relative: str | Path) -> Path:
        candidate = (self.paths.root / relative).resolve()
        try:
            candidate.relative_to(self.paths.root.resolve())
        except ValueError as exc:
            raise StorageError("Небезпечний шлях до локального файлу") from exc
        return candidate

    @staticmethod
    def clean_name(value: str, fallback: str = "Документ") -> str:
        allowed = " ._-()[]"
        cleaned = "".join(ch if ch.isalnum() or ch in allowed else "_" for ch in str(value).strip())
        return cleaned or fallback

    def unique_path(self, folder: Path, filename: str) -> Path:
        folder = self.safe(folder.relative_to(self.paths.root))
        folder.mkdir(parents=True, exist_ok=True)
        name = self.clean_name(filename)
        path = folder / name
        counter = 2
        while path.exists():
            path = folder / f"{Path(name).stem}_{counter}{Path(name).suffix}"
            counter += 1
        return path

    def save_bytes(self, folder: Path, filename: str, data: bytes) -> Path:
        path = self.unique_path(folder, filename)
        path.write_bytes(data)
        return path

    def read(self, relative: str | Path) -> bytes:
        path = self.safe(relative)
        if not path.is_file():
            raise StorageError("Файл не знайдено")
        return path.read_bytes()

    def delete_to_trash(self, relative_folder: str, label: str) -> Path:
        source = self.safe(relative_folder)
        if not source.exists():
            raise StorageError("Папку не знайдено")
        target = self.paths.trash / f"{datetime.now():%Y%m%d_%H%M%S}_{self.clean_name(label)}"
        target = self.unique_path(self.paths.trash, target.name)
        shutil.move(str(source), str(target))
        return target

    def restore_from_trash(self, trash_folder: Path, destination_name: str) -> Path:
        trash_folder = trash_folder.resolve()
        try:
            trash_folder.relative_to(self.paths.trash.resolve())
        except ValueError as exc:
            raise StorageError("Небезпечний шлях кошика") from exc
        destination = self.paths.orders / self.clean_name(destination_name)
        if destination.exists():
            destination = self.paths.orders / f"{destination.name}_відновлено_{datetime.now():%H%M%S}"
        shutil.move(str(trash_folder), str(destination))
        return destination

    def sha256(self, relative: str | Path) -> str:
        digest = hashlib.sha256()
        with self.safe(relative).open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def inventory(self) -> dict[str, int | float]:
        files = 0
        folders = 0
        bytes_total = 0
        for path in self.paths.root.rglob("*"):
            if any(part.startswith(".") for part in path.relative_to(self.paths.root).parts):
                continue
            if path.is_file():
                files += 1
                try:
                    bytes_total += path.stat().st_size
                except OSError:
                    pass
            elif path.is_dir():
                folders += 1
        return {"files": files, "folders": folders, "bytes": bytes_total, "mb": round(bytes_total / 1024 / 1024, 2)}

    def validate(self) -> list[str]:
        problems: list[str] = []
        if not self.paths.root.exists():
            problems.append("Кореневу папку не знайдено")
        for name, path in (("Розпорядження", self.paths.orders), ("Кошик", self.paths.trash), ("Резервні копії", self.paths.backups)):
            if not path.exists():
                problems.append(f"Відсутня папка: {name}")
        return problems
