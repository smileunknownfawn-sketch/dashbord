from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable

DONE = {"done", "completed", "виконано"}


def _date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not value:
        return None
    text = str(value)
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def _status(value: Any) -> str:
    return str(value or "").strip().lower()


@dataclass(frozen=True)
class Metrics:
    total: int
    completed: int
    active: int
    overdue: int
    today: int
    urgent: int
    completion_rate: float
    overdue_rate: float


def metrics(rows: Iterable[Any], today: date | None = None) -> Metrics:
    anchor = today or date.today()
    rows = list(rows)
    total = len(rows)
    completed = sum(_status(r["status"] if hasattr(r, "keys") else r.get("status")) in DONE for r in rows)
    overdue = 0
    due_today = 0
    urgent = 0
    for row in rows:
        status = _status(row["status"] if hasattr(row, "keys") else row.get("status"))
        priority = str(row["priority"] if hasattr(row, "keys") else row.get("priority", ""))
        due = _date(row["deadline"] if hasattr(row, "keys") else row.get("deadline"))
        if status in DONE or due is None:
            continue
        overdue += due < anchor
        due_today += due == anchor
        urgent += priority in {"Терміновий", "Критичний"}
    active = total - completed
    return Metrics(total, completed, active, overdue, due_today, urgent, round(completed / total * 100, 1) if total else 0.0, round(overdue / total * 100, 1) if total else 0.0)


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
        overdue = sum(_date(x["deadline"] if hasattr(x, "keys") else x.get("deadline")) is not None and _date(x["deadline"] if hasattr(x, "keys") else x.get("deadline")) < today and _status(x["status"] if hasattr(x, "keys") else x.get("status")) not in DONE for x in items)
        result.append({"відповідальний": name, "усього": total, "виконано": done, "у_роботі": total - done, "прострочено": overdue, "відсоток": round(done / total * 100, 1) if total else 0})
    return result


def workload_index(rows: Iterable[Any]) -> float:
    values = list(rows)
    if not values:
        return 0.0
    active = metrics(values).active
    overdue = metrics(values).overdue
    urgent = metrics(values).urgent
    return round(active + overdue * 2 + urgent * 1.5, 1)


def response_rate(rows: Iterable[Any], responses: Iterable[Any]) -> float:
    order_ids = {r["id"] for r in rows}
    answered = {r["order_id"] for r in responses if r["order_id"] in order_ids}
    return round(len(answered) / len(order_ids) * 100, 1) if order_ids else 0.0
