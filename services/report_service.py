"""Local report calculations and export preparation."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from collections import Counter
from typing import Iterable, Any

@dataclass(frozen=True)
class ReportSummary:
    total: int
    completed: int
    active: int
    overdue: int
    due_today: int
    completion_rate: float


def _status(value: Any) -> str:
    return str(value or "").strip().lower()


def summarize(rows: Iterable[dict[str, Any]], today: date | None = None) -> ReportSummary:
    items = list(rows)
    anchor = today or date.today()
    total = len(items)
    completed = sum(_status(r.get("status")) in {"виконано", "completed", "done"} for r in items)
    overdue = 0
    due_today = 0
    for row in items:
        if _status(row.get("status")) in {"виконано", "completed", "done"}:
            continue
        raw = row.get("due_date") or row.get("deadline")
        try:
            due = raw if isinstance(raw, date) else datetime.strptime(str(raw), "%Y-%m-%d").date()
        except (TypeError, ValueError):
            continue
        overdue += due < anchor
        due_today += due == anchor
    active = total - completed
    return ReportSummary(total, completed, active, overdue, due_today, round(completed / total * 100, 1) if total else 0.0)


def by_month(rows: Iterable[dict[str, Any]], field: str = "received_date") -> dict[str, int]:
    result = Counter()
    for row in rows:
        value = row.get(field)
        try:
            parsed = value if isinstance(value, date) else datetime.strptime(str(value), "%Y-%m-%d").date()
        except (TypeError, ValueError):
            continue
        result[parsed.strftime("%Y-%m")] += 1
    return dict(sorted(result.items()))


def by_field(rows: Iterable[dict[str, Any]], field: str, fallback: str = "Не вказано") -> dict[str, int]:
    counter = Counter(str(row.get(field) or fallback).strip() for row in rows)
    return dict(counter.most_common())


def completion_by_month(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for row in rows:
        value = row.get("received_date")
        try:
            parsed = value if isinstance(value, date) else datetime.strptime(str(value), "%Y-%m-%d").date()
        except (TypeError, ValueError):
            continue
        key = parsed.strftime("%Y-%m")
        bucket = result.setdefault(key, {"отримано": 0, "виконано": 0, "прострочено": 0, "у_роботі": 0})
        bucket["отримано"] += 1
        status = _status(row.get("status"))
        if status in {"виконано", "completed", "done"}:
            bucket["виконано"] += 1
        else:
            bucket["у_роботі"] += 1
    return dict(sorted(result.items()))
