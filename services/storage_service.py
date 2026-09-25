"""Safe local storage helpers for the dashboard."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import shutil

@dataclass(frozen=True)
class StorageCheck:
    root_exists: bool
    database_exists: bool
    orders_exists: bool
    backups_exists: bool
    writable: bool
    total_files: int
    total_bytes: int


def inside(root: Path, candidate: Path) -> bool:
    root = root.resolve()
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def safe_child(root: Path, name: str) -> Path:
    cleaned = "".join(ch if ch.isalnum() or ch in " ._-()[]" else "_" for ch in str(name).strip()) or "Документ"
    candidate = (root / cleaned).resolve()
    if not inside(root, candidate):
        raise ValueError("Небезпечний шлях")
    return candidate


def storage_check(workspace: Path) -> StorageCheck:
    root = workspace.resolve()
    files = [p for p in root.rglob("*") if p.is_file()] if root.exists() else []
    writable = False
    if root.exists():
        probe = root / f".dashboard_probe_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        try:
            probe.write_text("ok", encoding="utf-8")
            probe.unlink(missing_ok=True)
            writable = True
        except OSError:
            writable = False
    return StorageCheck(root.exists(), (root / "database.db").exists(), (root / "Розпорядження").exists(), (root / "Резервні копії").exists(), writable, len(files), sum(p.stat().st_size for p in files))


def make_backup(workspace: Path) -> Path:
    root = workspace.resolve()
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destination = safe_child(root / "Резервні копії", f"Резервна_копія_{stamp}")
    destination.mkdir(parents=True, exist_ok=True)
    database = root / "database.db"
    orders = root / "Розпорядження"
    if database.exists():
        shutil.copy2(database, destination / "database.db")
    if orders.exists():
        shutil.copytree(orders, destination / "Розпорядження", dirs_exist_ok=True)
    return destination
