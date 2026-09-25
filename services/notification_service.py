"""Local notification calculations; no network access."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Iterable, Optional
from .calendar_service import DeadlineItem, days_left

@dataclass(frozen=True)
class Notification:
    level: str
    title: str
    message: str
    order_id: Optional[int] = None


def build_notifications(items: Iterable[DeadlineItem], today: Optional[date] = None) -> list[Notification]:
    result: list[Notification] = []
    for item in items:
        status = (item.status or "").lower()
        if status in {"виконано", "completed", "done"}:
            continue
        left = days_left(item.due_date, today)
        if left is None:
            continue
        if left < 0:
            result.append(Notification("critical", "Прострочене розпорядження", f"№ {item.number}: прострочено на {abs(left)} дн.", item.order_id))
        elif left == 0:
            result.append(Notification("warning", "Термін сьогодні", f"№ {item.number}: необхідно виконати сьогодні.", item.order_id))
        elif left <= 3:
            result.append(Notification("info", "Наближається термін", f"№ {item.number}: залишилось {left} дн.", item.order_id))
    priority = {"critical": 0, "warning": 1, "info": 2}
    return sorted(result, key=lambda n: priority.get(n.level, 9))


def counts(notifications: Iterable[Notification]) -> dict[str, int]:
    result = {"critical": 0, "warning": 0, "info": 0}
    for item in notifications:
        result[item.level] = result.get(item.level, 0) + 1
    return result
