"""Reusable local statistics for dashboard cards and charts."""
from __future__ import annotations
from collections import Counter, defaultdict
from datetime import date, datetime
from typing import Iterable, Any

DONE = {"виконано", "completed", "done"}


def normalized_status(value: Any) -> str:
    return str(value or "").strip().lower()


def parse_day(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = str(value or "").strip()
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def status_counts(rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    result = {"виконано": 0, "у роботі": 0, "прострочено": 0, "сьогодні": 0}
    today = date.today()
    for row in rows:
        status = normalized_status(row.get("status"))
        if status in DONE:
            result["виконано"] += 1
            continue
        due = parse_day(row.get("deadline") or row.get("due_date"))
        if due and due < today:
            result["прострочено"] += 1
        elif due == today:
            result["сьогодні"] += 1
        else:
            result["у роботі"] += 1
    return result


def workload_by_responsible(rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(str(r.get("responsible") or "Не вказано").strip() for r in rows)
    return dict(counter.most_common())


def workload_by_category(rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(str(r.get("category") or "Інше").strip() for r in rows)
    return dict(counter.most_common())


def monthly_received(rows: Iterable[dict[str, Any]], year: int) -> dict[int, int]:
    result = {month: 0 for month in range(1, 13)}
    for row in rows:
        received = parse_day(row.get("received_date"))
        if received and received.year == year:
            result[received.month] += 1
    return result


def monthly_completed(rows: Iterable[dict[str, Any]], year: int) -> dict[int, int]:
    result = {month: 0 for month in range(1, 13)}
    for row in rows:
        if normalized_status(row.get("status")) not in DONE:
            continue
        completed = parse_day(row.get("completed_date")) or parse_day(row.get("updated_at"))
        if completed and completed.year == year:
            result[completed.month] += 1
    return result


def completion_rate(rows: Iterable[dict[str, Any]]) -> float:
    values = list(rows)
    if not values:
        return 0.0
    return round(sum(normalized_status(r.get("status")) in DONE for r in values) / len(values) * 100, 1)


def priority_counts(rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(str(r.get("priority") or "Звичайний").strip() for r in rows)
    return dict(counter.most_common())
