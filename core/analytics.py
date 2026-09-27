from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable

DONE = {"done", "виконано", "Виконано", "completed"}
MONTHS_UA = [
    "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
    "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень",
]


def _date(value: Any):
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def _status(value: Any) -> str:
    return str(value or "").strip().lower()


@dataclass(frozen=True)
class Metrics:
    total: int
    completed: int
    active: int
    overdue: int
    due_today: int
    urgent: int
    completion_rate: float
    overdue_rate: float

    @property
    def today(self) -> int:
        """Backward-compatible alias used by existing UI/tests."""
        return self.due_today


def metrics(rows: Iterable[Any], anchor: date | None = None) -> Metrics:
    values = list(rows)
    anchor = anchor or date.today()
    total = len(values)
    completed = 0
    overdue = 0
    due_today = 0
    urgent = 0
    for row in values:
        status = _status(row["status"] if hasattr(row, "keys") else row.get("status"))
        if status in DONE:
            completed += 1
        due = _date(row["deadline"] if hasattr(row, "keys") else row.get("deadline"))
        if due:
            overdue += bool(due < anchor and status not in DONE)
            due_today += due == anchor
        priority = str(row["priority"] if hasattr(row, "keys") else row.get("priority") or "").strip()
        urgent += priority in {"Терміновий", "Критичний"}
    active = total - completed
    return Metrics(
        total, completed, active, overdue, due_today, urgent,
        round(completed / total * 100, 1) if total else 0.0,
        round(overdue / total * 100, 1) if total else 0.0,
    )


def monthly(rows: Iterable[Any], year: int) -> list[dict[str, int]]:
    buckets = {month: {"отримано": 0, "виконано": 0, "прострочено": 0, "у_роботі": 0} for month in range(1, 13)}
    today = date.today()
    for row in rows:
        received = _date(row["received_date"] if hasattr(row, "keys") else row.get("received_date"))
        if received is None or received.year != year:
            continue
        bucket = buckets[received.month]
        bucket["отримано"] += 1
        status = _status(row["status"] if hasattr(row, "keys") else row.get("status"))
        due = _date(row["deadline"] if hasattr(row, "keys") else row.get("deadline"))
        if status in DONE:
            bucket["виконано"] += 1
        else:
            bucket["у_роботі"] += 1
            if due and due < today:
                bucket["прострочено"] += 1
    return [dict(month=month, **buckets[month]) for month in range(1, 13)]


def distribution(rows: Iterable[Any], field: str) -> dict[str, int]:
    values = []
    for row in rows:
        value = row[field] if hasattr(row, "keys") else row.get(field)
        value = str(value or "Не вказано").strip() or "Не вказано"
        values.append(value)
    return dict(Counter(values))


def year_comparison(rows: Iterable[Any], year_a: int, year_b: int) -> dict[str, int]:
    values = list(rows)
    count_a = sum(1 for row in values if (_date(row["received_date"] if hasattr(row, "keys") else row.get("received_date")) or date.min).year == year_a)
    count_b = sum(1 for row in values if (_date(row["received_date"] if hasattr(row, "keys") else row.get("received_date")) or date.min).year == year_b)
    return {"year_a": count_a, "year_b": count_b, "difference": count_b - count_a}


def month_comparison(rows: Iterable[Any], year_a: int, month_a: int, year_b: int, month_b: int) -> dict[str, int]:
    values = list(rows)
    def count(year: int, month: int) -> int:
        return sum(1 for row in values if (d := _date(row["received_date"] if hasattr(row, "keys") else row.get("received_date"))) and d.year == year and d.month == month)
    first = count(year_a, month_a)
    second = count(year_b, month_b)
    return {"first": first, "second": second, "difference": second - first}


def available_years(rows: Iterable[Any]) -> list[int]:
    years = set()
    for row in rows:
        d = _date(row["received_date"] if hasattr(row, "keys") else row.get("received_date"))
        if d:
            years.add(d.year)
    return sorted(years)
