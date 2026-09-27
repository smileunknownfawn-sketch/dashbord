from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable

DONE = {"done", "виконано", "Виконано", "completed"}
MONTHS_UA = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень", "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]


def _date(value: Any):
    if value is None or value == "": return None
    if isinstance(value, datetime): return value.date()
    if isinstance(value, date): return value
    try: return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError): return None


def _value(row: Any, key: str, default: Any = None) -> Any:
    if hasattr(row, "keys"): return row[key] if key in row.keys() else default
    return row.get(key, default)


def _status(value: Any) -> str: return str(value or "").strip().lower()


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
    def today(self) -> int: return self.due_today


def metrics(rows: Iterable[Any], anchor: date | None = None) -> Metrics:
    values = list(rows); anchor = anchor or date.today(); total = len(values)
    completed = overdue = due_today = urgent = 0
    for row in values:
        status = _status(_value(row, "status"))
        completed += status in DONE
        due = _date(_value(row, "deadline"))
        if due:
            overdue += due < anchor and status not in DONE
            # "today" means active items due today; completed items are no longer pending.
            due_today += due == anchor and status not in DONE
        urgent += str(_value(row, "priority", "")).strip() in {"Терміновий", "Критичний"}
    active = total - completed
    return Metrics(total, completed, active, overdue, due_today, urgent, round(completed / total * 100, 1) if total else 0.0, round(overdue / total * 100, 1) if total else 0.0)


def monthly(rows: Iterable[Any], year: int) -> list[dict[str, int]]:
    buckets = {m: {"отримано": 0, "виконано": 0, "прострочено": 0, "у_роботі": 0} for m in range(1, 13)}; today = date.today()
    for row in rows:
        received = _date(_value(row, "received_date"))
        if not received or received.year != year: continue
        b = buckets[received.month]; b["отримано"] += 1; status = _status(_value(row, "status")); due = _date(_value(row, "deadline"))
        if status in DONE: b["виконано"] += 1
        else:
            b["у_роботі"] += 1
            if due and due < today: b["прострочено"] += 1
    return [dict(month=m, **buckets[m]) for m in range(1, 13)]


def distribution(rows: Iterable[Any], field: str) -> dict[str, int]:
    return dict(Counter(str(_value(row, field, "Не вказано") or "Не вказано").strip() or "Не вказано" for row in rows))


def year_comparison(rows: Iterable[Any], year_a: int, year_b: int) -> dict[str, int]:
    values = list(rows)
    count_a = sum(1 for row in values if (_date(_value(row, "received_date")) or date.min).year == year_a)
    count_b = sum(1 for row in values if (_date(_value(row, "received_date")) or date.min).year == year_b)
    return {"year_a": count_a, "year_b": count_b, "difference": count_b - count_a}


def month_comparison(rows: Iterable[Any], year_a: int, month_a: int, year_b: int, month_b: int) -> dict[str, int]:
    values = list(rows)
    def count(year: int, month: int) -> int:
        return sum(1 for row in values if (d := _date(_value(row, "received_date"))) and d.year == year and d.month == month)
    first, second = count(year_a, month_a), count(year_b, month_b)
    return {"first": first, "second": second, "difference": second - first}


def available_years(rows: Iterable[Any]) -> list[int]:
    years = set()
    for row in rows:
        d = _date(_value(row, "received_date"))
        if d: years.add(d.year)
    return sorted(years)
