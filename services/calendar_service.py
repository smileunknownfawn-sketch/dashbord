"""Calendar and deadline service for the local orders dashboard."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Iterable, Optional

@dataclass(frozen=True)
class DeadlineItem:
    order_id: int
    number: str
    due_date: date
    status: str
    priority: str

@dataclass(frozen=True)
class CalendarDay:
    day: date
    items: tuple[DeadlineItem, ...]


def parse_date(value: object) -> Optional[date]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def days_left(due: object, today: Optional[date] = None) -> Optional[int]:
    parsed = parse_date(due)
    if parsed is None:
        return None
    return (parsed - (today or date.today())).days


def deadline_label(due: object, today: Optional[date] = None) -> str:
    left = days_left(due, today)
    if left is None:
        return "Без терміну"
    if left < 0:
        return f"Прострочено на {abs(left)} дн."
    if left == 0:
        return "Термін сьогодні"
    if left == 1:
        return "Залишився 1 день"
    return f"Залишилось {left} дн."


def deadline_state(due: object, status: str = "") -> str:
    normalized = (status or "").lower()
    if normalized in {"виконано", "completed", "done"}:
        return "completed"
    left = days_left(due)
    if left is None:
        return "unknown"
    if left < 0:
        return "overdue"
    if left == 0:
        return "today"
    if left <= 3:
        return "soon"
    return "normal"


def month_days(year: int, month: int) -> list[date]:
    first = date(year, month, 1)
    next_month = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return [first + timedelta(days=i) for i in range((next_month - first).days)]


def group_by_day(items: Iterable[DeadlineItem], year: int, month: int) -> dict[date, list[DeadlineItem]]:
    result: dict[date, list[DeadlineItem]] = {d: [] for d in month_days(year, month)}
    for item in items:
        if item.due_date.year == year and item.due_date.month == month:
            result.setdefault(item.due_date, []).append(item)
    return result


def build_calendar(items: Iterable[DeadlineItem], year: int, month: int) -> list[CalendarDay]:
    grouped = group_by_day(items, year, month)
    return [CalendarDay(day=d, items=tuple(grouped.get(d, []))) for d in month_days(year, month)]


def upcoming(items: Iterable[DeadlineItem], days: int = 7, today: Optional[date] = None) -> list[DeadlineItem]:
    anchor = today or date.today()
    end = anchor + timedelta(days=days)
    return sorted((i for i in items if anchor <= i.due_date <= end), key=lambda x: x.due_date)


def overdue(items: Iterable[DeadlineItem], today: Optional[date] = None) -> list[DeadlineItem]:
    anchor = today or date.today()
    return sorted((i for i in items if i.due_date < anchor and i.status.lower() not in {"виконано", "completed"}), key=lambda x: x.due_date)
