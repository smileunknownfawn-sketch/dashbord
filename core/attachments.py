"""Необов'язкові додатки до розпоряджень та відповідей."""
from __future__ import annotations

from pathlib import Path
import shutil
from uuid import uuid4

ALLOWED_ATTACHMENT_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt", ".rtf",
    ".jpg", ".jpeg", ".png", ".zip", ".7z", ".rar", ".odt", ".ods",
}


def safe_filename(name: str) -> str:
    name = Path(name).name.strip()
    return "_".join(name.split()) or "додаток"


def add_attachment(source: str | Path, target_dir: str | Path) -> Path:
    """Копіює додаток у локальну папку розпорядження без зміни оригіналу."""
    source = Path(source).resolve()
    target_dir = Path(target_dir).resolve()
    if not source.is_file():
        raise FileNotFoundError("Файл додатка не знайдено")
    if source.suffix.casefold() not in ALLOWED_ATTACHMENT_EXTENSIONS:
        raise ValueError("Тип файла додатка не підтримується")
    target_dir.mkdir(parents=True, exist_ok=True)
    destination = target_dir / safe_filename(source.name)
    if destination.exists():
        destination = target_dir / f"{destination.stem}_{uuid4().hex[:8]}{destination.suffix}"
    shutil.copy2(source, destination)
    return destination


def list_attachments(folder: str | Path) -> list[Path]:
    folder = Path(folder)
    if not folder.exists():
        return []
    return sorted((p for p in folder.iterdir() if p.is_file()), key=lambda p: p.name.casefold())
