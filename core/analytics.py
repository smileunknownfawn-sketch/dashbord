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
        elif due and due < today:
            bucket["прострочено"] += 1
        else:
            bucket["у_роботі"] += 1
    return [{"month": m, **buckets[m]} for m in range(1, 13)]


def distribution(rows: Iterable[Any], field: str, fallback: str = "Не вказано") -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        try:
            value = row[field]
        except (KeyError, TypeError):
            value = None
        counter[str(value or fallback).strip()] += 1
    return dict(counter.most_common())


def responsible_table(rows: Iterable[Any]) -> list[dict[str, Any]]:
    groups: dict[str, list[Any]] = defaultdict(list)
    for row in rows:
        name = str(row["responsible"] or "Не вказано") if hasattr(row, "keys") else str(row.get("responsible") or "Не вказано")
        groups[name].append(row)
    result = []
    today = date.today()
    for name, items in sorted(groups.items(), key=lambda pair: len(pair[1]), reverse=True):
        total = len(items)
        done = sum(_status(x["status"] if hasattr(x, "keys") else x.get("status")) in DONE for x in items)
        overdue = 0
        for x in items:
            due = _date(x["deadline"] if hasattr(x, "keys") else x.get("deadline"))
            st = _status(x["status"] if hasattr(x, "keys") else x.get("status"))
            overdue += bool(due and due < today and st not in DONE)
        result.append({"відповідальний": name, "усього": total, "виконано": done, "у_роботі": total - done, "прострочено": overdue, "відсоток": round(done / total * 100, 1) if total else 0})
    return result


def workload_index(rows: Iterable[Any]) -> float:
    values = list(rows)
    if not values:
        return 0.0
    m = metrics(values)
    return round(m.active + m.overdue * 2 + m.urgent * 1.5, 1)


def response_rate(rows: Iterable[Any], responses: Iterable[Any]) -> float:
    order_ids = {r["id"] for r in rows}
    answered = {r["order_id"] for r in responses if r["order_id"] in order_ids}
    return round(len(answered) / len(order_ids) * 100, 1) if order_ids else 0.0


def category_counts(rows: Iterable[Any]) -> dict[str, int]:
    return distribution(rows, "category", "Інше")


def responsible_counts(rows: Iterable[Any]) -> dict[str, int]:
    return distribution(rows, "responsible", "Не визначено")


def monthly_received(rows: Iterable[Any], year: int) -> list[int]:
    return [x["отримано"] for x in monthly(rows, year)]


def monthly_completed(rows: Iterable[Any], year: int) -> list[int]:
    return [x["виконано"] for x in monthly(rows, year)]


def monthly_deadlines(rows: Iterable[Any], year: int) -> list[int]:
    result = [0] * 12
    for row in rows:
        d = _date(row["deadline"] if hasattr(row, "keys") else row.get("deadline"))
        if d and d.year == year:
            result[d.month - 1] += 1
    return result


def available_years(rows: Iterable[Any]) -> list[int]:
    years = set()
    for row in rows:
        d = _date(row["received_date"] if hasattr(row, "keys") else row.get("received_date"))
        if d:
            years.add(d.year)
    years.add(date.today().year)
    return sorted(years, reverse=True)


def yearly_received(rows: Iterable[Any]) -> dict[int, int]:
    return {y: sum(monthly_received(rows, y)) for y in available_years(rows)}


def year_comparison(rows: Iterable[Any], year_a: int, year_b: int) -> dict[str, int]:
    a = sum(monthly_received(rows, year_a))
    b = sum(monthly_received(rows, year_b))
    return {"year_a": a, "year_b": b, "difference": b - a}


def month_comparison(rows: Iterable[Any], year_a: int, month_a: int, year_b: int, month_b: int) -> dict[str, int]:
    a = monthly_received(rows, year_a)[month_a - 1]
    b = monthly_received(rows, year_b)[month_b - 1]
    return {"first": a, "second": b, "difference": b - a}
