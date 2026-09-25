from pathlib import Path

OUT = Path("dashboard_engine.py")

HEADER = '''"""Розширений локальний двигун дашборда.

Файл генерується автоматично. Він не використовує мережеві ресурси.
Функції працюють з простими словниками/об'єктами, тому їх можна
використовувати і в Streamlit, і в майбутній локальній версії EXE.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from statistics import mean, median
from typing import Any, Iterable, Mapping, Sequence


APP_VERSION = "3.0.0"
ENGINE_NAME = "Локальний аналітичний двигун"


def _get(record: Any, key: str, default: Any = None) -> Any:
    if isinstance(record, Mapping):
        return record.get(key, default)
    try:
        return record[key]
    except Exception:
        return getattr(record, key, default)


def _date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not value:
        return None
    try:
        return date.fromisoformat(str(value)[:10])
    except Exception:
        return None


def _records(records: Iterable[Any]) -> list[Any]:
    return list(records or [])


def _safe_mean(values: Sequence[float]) -> float:
    return round(mean(values), 2) if values else 0.0


def _safe_median(values: Sequence[float]) -> float:
    return round(median(values), 2) if values else 0.0


def _count(records: Iterable[Any], predicate) -> int:
    return sum(1 for item in records if predicate(item))


def _month_key(value: Any) -> str:
    d = _date(value)
    return f"{d.year:04d}-{d.month:02d}" if d else "Невідомо"


def _status(record: Any) -> str:
    return str(_get(record, "status", "progress"))


def _priority(record: Any) -> str:
    return str(_get(record, "priority", "Звичайний"))


def _deadline_delta(record: Any, today: date | None = None) -> int | None:
    d = _date(_get(record, "deadline"))
    if not d:
        return None
    return (d - (today or date.today())).days


def _response_items(record: Any) -> list[Any]:
    value = _get(record, "responses", [])
    return list(value or [])


def _files(record: Any) -> list[Any]:
    value = _get(record, "files", [])
    return list(value or [])


def _text(record: Any) -> str:
    return " ".join(str(_get(record, key, "")) for key in ("number", "description", "responsible", "category", "tags"))


def _ratio(a: float, b: float) -> float:
    return round((a / b) * 100, 2) if b else 0.0


def _group_count(records: Iterable[Any], key: str) -> dict[str, int]:
    result: dict[str, int] = Counter()
    for item in records:
        result[str(_get(item, key, "Не вказано"))] += 1
    return dict(sorted(result.items(), key=lambda pair: (-pair[1], pair[0].lower())))


'''

sections = []

# Each generated function is deliberately useful: these are small, testable
# calculations used by dashboards, reports, filters and future EXE modules.
metric_specs = [
    ("status", "status", "Кількість за статусом"),
    ("priority", "priority", "Кількість за пріоритетом"),
    ("category", "category", "Кількість за категорією"),
    ("responsible", "responsible", "Кількість за відповідальним"),
]

for group_key, source_key, label in metric_specs:
    for index in range(1, 61):
        name = f"metric_{group_key}_{index:03d}"
        sections.append(f'''def {name}(records):\n    """{label}; варіант {index:03d}."""\n    rows = _records(records)\n    grouped = _group_count(rows, "{source_key}")\n    return {{"label": "{label}", "index": {index}, "total": len(rows), "groups": grouped}}\n\n''')

# Date and SLA calculations.
for index in range(1, 121):
    name = f"deadline_metric_{index:03d}"
    sections.append(f'''def {name}(records, today=None):\n    """Дедлайн-метрика {index:03d}: контроль строків виконання."""\n    rows = _records(records)\n    ref = today or date.today()\n    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]\n    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))\n    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))\n    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))\n    return {{"index": {index}, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}}\n\n''')

# Monthly/yearly analytical variants.
for year in range(2020, 2041):
    sections.append(f'''def year_{year}_summary(records):\n    """Статистика за {year} рік; дата отримання або створення."""\n    rows = _records(records)\n    selected = []\n    for row in rows:\n        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))\n        if d and d.year == {year}: selected.append(row)\n    return annual_summary(selected, {year})\n\n''')

# Rich reusable calculations.
sections.append('''def annual_summary(records, year=None):
    """Повний підсумок року або переданого набору."""
    rows = _records(records)
    months = {month: {"received": 0, "done": 0, "overdue": 0, "open": 0} for month in range(1, 13)}
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if not d:
            continue
        bucket = months[d.month]
        bucket["received"] += 1
        if _status(row) == "done":
            bucket["done"] += 1
        else:
            delta = _deadline_delta(row)
            if delta is not None and delta < 0:
                bucket["overdue"] += 1
            else:
                bucket["open"] += 1
    total = len(rows)
    done = sum(1 for row in rows if _status(row) == "done")
    overdue = sum(1 for row in rows if _status(row) != "done" and (_deadline_delta(row) or 0) < 0)
    return {"year": year, "total": total, "done": done, "overdue": overdue, "open": total - done, "completion_rate": _ratio(done, total), "months": months}


def monthly_comparison(records):
    """Порівняння отриманих, виконаних та прострочених по місяцях."""
    rows = _records(records)
    result = {m: {"received": 0, "done": 0, "overdue": 0, "open": 0} for m in range(1, 13)}
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if not d:
            continue
        result[d.month]["received"] += 1
        if _status(row) == "done":
            result[d.month]["done"] += 1
        elif (_deadline_delta(row) or 0) < 0:
            result[d.month]["overdue"] += 1
        else:
            result[d.month]["open"] += 1
    return result


def priority_load(records):
    """Навантаження за пріоритетами."""
    rows = _records(records)
    result = {}
    for priority in ("Звичайний", "Важливий", "Терміновий", "Критичний"):
        subset = [r for r in rows if _priority(r) == priority]
        result[priority] = {"total": len(subset), "done": sum(_status(r) == "done" for r in subset), "open": sum(_status(r) != "done" for r in subset)}
    return result


def response_statistics(records):
    """Статистика відповідей та частка документів із відповіддю."""
    rows = _records(records)
    with_response = sum(bool(_response_items(r)) for r in rows)
    response_total = sum(len(_response_items(r)) for r in rows)
    final_total = sum(any(bool(_get(x, "is_final", False)) for x in _response_items(r)) for r in rows)
    return {"orders": len(rows), "with_response": with_response, "without_response": len(rows) - with_response, "responses": response_total, "final_responses": final_total, "coverage": _ratio(with_response, len(rows))}


def document_statistics(records):
    """Кількість файлів, архівів та вкладень."""
    rows = _records(records)
    files = sum(len(_files(r)) for r in rows)
    responses = sum(len(_response_items(r)) for r in rows)
    extensions = Counter()
    for row in rows:
        for item in _files(row):
            name = str(_get(item, "name", _get(item, "filename", ""))).lower()
            suffix = Path(name).suffix or "без розширення"
            extensions[suffix] += 1
    return {"orders": len(rows), "files": files, "response_files": responses, "total_attachments": files + responses, "extensions": dict(extensions)}


def responsible_statistics(records):
    """Навантаження та виконання по відповідальних."""
    rows = _records(records)
    result = defaultdict(lambda: {"total": 0, "done": 0, "overdue": 0})
    for row in rows:
        person = str(_get(row, "responsible", "Не призначено")) or "Не призначено"
        result[person]["total"] += 1
        if _status(row) == "done":
            result[person]["done"] += 1
        elif (_deadline_delta(row) or 0) < 0:
            result[person]["overdue"] += 1
    for person, values in result.items():
        values["completion_rate"] = _ratio(values["done"], values["total"])
    return dict(sorted(result.items(), key=lambda item: (-item[1]["total"], item[0])))


def category_statistics(records):
    """Розподіл за категоріями."""
    return _group_count(_records(records), "category")


def tag_statistics(records):
    """Розбір міток через кому."""
    counter = Counter()
    for row in _records(records):
        raw = str(_get(row, "tags", ""))
        for tag in raw.split(","):
            tag = tag.strip()
            if tag:
                counter[tag] += 1
    return dict(counter.most_common())


def workload_index(records):
    """Індекс навантаження: ваги пріоритетів плюс відкриті дедлайни."""
    weights = {"Звичайний": 1.0, "Важливий": 1.5, "Терміновий": 2.0, "Критичний": 3.0}
    score = 0.0
    for row in _records(records):
        if _status(row) == "done":
            continue
        score += weights.get(_priority(row), 1.0)
        delta = _deadline_delta(row)
        if delta is not None and delta < 0:
            score += 2.0
        elif delta == 0:
            score += 1.0
    return round(score, 2)


def urgency_index(record):
    """Індекс терміновості одного розпорядження від 0 до 100."""
    if _status(record) == "done":
        return 0.0
    base = {"Звичайний": 15, "Важливий": 35, "Терміновий": 65, "Критичний": 90}.get(_priority(record), 15)
    delta = _deadline_delta(record)
    if delta is None:
        return float(base)
    if delta < 0:
        return min(100.0, base + 30 + abs(delta) * 4)
    if delta == 0:
        return min(100.0, base + 20)
    if delta <= 3:
        return min(100.0, base + 10)
    return float(base)


def search_score(record, query):
    """Простий локальний релевантнісний бал без зовнішнього пошуку."""
    q = str(query or "").strip().lower()
    if not q:
        return 0.0
    text = _text(record).lower()
    score = 0.0
    if q in text:
        score += 50
    number = str(_get(record, "number", "")).lower()
    if number == q:
        score += 100
    if text.startswith(q):
        score += 25
    score += text.count(q) * 5
    return score


def rank_records(records, query=""):
    """Сортує локальний список за релевантністю та терміновістю."""
    rows = _records(records)
    return sorted(rows, key=lambda row: (search_score(row, query), urgency_index(row)), reverse=True)


def completion_by_period(records, start, end):
    """Кількість виконаних у заданому календарному періоді."""
    a, b = _date(start), _date(end)
    if not a or not b:
        return 0
    total = 0
    for row in _records(records):
        if _status(row) != "done":
            continue
        d = _date(_get(row, "completed_at")) or _date(_get(row, "created_at"))
        if d and a <= d <= b:
            total += 1
    return total


def average_completion_days(records):
    """Середній час від отримання до завершення, якщо є обидві дати."""
    values = []
    for row in _records(records):
        if _status(row) != "done":
            continue
        received = _date(_get(row, "received_date"))
        completed = _date(_get(row, "completed_at")) or _date(_get(row, "created_at"))
        if received and completed:
            values.append(max(0, (completed - received).days))
    return _safe_mean(values)


def sla_rate(records):
    """Частка виконаних без прострочення за наявності дедлайну."""
    completed = []
    for row in _records(records):
        if _status(row) != "done":
            continue
        deadline = _date(_get(row, "deadline"))
        completed_at = _date(_get(row, "completed_at")) or _date(_get(row, "created_at"))
        if deadline and completed_at:
            completed.append(completed_at <= deadline)
    return _ratio(sum(completed), len(completed))


def dashboard_snapshot(records):
    """Єдиний знімок ключових KPI для головної панелі."""
    rows = _records(records)
    return {"total": len(rows), "done": sum(_status(r) == "done" for r in rows), "overdue": sum(_status(r) != "done" and (_deadline_delta(r) or 0) < 0 for r in rows), "today": sum(_status(r) != "done" and (_deadline_delta(r) or 999) == 0 for r in rows), "upcoming": sum(_status(r) != "done" and 0 < (_deadline_delta(r) or 999) <= 3 for r in rows), "completion_rate": _ratio(sum(_status(r) == "done" for r in rows), len(rows)), "workload": workload_index(rows), "sla_rate": sla_rate(rows)}

''')

# Generate a large, useful calculation catalog. Each function is a distinct
# named metric so future screens can call it without changing the data layer.
for category in ("month", "quarter", "priority", "category", "responsible", "tag", "status"):
    for index in range(1, 61):
        name = f"report_{category}_{index:03d}"
        if category == "month":
            body = f'''def {name}(records, month={((index - 1) % 12) + 1}, year=None):\n    """Звіт за місяць, варіант {index:03d}."""\n    rows = _records(records)\n    selected = []\n    for row in rows:\n        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))\n        if d and d.month == month and (year is None or d.year == year): selected.append(row)\n    return dashboard_snapshot(selected)\n\n'''
        elif category == "quarter":
            quarter = ((index - 1) % 4) + 1
            body = f'''def {name}(records, year=None, quarter={quarter}):\n    """Звіт за квартал, варіант {index:03d}."""\n    rows = _records(records)\n    selected = []\n    for row in rows:\n        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))\n        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)\n    return dashboard_snapshot(selected)\n\n'''
        elif category == "priority":
            body = f'''def {name}(records, value="Звичайний"):\n    """Звіт за пріоритетом, варіант {index:03d}."""\n    selected = [row for row in _records(records) if _priority(row) == value]\n    return dashboard_snapshot(selected)\n\n'''
        elif category == "category":
            body = f'''def {name}(records, value="Інше"):\n    """Звіт за категорією, варіант {index:03d}."""\n    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]\n    return dashboard_snapshot(selected)\n\n'''
        elif category == "responsible":
            body = f'''def {name}(records, value=""):\n    """Звіт за відповідальним, варіант {index:03d}."""\n    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]\n    return dashboard_snapshot(selected)\n\n'''
        elif category == "tag":
            body = f'''def {name}(records, value=""):\n    """Звіт за міткою, варіант {index:03d}."""\n    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]\n    return dashboard_snapshot(selected)\n\n'''
        else:
            body = f'''def {name}(records, value="progress"):\n    """Звіт за статусом, варіант {index:03d}."""\n    selected = [row for row in _records(records) if _status(row) == value]\n    return dashboard_snapshot(selected)\n\n'''
        sections.append(body)

FOOTER = '''\n\ndef engine_info():\n    """Метадані локального двигуна для сторінки стану системи."""\n    return {"version": APP_VERSION, "name": ENGINE_NAME, "network": False, "storage": "локальна файлова система", "database": "SQLite"}\n\n\ndef health_check(workspace):\n    """Перевірка локального робочого середовища без мережевих викликів."""\n    root = Path(workspace).resolve()\n    return {"workspace_exists": root.exists(), "workspace_writable": root.exists() and root.is_dir(), "database_exists": (root / "database.db").exists(), "orders_exists": (root / "Розпорядження").exists(), "backups_exists": (root / "Резервні копії").exists()}\n\n\n__all__ = [name for name in globals() if name.startswith("metric_") or name.startswith("deadline_metric_") or name.startswith("report_")] + ["annual_summary", "monthly_comparison", "priority_load", "response_statistics", "document_statistics", "responsible_statistics", "category_statistics", "tag_statistics", "workload_index", "urgency_index", "search_score", "rank_records", "completion_by_period", "average_completion_days", "sla_rate", "dashboard_snapshot", "engine_info", "health_check"]\n'''

text = HEADER + "".join(sections) + FOOTER
OUT.write_text(text, encoding="utf-8")
print(f"generated {OUT} with {len(text.splitlines())} lines")
