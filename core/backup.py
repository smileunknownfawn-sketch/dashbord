from __future__ import annotations

import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from .config import AppPaths
from .database import Database


class BackupService:
    """Creates portable local ZIP backups containing the database and documents."""

    def __init__(self, paths: AppPaths, database: Database):
        self.paths = paths
        self.db = database
        self.paths.backups.mkdir(parents=True, exist_ok=True)

    def create(self, include_documents: bool = True) -> Path:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive = self.paths.backups / f"backup_{stamp}.zip"
        manifest = {
            "version": "3.0",
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "includes_documents": include_documents,
            "database": self.paths.database.name,
        }
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            if self.paths.database.exists():
                zf.write(self.paths.database, "database.db")
            zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
            if include_documents and self.paths.orders.exists():
                for path in self.paths.orders.rglob("*"):
                    if path.is_file():
                        zf.write(path, Path("Розпорядження") / path.relative_to(self.paths.orders))
        return archive

    def list_backups(self) -> list[Path]:
        return sorted(self.paths.backups.glob("*.zip"), reverse=True)

    def restore_database(self, archive: Path) -> Path:
        archive = archive.resolve()
        try:
            archive.relative_to(self.paths.backups.resolve())
        except ValueError as exc:
            raise ValueError("Для відновлення дозволені лише локальні резервні копії") from exc
        staging = self.paths.backups / ".restore_tmp"
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True)
        with zipfile.ZipFile(archive) as zf:
            members = [m for m in zf.namelist() if m in {"database.db", "manifest.json"}]
            zf.extractall(staging, members=members)
        source = staging / "database.db"
        if not source.exists():
            shutil.rmtree(staging)
            raise ValueError("У резервній копії немає database.db")
        current = self.paths.database.with_suffix(".before_restore.db")
        if self.paths.database.exists():
            shutil.copy2(self.paths.database, current)
        shutil.copy2(source, self.paths.database)
        shutil.rmtree(staging)
        return current
