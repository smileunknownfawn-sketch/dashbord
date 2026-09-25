from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

MONTHS_UA = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
WEEKDAYS_UA = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
PRIORITIES = ["Звичайний", "Важливий", "Терміновий", "Критичний"]
CATEGORIES = ["Організаційне", "Особовий склад", "Матеріальне", "Навчання", "Бойова підготовка", "Документація", "Інше"]
STATUSES = {"progress": "У РОБОТІ", "today": "ТЕРМІН СЬОГОДНІ", "overdue": "ПРОСТРОЧЕНО", "done": "ВИКОНАНО"}


@dataclass(frozen=True)
class AppPaths:
    root: Path
    orders: Path
    backups: Path
    trash: Path
    exports: Path
    sounds: Path
    database: Path

    @classmethod
    def from_root(cls, root: Path) -> "AppPaths":
        root = root.expanduser().resolve()
        return cls(root, root / "Розпорядження", root / "Резервні копії", root / "Кошик", root / "Звіти", root / "sounds", root / "database.db")

    def ensure(self) -> None:
        for path in (self.root, self.orders, self.backups, self.trash, self.exports):
            path.mkdir(parents=True, exist_ok=True)


APP_VERSION = "3.0.0"
APP_TITLE = "Процес виконання розпоряджень"
