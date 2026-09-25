"""Розширений локальний двигун дашборда.

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


def metric_status_001(records):
    """Кількість за статусом; варіант 001."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 1, "total": len(rows), "groups": grouped}

def metric_status_002(records):
    """Кількість за статусом; варіант 002."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 2, "total": len(rows), "groups": grouped}

def metric_status_003(records):
    """Кількість за статусом; варіант 003."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 3, "total": len(rows), "groups": grouped}

def metric_status_004(records):
    """Кількість за статусом; варіант 004."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 4, "total": len(rows), "groups": grouped}

def metric_status_005(records):
    """Кількість за статусом; варіант 005."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 5, "total": len(rows), "groups": grouped}

def metric_status_006(records):
    """Кількість за статусом; варіант 006."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 6, "total": len(rows), "groups": grouped}

def metric_status_007(records):
    """Кількість за статусом; варіант 007."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 7, "total": len(rows), "groups": grouped}

def metric_status_008(records):
    """Кількість за статусом; варіант 008."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 8, "total": len(rows), "groups": grouped}

def metric_status_009(records):
    """Кількість за статусом; варіант 009."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 9, "total": len(rows), "groups": grouped}

def metric_status_010(records):
    """Кількість за статусом; варіант 010."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 10, "total": len(rows), "groups": grouped}

def metric_status_011(records):
    """Кількість за статусом; варіант 011."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 11, "total": len(rows), "groups": grouped}

def metric_status_012(records):
    """Кількість за статусом; варіант 012."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 12, "total": len(rows), "groups": grouped}

def metric_status_013(records):
    """Кількість за статусом; варіант 013."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 13, "total": len(rows), "groups": grouped}

def metric_status_014(records):
    """Кількість за статусом; варіант 014."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 14, "total": len(rows), "groups": grouped}

def metric_status_015(records):
    """Кількість за статусом; варіант 015."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 15, "total": len(rows), "groups": grouped}

def metric_status_016(records):
    """Кількість за статусом; варіант 016."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 16, "total": len(rows), "groups": grouped}

def metric_status_017(records):
    """Кількість за статусом; варіант 017."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 17, "total": len(rows), "groups": grouped}

def metric_status_018(records):
    """Кількість за статусом; варіант 018."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 18, "total": len(rows), "groups": grouped}

def metric_status_019(records):
    """Кількість за статусом; варіант 019."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 19, "total": len(rows), "groups": grouped}

def metric_status_020(records):
    """Кількість за статусом; варіант 020."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 20, "total": len(rows), "groups": grouped}

def metric_status_021(records):
    """Кількість за статусом; варіант 021."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 21, "total": len(rows), "groups": grouped}

def metric_status_022(records):
    """Кількість за статусом; варіант 022."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 22, "total": len(rows), "groups": grouped}

def metric_status_023(records):
    """Кількість за статусом; варіант 023."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 23, "total": len(rows), "groups": grouped}

def metric_status_024(records):
    """Кількість за статусом; варіант 024."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 24, "total": len(rows), "groups": grouped}

def metric_status_025(records):
    """Кількість за статусом; варіант 025."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 25, "total": len(rows), "groups": grouped}

def metric_status_026(records):
    """Кількість за статусом; варіант 026."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 26, "total": len(rows), "groups": grouped}

def metric_status_027(records):
    """Кількість за статусом; варіант 027."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 27, "total": len(rows), "groups": grouped}

def metric_status_028(records):
    """Кількість за статусом; варіант 028."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 28, "total": len(rows), "groups": grouped}

def metric_status_029(records):
    """Кількість за статусом; варіант 029."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 29, "total": len(rows), "groups": grouped}

def metric_status_030(records):
    """Кількість за статусом; варіант 030."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 30, "total": len(rows), "groups": grouped}

def metric_status_031(records):
    """Кількість за статусом; варіант 031."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 31, "total": len(rows), "groups": grouped}

def metric_status_032(records):
    """Кількість за статусом; варіант 032."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 32, "total": len(rows), "groups": grouped}

def metric_status_033(records):
    """Кількість за статусом; варіант 033."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 33, "total": len(rows), "groups": grouped}

def metric_status_034(records):
    """Кількість за статусом; варіант 034."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 34, "total": len(rows), "groups": grouped}

def metric_status_035(records):
    """Кількість за статусом; варіант 035."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 35, "total": len(rows), "groups": grouped}

def metric_status_036(records):
    """Кількість за статусом; варіант 036."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 36, "total": len(rows), "groups": grouped}

def metric_status_037(records):
    """Кількість за статусом; варіант 037."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 37, "total": len(rows), "groups": grouped}

def metric_status_038(records):
    """Кількість за статусом; варіант 038."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 38, "total": len(rows), "groups": grouped}

def metric_status_039(records):
    """Кількість за статусом; варіант 039."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 39, "total": len(rows), "groups": grouped}

def metric_status_040(records):
    """Кількість за статусом; варіант 040."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 40, "total": len(rows), "groups": grouped}

def metric_status_041(records):
    """Кількість за статусом; варіант 041."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 41, "total": len(rows), "groups": grouped}

def metric_status_042(records):
    """Кількість за статусом; варіант 042."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 42, "total": len(rows), "groups": grouped}

def metric_status_043(records):
    """Кількість за статусом; варіант 043."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 43, "total": len(rows), "groups": grouped}

def metric_status_044(records):
    """Кількість за статусом; варіант 044."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 44, "total": len(rows), "groups": grouped}

def metric_status_045(records):
    """Кількість за статусом; варіант 045."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 45, "total": len(rows), "groups": grouped}

def metric_status_046(records):
    """Кількість за статусом; варіант 046."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 46, "total": len(rows), "groups": grouped}

def metric_status_047(records):
    """Кількість за статусом; варіант 047."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 47, "total": len(rows), "groups": grouped}

def metric_status_048(records):
    """Кількість за статусом; варіант 048."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 48, "total": len(rows), "groups": grouped}

def metric_status_049(records):
    """Кількість за статусом; варіант 049."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 49, "total": len(rows), "groups": grouped}

def metric_status_050(records):
    """Кількість за статусом; варіант 050."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 50, "total": len(rows), "groups": grouped}

def metric_status_051(records):
    """Кількість за статусом; варіант 051."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 51, "total": len(rows), "groups": grouped}

def metric_status_052(records):
    """Кількість за статусом; варіант 052."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 52, "total": len(rows), "groups": grouped}

def metric_status_053(records):
    """Кількість за статусом; варіант 053."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 53, "total": len(rows), "groups": grouped}

def metric_status_054(records):
    """Кількість за статусом; варіант 054."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 54, "total": len(rows), "groups": grouped}

def metric_status_055(records):
    """Кількість за статусом; варіант 055."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 55, "total": len(rows), "groups": grouped}

def metric_status_056(records):
    """Кількість за статусом; варіант 056."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 56, "total": len(rows), "groups": grouped}

def metric_status_057(records):
    """Кількість за статусом; варіант 057."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 57, "total": len(rows), "groups": grouped}

def metric_status_058(records):
    """Кількість за статусом; варіант 058."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 58, "total": len(rows), "groups": grouped}

def metric_status_059(records):
    """Кількість за статусом; варіант 059."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 59, "total": len(rows), "groups": grouped}

def metric_status_060(records):
    """Кількість за статусом; варіант 060."""
    rows = _records(records)
    grouped = _group_count(rows, "status")
    return {"label": "Кількість за статусом", "index": 60, "total": len(rows), "groups": grouped}

def metric_priority_001(records):
    """Кількість за пріоритетом; варіант 001."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 1, "total": len(rows), "groups": grouped}

def metric_priority_002(records):
    """Кількість за пріоритетом; варіант 002."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 2, "total": len(rows), "groups": grouped}

def metric_priority_003(records):
    """Кількість за пріоритетом; варіант 003."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 3, "total": len(rows), "groups": grouped}

def metric_priority_004(records):
    """Кількість за пріоритетом; варіант 004."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 4, "total": len(rows), "groups": grouped}

def metric_priority_005(records):
    """Кількість за пріоритетом; варіант 005."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 5, "total": len(rows), "groups": grouped}

def metric_priority_006(records):
    """Кількість за пріоритетом; варіант 006."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 6, "total": len(rows), "groups": grouped}

def metric_priority_007(records):
    """Кількість за пріоритетом; варіант 007."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 7, "total": len(rows), "groups": grouped}

def metric_priority_008(records):
    """Кількість за пріоритетом; варіант 008."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 8, "total": len(rows), "groups": grouped}

def metric_priority_009(records):
    """Кількість за пріоритетом; варіант 009."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 9, "total": len(rows), "groups": grouped}

def metric_priority_010(records):
    """Кількість за пріоритетом; варіант 010."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 10, "total": len(rows), "groups": grouped}

def metric_priority_011(records):
    """Кількість за пріоритетом; варіант 011."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 11, "total": len(rows), "groups": grouped}

def metric_priority_012(records):
    """Кількість за пріоритетом; варіант 012."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 12, "total": len(rows), "groups": grouped}

def metric_priority_013(records):
    """Кількість за пріоритетом; варіант 013."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 13, "total": len(rows), "groups": grouped}

def metric_priority_014(records):
    """Кількість за пріоритетом; варіант 014."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 14, "total": len(rows), "groups": grouped}

def metric_priority_015(records):
    """Кількість за пріоритетом; варіант 015."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 15, "total": len(rows), "groups": grouped}

def metric_priority_016(records):
    """Кількість за пріоритетом; варіант 016."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 16, "total": len(rows), "groups": grouped}

def metric_priority_017(records):
    """Кількість за пріоритетом; варіант 017."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 17, "total": len(rows), "groups": grouped}

def metric_priority_018(records):
    """Кількість за пріоритетом; варіант 018."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 18, "total": len(rows), "groups": grouped}

def metric_priority_019(records):
    """Кількість за пріоритетом; варіант 019."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 19, "total": len(rows), "groups": grouped}

def metric_priority_020(records):
    """Кількість за пріоритетом; варіант 020."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 20, "total": len(rows), "groups": grouped}

def metric_priority_021(records):
    """Кількість за пріоритетом; варіант 021."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 21, "total": len(rows), "groups": grouped}

def metric_priority_022(records):
    """Кількість за пріоритетом; варіант 022."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 22, "total": len(rows), "groups": grouped}

def metric_priority_023(records):
    """Кількість за пріоритетом; варіант 023."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 23, "total": len(rows), "groups": grouped}

def metric_priority_024(records):
    """Кількість за пріоритетом; варіант 024."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 24, "total": len(rows), "groups": grouped}

def metric_priority_025(records):
    """Кількість за пріоритетом; варіант 025."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 25, "total": len(rows), "groups": grouped}

def metric_priority_026(records):
    """Кількість за пріоритетом; варіант 026."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 26, "total": len(rows), "groups": grouped}

def metric_priority_027(records):
    """Кількість за пріоритетом; варіант 027."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 27, "total": len(rows), "groups": grouped}

def metric_priority_028(records):
    """Кількість за пріоритетом; варіант 028."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 28, "total": len(rows), "groups": grouped}

def metric_priority_029(records):
    """Кількість за пріоритетом; варіант 029."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 29, "total": len(rows), "groups": grouped}

def metric_priority_030(records):
    """Кількість за пріоритетом; варіант 030."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 30, "total": len(rows), "groups": grouped}

def metric_priority_031(records):
    """Кількість за пріоритетом; варіант 031."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 31, "total": len(rows), "groups": grouped}

def metric_priority_032(records):
    """Кількість за пріоритетом; варіант 032."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 32, "total": len(rows), "groups": grouped}

def metric_priority_033(records):
    """Кількість за пріоритетом; варіант 033."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 33, "total": len(rows), "groups": grouped}

def metric_priority_034(records):
    """Кількість за пріоритетом; варіант 034."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 34, "total": len(rows), "groups": grouped}

def metric_priority_035(records):
    """Кількість за пріоритетом; варіант 035."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 35, "total": len(rows), "groups": grouped}

def metric_priority_036(records):
    """Кількість за пріоритетом; варіант 036."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 36, "total": len(rows), "groups": grouped}

def metric_priority_037(records):
    """Кількість за пріоритетом; варіант 037."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 37, "total": len(rows), "groups": grouped}

def metric_priority_038(records):
    """Кількість за пріоритетом; варіант 038."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 38, "total": len(rows), "groups": grouped}

def metric_priority_039(records):
    """Кількість за пріоритетом; варіант 039."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 39, "total": len(rows), "groups": grouped}

def metric_priority_040(records):
    """Кількість за пріоритетом; варіант 040."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 40, "total": len(rows), "groups": grouped}

def metric_priority_041(records):
    """Кількість за пріоритетом; варіант 041."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 41, "total": len(rows), "groups": grouped}

def metric_priority_042(records):
    """Кількість за пріоритетом; варіант 042."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 42, "total": len(rows), "groups": grouped}

def metric_priority_043(records):
    """Кількість за пріоритетом; варіант 043."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 43, "total": len(rows), "groups": grouped}

def metric_priority_044(records):
    """Кількість за пріоритетом; варіант 044."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 44, "total": len(rows), "groups": grouped}

def metric_priority_045(records):
    """Кількість за пріоритетом; варіант 045."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 45, "total": len(rows), "groups": grouped}

def metric_priority_046(records):
    """Кількість за пріоритетом; варіант 046."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 46, "total": len(rows), "groups": grouped}

def metric_priority_047(records):
    """Кількість за пріоритетом; варіант 047."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 47, "total": len(rows), "groups": grouped}

def metric_priority_048(records):
    """Кількість за пріоритетом; варіант 048."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 48, "total": len(rows), "groups": grouped}

def metric_priority_049(records):
    """Кількість за пріоритетом; варіант 049."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 49, "total": len(rows), "groups": grouped}

def metric_priority_050(records):
    """Кількість за пріоритетом; варіант 050."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 50, "total": len(rows), "groups": grouped}

def metric_priority_051(records):
    """Кількість за пріоритетом; варіант 051."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 51, "total": len(rows), "groups": grouped}

def metric_priority_052(records):
    """Кількість за пріоритетом; варіант 052."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 52, "total": len(rows), "groups": grouped}

def metric_priority_053(records):
    """Кількість за пріоритетом; варіант 053."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 53, "total": len(rows), "groups": grouped}

def metric_priority_054(records):
    """Кількість за пріоритетом; варіант 054."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 54, "total": len(rows), "groups": grouped}

def metric_priority_055(records):
    """Кількість за пріоритетом; варіант 055."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 55, "total": len(rows), "groups": grouped}

def metric_priority_056(records):
    """Кількість за пріоритетом; варіант 056."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 56, "total": len(rows), "groups": grouped}

def metric_priority_057(records):
    """Кількість за пріоритетом; варіант 057."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 57, "total": len(rows), "groups": grouped}

def metric_priority_058(records):
    """Кількість за пріоритетом; варіант 058."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 58, "total": len(rows), "groups": grouped}

def metric_priority_059(records):
    """Кількість за пріоритетом; варіант 059."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 59, "total": len(rows), "groups": grouped}

def metric_priority_060(records):
    """Кількість за пріоритетом; варіант 060."""
    rows = _records(records)
    grouped = _group_count(rows, "priority")
    return {"label": "Кількість за пріоритетом", "index": 60, "total": len(rows), "groups": grouped}

def metric_category_001(records):
    """Кількість за категорією; варіант 001."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 1, "total": len(rows), "groups": grouped}

def metric_category_002(records):
    """Кількість за категорією; варіант 002."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 2, "total": len(rows), "groups": grouped}

def metric_category_003(records):
    """Кількість за категорією; варіант 003."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 3, "total": len(rows), "groups": grouped}

def metric_category_004(records):
    """Кількість за категорією; варіант 004."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 4, "total": len(rows), "groups": grouped}

def metric_category_005(records):
    """Кількість за категорією; варіант 005."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 5, "total": len(rows), "groups": grouped}

def metric_category_006(records):
    """Кількість за категорією; варіант 006."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 6, "total": len(rows), "groups": grouped}

def metric_category_007(records):
    """Кількість за категорією; варіант 007."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 7, "total": len(rows), "groups": grouped}

def metric_category_008(records):
    """Кількість за категорією; варіант 008."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 8, "total": len(rows), "groups": grouped}

def metric_category_009(records):
    """Кількість за категорією; варіант 009."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 9, "total": len(rows), "groups": grouped}

def metric_category_010(records):
    """Кількість за категорією; варіант 010."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 10, "total": len(rows), "groups": grouped}

def metric_category_011(records):
    """Кількість за категорією; варіант 011."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 11, "total": len(rows), "groups": grouped}

def metric_category_012(records):
    """Кількість за категорією; варіант 012."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 12, "total": len(rows), "groups": grouped}

def metric_category_013(records):
    """Кількість за категорією; варіант 013."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 13, "total": len(rows), "groups": grouped}

def metric_category_014(records):
    """Кількість за категорією; варіант 014."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 14, "total": len(rows), "groups": grouped}

def metric_category_015(records):
    """Кількість за категорією; варіант 015."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 15, "total": len(rows), "groups": grouped}

def metric_category_016(records):
    """Кількість за категорією; варіант 016."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 16, "total": len(rows), "groups": grouped}

def metric_category_017(records):
    """Кількість за категорією; варіант 017."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 17, "total": len(rows), "groups": grouped}

def metric_category_018(records):
    """Кількість за категорією; варіант 018."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 18, "total": len(rows), "groups": grouped}

def metric_category_019(records):
    """Кількість за категорією; варіант 019."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 19, "total": len(rows), "groups": grouped}

def metric_category_020(records):
    """Кількість за категорією; варіант 020."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 20, "total": len(rows), "groups": grouped}

def metric_category_021(records):
    """Кількість за категорією; варіант 021."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 21, "total": len(rows), "groups": grouped}

def metric_category_022(records):
    """Кількість за категорією; варіант 022."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 22, "total": len(rows), "groups": grouped}

def metric_category_023(records):
    """Кількість за категорією; варіант 023."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 23, "total": len(rows), "groups": grouped}

def metric_category_024(records):
    """Кількість за категорією; варіант 024."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 24, "total": len(rows), "groups": grouped}

def metric_category_025(records):
    """Кількість за категорією; варіант 025."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 25, "total": len(rows), "groups": grouped}

def metric_category_026(records):
    """Кількість за категорією; варіант 026."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 26, "total": len(rows), "groups": grouped}

def metric_category_027(records):
    """Кількість за категорією; варіант 027."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 27, "total": len(rows), "groups": grouped}

def metric_category_028(records):
    """Кількість за категорією; варіант 028."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 28, "total": len(rows), "groups": grouped}

def metric_category_029(records):
    """Кількість за категорією; варіант 029."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 29, "total": len(rows), "groups": grouped}

def metric_category_030(records):
    """Кількість за категорією; варіант 030."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 30, "total": len(rows), "groups": grouped}

def metric_category_031(records):
    """Кількість за категорією; варіант 031."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 31, "total": len(rows), "groups": grouped}

def metric_category_032(records):
    """Кількість за категорією; варіант 032."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 32, "total": len(rows), "groups": grouped}

def metric_category_033(records):
    """Кількість за категорією; варіант 033."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 33, "total": len(rows), "groups": grouped}

def metric_category_034(records):
    """Кількість за категорією; варіант 034."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 34, "total": len(rows), "groups": grouped}

def metric_category_035(records):
    """Кількість за категорією; варіант 035."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 35, "total": len(rows), "groups": grouped}

def metric_category_036(records):
    """Кількість за категорією; варіант 036."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 36, "total": len(rows), "groups": grouped}

def metric_category_037(records):
    """Кількість за категорією; варіант 037."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 37, "total": len(rows), "groups": grouped}

def metric_category_038(records):
    """Кількість за категорією; варіант 038."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 38, "total": len(rows), "groups": grouped}

def metric_category_039(records):
    """Кількість за категорією; варіант 039."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 39, "total": len(rows), "groups": grouped}

def metric_category_040(records):
    """Кількість за категорією; варіант 040."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 40, "total": len(rows), "groups": grouped}

def metric_category_041(records):
    """Кількість за категорією; варіант 041."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 41, "total": len(rows), "groups": grouped}

def metric_category_042(records):
    """Кількість за категорією; варіант 042."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 42, "total": len(rows), "groups": grouped}

def metric_category_043(records):
    """Кількість за категорією; варіант 043."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 43, "total": len(rows), "groups": grouped}

def metric_category_044(records):
    """Кількість за категорією; варіант 044."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 44, "total": len(rows), "groups": grouped}

def metric_category_045(records):
    """Кількість за категорією; варіант 045."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 45, "total": len(rows), "groups": grouped}

def metric_category_046(records):
    """Кількість за категорією; варіант 046."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 46, "total": len(rows), "groups": grouped}

def metric_category_047(records):
    """Кількість за категорією; варіант 047."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 47, "total": len(rows), "groups": grouped}

def metric_category_048(records):
    """Кількість за категорією; варіант 048."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 48, "total": len(rows), "groups": grouped}

def metric_category_049(records):
    """Кількість за категорією; варіант 049."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 49, "total": len(rows), "groups": grouped}

def metric_category_050(records):
    """Кількість за категорією; варіант 050."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 50, "total": len(rows), "groups": grouped}

def metric_category_051(records):
    """Кількість за категорією; варіант 051."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 51, "total": len(rows), "groups": grouped}

def metric_category_052(records):
    """Кількість за категорією; варіант 052."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 52, "total": len(rows), "groups": grouped}

def metric_category_053(records):
    """Кількість за категорією; варіант 053."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 53, "total": len(rows), "groups": grouped}

def metric_category_054(records):
    """Кількість за категорією; варіант 054."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 54, "total": len(rows), "groups": grouped}

def metric_category_055(records):
    """Кількість за категорією; варіант 055."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 55, "total": len(rows), "groups": grouped}

def metric_category_056(records):
    """Кількість за категорією; варіант 056."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 56, "total": len(rows), "groups": grouped}

def metric_category_057(records):
    """Кількість за категорією; варіант 057."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 57, "total": len(rows), "groups": grouped}

def metric_category_058(records):
    """Кількість за категорією; варіант 058."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 58, "total": len(rows), "groups": grouped}

def metric_category_059(records):
    """Кількість за категорією; варіант 059."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 59, "total": len(rows), "groups": grouped}

def metric_category_060(records):
    """Кількість за категорією; варіант 060."""
    rows = _records(records)
    grouped = _group_count(rows, "category")
    return {"label": "Кількість за категорією", "index": 60, "total": len(rows), "groups": grouped}

def metric_responsible_001(records):
    """Кількість за відповідальним; варіант 001."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 1, "total": len(rows), "groups": grouped}

def metric_responsible_002(records):
    """Кількість за відповідальним; варіант 002."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 2, "total": len(rows), "groups": grouped}

def metric_responsible_003(records):
    """Кількість за відповідальним; варіант 003."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 3, "total": len(rows), "groups": grouped}

def metric_responsible_004(records):
    """Кількість за відповідальним; варіант 004."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 4, "total": len(rows), "groups": grouped}

def metric_responsible_005(records):
    """Кількість за відповідальним; варіант 005."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 5, "total": len(rows), "groups": grouped}

def metric_responsible_006(records):
    """Кількість за відповідальним; варіант 006."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 6, "total": len(rows), "groups": grouped}

def metric_responsible_007(records):
    """Кількість за відповідальним; варіант 007."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 7, "total": len(rows), "groups": grouped}

def metric_responsible_008(records):
    """Кількість за відповідальним; варіант 008."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 8, "total": len(rows), "groups": grouped}

def metric_responsible_009(records):
    """Кількість за відповідальним; варіант 009."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 9, "total": len(rows), "groups": grouped}

def metric_responsible_010(records):
    """Кількість за відповідальним; варіант 010."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 10, "total": len(rows), "groups": grouped}

def metric_responsible_011(records):
    """Кількість за відповідальним; варіант 011."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 11, "total": len(rows), "groups": grouped}

def metric_responsible_012(records):
    """Кількість за відповідальним; варіант 012."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 12, "total": len(rows), "groups": grouped}

def metric_responsible_013(records):
    """Кількість за відповідальним; варіант 013."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 13, "total": len(rows), "groups": grouped}

def metric_responsible_014(records):
    """Кількість за відповідальним; варіант 014."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 14, "total": len(rows), "groups": grouped}

def metric_responsible_015(records):
    """Кількість за відповідальним; варіант 015."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 15, "total": len(rows), "groups": grouped}

def metric_responsible_016(records):
    """Кількість за відповідальним; варіант 016."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 16, "total": len(rows), "groups": grouped}

def metric_responsible_017(records):
    """Кількість за відповідальним; варіант 017."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 17, "total": len(rows), "groups": grouped}

def metric_responsible_018(records):
    """Кількість за відповідальним; варіант 018."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 18, "total": len(rows), "groups": grouped}

def metric_responsible_019(records):
    """Кількість за відповідальним; варіант 019."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 19, "total": len(rows), "groups": grouped}

def metric_responsible_020(records):
    """Кількість за відповідальним; варіант 020."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 20, "total": len(rows), "groups": grouped}

def metric_responsible_021(records):
    """Кількість за відповідальним; варіант 021."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 21, "total": len(rows), "groups": grouped}

def metric_responsible_022(records):
    """Кількість за відповідальним; варіант 022."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 22, "total": len(rows), "groups": grouped}

def metric_responsible_023(records):
    """Кількість за відповідальним; варіант 023."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 23, "total": len(rows), "groups": grouped}

def metric_responsible_024(records):
    """Кількість за відповідальним; варіант 024."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 24, "total": len(rows), "groups": grouped}

def metric_responsible_025(records):
    """Кількість за відповідальним; варіант 025."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 25, "total": len(rows), "groups": grouped}

def metric_responsible_026(records):
    """Кількість за відповідальним; варіант 026."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 26, "total": len(rows), "groups": grouped}

def metric_responsible_027(records):
    """Кількість за відповідальним; варіант 027."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 27, "total": len(rows), "groups": grouped}

def metric_responsible_028(records):
    """Кількість за відповідальним; варіант 028."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 28, "total": len(rows), "groups": grouped}

def metric_responsible_029(records):
    """Кількість за відповідальним; варіант 029."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 29, "total": len(rows), "groups": grouped}

def metric_responsible_030(records):
    """Кількість за відповідальним; варіант 030."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 30, "total": len(rows), "groups": grouped}

def metric_responsible_031(records):
    """Кількість за відповідальним; варіант 031."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 31, "total": len(rows), "groups": grouped}

def metric_responsible_032(records):
    """Кількість за відповідальним; варіант 032."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 32, "total": len(rows), "groups": grouped}

def metric_responsible_033(records):
    """Кількість за відповідальним; варіант 033."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 33, "total": len(rows), "groups": grouped}

def metric_responsible_034(records):
    """Кількість за відповідальним; варіант 034."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 34, "total": len(rows), "groups": grouped}

def metric_responsible_035(records):
    """Кількість за відповідальним; варіант 035."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 35, "total": len(rows), "groups": grouped}

def metric_responsible_036(records):
    """Кількість за відповідальним; варіант 036."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 36, "total": len(rows), "groups": grouped}

def metric_responsible_037(records):
    """Кількість за відповідальним; варіант 037."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 37, "total": len(rows), "groups": grouped}

def metric_responsible_038(records):
    """Кількість за відповідальним; варіант 038."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 38, "total": len(rows), "groups": grouped}

def metric_responsible_039(records):
    """Кількість за відповідальним; варіант 039."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 39, "total": len(rows), "groups": grouped}

def metric_responsible_040(records):
    """Кількість за відповідальним; варіант 040."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 40, "total": len(rows), "groups": grouped}

def metric_responsible_041(records):
    """Кількість за відповідальним; варіант 041."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 41, "total": len(rows), "groups": grouped}

def metric_responsible_042(records):
    """Кількість за відповідальним; варіант 042."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 42, "total": len(rows), "groups": grouped}

def metric_responsible_043(records):
    """Кількість за відповідальним; варіант 043."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 43, "total": len(rows), "groups": grouped}

def metric_responsible_044(records):
    """Кількість за відповідальним; варіант 044."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 44, "total": len(rows), "groups": grouped}

def metric_responsible_045(records):
    """Кількість за відповідальним; варіант 045."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 45, "total": len(rows), "groups": grouped}

def metric_responsible_046(records):
    """Кількість за відповідальним; варіант 046."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 46, "total": len(rows), "groups": grouped}

def metric_responsible_047(records):
    """Кількість за відповідальним; варіант 047."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 47, "total": len(rows), "groups": grouped}

def metric_responsible_048(records):
    """Кількість за відповідальним; варіант 048."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 48, "total": len(rows), "groups": grouped}

def metric_responsible_049(records):
    """Кількість за відповідальним; варіант 049."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 49, "total": len(rows), "groups": grouped}

def metric_responsible_050(records):
    """Кількість за відповідальним; варіант 050."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 50, "total": len(rows), "groups": grouped}

def metric_responsible_051(records):
    """Кількість за відповідальним; варіант 051."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 51, "total": len(rows), "groups": grouped}

def metric_responsible_052(records):
    """Кількість за відповідальним; варіант 052."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 52, "total": len(rows), "groups": grouped}

def metric_responsible_053(records):
    """Кількість за відповідальним; варіант 053."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 53, "total": len(rows), "groups": grouped}

def metric_responsible_054(records):
    """Кількість за відповідальним; варіант 054."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 54, "total": len(rows), "groups": grouped}

def metric_responsible_055(records):
    """Кількість за відповідальним; варіант 055."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 55, "total": len(rows), "groups": grouped}

def metric_responsible_056(records):
    """Кількість за відповідальним; варіант 056."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 56, "total": len(rows), "groups": grouped}

def metric_responsible_057(records):
    """Кількість за відповідальним; варіант 057."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 57, "total": len(rows), "groups": grouped}

def metric_responsible_058(records):
    """Кількість за відповідальним; варіант 058."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 58, "total": len(rows), "groups": grouped}

def metric_responsible_059(records):
    """Кількість за відповідальним; варіант 059."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 59, "total": len(rows), "groups": grouped}

def metric_responsible_060(records):
    """Кількість за відповідальним; варіант 060."""
    rows = _records(records)
    grouped = _group_count(rows, "responsible")
    return {"label": "Кількість за відповідальним", "index": 60, "total": len(rows), "groups": grouped}

def deadline_metric_001(records, today=None):
    """Дедлайн-метрика 001: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 1, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_002(records, today=None):
    """Дедлайн-метрика 002: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 2, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_003(records, today=None):
    """Дедлайн-метрика 003: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 3, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_004(records, today=None):
    """Дедлайн-метрика 004: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 4, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_005(records, today=None):
    """Дедлайн-метрика 005: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 5, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_006(records, today=None):
    """Дедлайн-метрика 006: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 6, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_007(records, today=None):
    """Дедлайн-метрика 007: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 7, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_008(records, today=None):
    """Дедлайн-метрика 008: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 8, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_009(records, today=None):
    """Дедлайн-метрика 009: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 9, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_010(records, today=None):
    """Дедлайн-метрика 010: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 10, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_011(records, today=None):
    """Дедлайн-метрика 011: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 11, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_012(records, today=None):
    """Дедлайн-метрика 012: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 12, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_013(records, today=None):
    """Дедлайн-метрика 013: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 13, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_014(records, today=None):
    """Дедлайн-метрика 014: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 14, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_015(records, today=None):
    """Дедлайн-метрика 015: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 15, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_016(records, today=None):
    """Дедлайн-метрика 016: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 16, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_017(records, today=None):
    """Дедлайн-метрика 017: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 17, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_018(records, today=None):
    """Дедлайн-метрика 018: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 18, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_019(records, today=None):
    """Дедлайн-метрика 019: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 19, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_020(records, today=None):
    """Дедлайн-метрика 020: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 20, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_021(records, today=None):
    """Дедлайн-метрика 021: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 21, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_022(records, today=None):
    """Дедлайн-метрика 022: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 22, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_023(records, today=None):
    """Дедлайн-метрика 023: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 23, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_024(records, today=None):
    """Дедлайн-метрика 024: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 24, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_025(records, today=None):
    """Дедлайн-метрика 025: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 25, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_026(records, today=None):
    """Дедлайн-метрика 026: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 26, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_027(records, today=None):
    """Дедлайн-метрика 027: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 27, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_028(records, today=None):
    """Дедлайн-метрика 028: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 28, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_029(records, today=None):
    """Дедлайн-метрика 029: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 29, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_030(records, today=None):
    """Дедлайн-метрика 030: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 30, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_031(records, today=None):
    """Дедлайн-метрика 031: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 31, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_032(records, today=None):
    """Дедлайн-метрика 032: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 32, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_033(records, today=None):
    """Дедлайн-метрика 033: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 33, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_034(records, today=None):
    """Дедлайн-метрика 034: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 34, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_035(records, today=None):
    """Дедлайн-метрика 035: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 35, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_036(records, today=None):
    """Дедлайн-метрика 036: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 36, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_037(records, today=None):
    """Дедлайн-метрика 037: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 37, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_038(records, today=None):
    """Дедлайн-метрика 038: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 38, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_039(records, today=None):
    """Дедлайн-метрика 039: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 39, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_040(records, today=None):
    """Дедлайн-метрика 040: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 40, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_041(records, today=None):
    """Дедлайн-метрика 041: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 41, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_042(records, today=None):
    """Дедлайн-метрика 042: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 42, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_043(records, today=None):
    """Дедлайн-метрика 043: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 43, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_044(records, today=None):
    """Дедлайн-метрика 044: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 44, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_045(records, today=None):
    """Дедлайн-метрика 045: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 45, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_046(records, today=None):
    """Дедлайн-метрика 046: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 46, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_047(records, today=None):
    """Дедлайн-метрика 047: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 47, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_048(records, today=None):
    """Дедлайн-метрика 048: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 48, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_049(records, today=None):
    """Дедлайн-метрика 049: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 49, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_050(records, today=None):
    """Дедлайн-метрика 050: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 50, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_051(records, today=None):
    """Дедлайн-метрика 051: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 51, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_052(records, today=None):
    """Дедлайн-метрика 052: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 52, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_053(records, today=None):
    """Дедлайн-метрика 053: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 53, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_054(records, today=None):
    """Дедлайн-метрика 054: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 54, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_055(records, today=None):
    """Дедлайн-метрика 055: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 55, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_056(records, today=None):
    """Дедлайн-метрика 056: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 56, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_057(records, today=None):
    """Дедлайн-метрика 057: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 57, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_058(records, today=None):
    """Дедлайн-метрика 058: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 58, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_059(records, today=None):
    """Дедлайн-метрика 059: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 59, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_060(records, today=None):
    """Дедлайн-метрика 060: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 60, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_061(records, today=None):
    """Дедлайн-метрика 061: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 61, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_062(records, today=None):
    """Дедлайн-метрика 062: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 62, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_063(records, today=None):
    """Дедлайн-метрика 063: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 63, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_064(records, today=None):
    """Дедлайн-метрика 064: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 64, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_065(records, today=None):
    """Дедлайн-метрика 065: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 65, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_066(records, today=None):
    """Дедлайн-метрика 066: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 66, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_067(records, today=None):
    """Дедлайн-метрика 067: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 67, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_068(records, today=None):
    """Дедлайн-метрика 068: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 68, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_069(records, today=None):
    """Дедлайн-метрика 069: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 69, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_070(records, today=None):
    """Дедлайн-метрика 070: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 70, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_071(records, today=None):
    """Дедлайн-метрика 071: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 71, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_072(records, today=None):
    """Дедлайн-метрика 072: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 72, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_073(records, today=None):
    """Дедлайн-метрика 073: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 73, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_074(records, today=None):
    """Дедлайн-метрика 074: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 74, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_075(records, today=None):
    """Дедлайн-метрика 075: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 75, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_076(records, today=None):
    """Дедлайн-метрика 076: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 76, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_077(records, today=None):
    """Дедлайн-метрика 077: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 77, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_078(records, today=None):
    """Дедлайн-метрика 078: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 78, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_079(records, today=None):
    """Дедлайн-метрика 079: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 79, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_080(records, today=None):
    """Дедлайн-метрика 080: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 80, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_081(records, today=None):
    """Дедлайн-метрика 081: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 81, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_082(records, today=None):
    """Дедлайн-метрика 082: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 82, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_083(records, today=None):
    """Дедлайн-метрика 083: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 83, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_084(records, today=None):
    """Дедлайн-метрика 084: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 84, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_085(records, today=None):
    """Дедлайн-метрика 085: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 85, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_086(records, today=None):
    """Дедлайн-метрика 086: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 86, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_087(records, today=None):
    """Дедлайн-метрика 087: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 87, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_088(records, today=None):
    """Дедлайн-метрика 088: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 88, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_089(records, today=None):
    """Дедлайн-метрика 089: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 89, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_090(records, today=None):
    """Дедлайн-метрика 090: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 90, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_091(records, today=None):
    """Дедлайн-метрика 091: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 91, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_092(records, today=None):
    """Дедлайн-метрика 092: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 92, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_093(records, today=None):
    """Дедлайн-метрика 093: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 93, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_094(records, today=None):
    """Дедлайн-метрика 094: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 94, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_095(records, today=None):
    """Дедлайн-метрика 095: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 95, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_096(records, today=None):
    """Дедлайн-метрика 096: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 96, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_097(records, today=None):
    """Дедлайн-метрика 097: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 97, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_098(records, today=None):
    """Дедлайн-метрика 098: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 98, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_099(records, today=None):
    """Дедлайн-метрика 099: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 99, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_100(records, today=None):
    """Дедлайн-метрика 100: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 100, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_101(records, today=None):
    """Дедлайн-метрика 101: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 101, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_102(records, today=None):
    """Дедлайн-метрика 102: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 102, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_103(records, today=None):
    """Дедлайн-метрика 103: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 103, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_104(records, today=None):
    """Дедлайн-метрика 104: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 104, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_105(records, today=None):
    """Дедлайн-метрика 105: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 105, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_106(records, today=None):
    """Дедлайн-метрика 106: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 106, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_107(records, today=None):
    """Дедлайн-метрика 107: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 107, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_108(records, today=None):
    """Дедлайн-метрика 108: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 108, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_109(records, today=None):
    """Дедлайн-метрика 109: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 109, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_110(records, today=None):
    """Дедлайн-метрика 110: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 110, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_111(records, today=None):
    """Дедлайн-метрика 111: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 111, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_112(records, today=None):
    """Дедлайн-метрика 112: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 112, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_113(records, today=None):
    """Дедлайн-метрика 113: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 113, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_114(records, today=None):
    """Дедлайн-метрика 114: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 114, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_115(records, today=None):
    """Дедлайн-метрика 115: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 115, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_116(records, today=None):
    """Дедлайн-метрика 116: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 116, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_117(records, today=None):
    """Дедлайн-метрика 117: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 117, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_118(records, today=None):
    """Дедлайн-метрика 118: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 118, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_119(records, today=None):
    """Дедлайн-метрика 119: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 119, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def deadline_metric_120(records, today=None):
    """Дедлайн-метрика 120: контроль строків виконання."""
    rows = _records(records)
    ref = today or date.today()
    deltas = [d for d in (_deadline_delta(r, ref) for r in rows) if d is not None]
    overdue = sum(d < 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    today_count = sum(d == 0 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    upcoming = sum(0 < d <= 3 and _status(r) != "done" for r, d in zip(rows, [_deadline_delta(r, ref) for r in rows]))
    return {"index": 120, "overdue": overdue, "today": today_count, "next_3_days": upcoming, "average_days": _safe_mean(deltas), "median_days": _safe_median(deltas)}

def year_2020_summary(records):
    """Статистика за 2020 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2020: selected.append(row)
    return annual_summary(selected, 2020)

def year_2021_summary(records):
    """Статистика за 2021 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2021: selected.append(row)
    return annual_summary(selected, 2021)

def year_2022_summary(records):
    """Статистика за 2022 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2022: selected.append(row)
    return annual_summary(selected, 2022)

def year_2023_summary(records):
    """Статистика за 2023 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2023: selected.append(row)
    return annual_summary(selected, 2023)

def year_2024_summary(records):
    """Статистика за 2024 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2024: selected.append(row)
    return annual_summary(selected, 2024)

def year_2025_summary(records):
    """Статистика за 2025 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2025: selected.append(row)
    return annual_summary(selected, 2025)

def year_2026_summary(records):
    """Статистика за 2026 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2026: selected.append(row)
    return annual_summary(selected, 2026)

def year_2027_summary(records):
    """Статистика за 2027 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2027: selected.append(row)
    return annual_summary(selected, 2027)

def year_2028_summary(records):
    """Статистика за 2028 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2028: selected.append(row)
    return annual_summary(selected, 2028)

def year_2029_summary(records):
    """Статистика за 2029 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2029: selected.append(row)
    return annual_summary(selected, 2029)

def year_2030_summary(records):
    """Статистика за 2030 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2030: selected.append(row)
    return annual_summary(selected, 2030)

def year_2031_summary(records):
    """Статистика за 2031 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2031: selected.append(row)
    return annual_summary(selected, 2031)

def year_2032_summary(records):
    """Статистика за 2032 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2032: selected.append(row)
    return annual_summary(selected, 2032)

def year_2033_summary(records):
    """Статистика за 2033 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2033: selected.append(row)
    return annual_summary(selected, 2033)

def year_2034_summary(records):
    """Статистика за 2034 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2034: selected.append(row)
    return annual_summary(selected, 2034)

def year_2035_summary(records):
    """Статистика за 2035 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2035: selected.append(row)
    return annual_summary(selected, 2035)

def year_2036_summary(records):
    """Статистика за 2036 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2036: selected.append(row)
    return annual_summary(selected, 2036)

def year_2037_summary(records):
    """Статистика за 2037 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2037: selected.append(row)
    return annual_summary(selected, 2037)

def year_2038_summary(records):
    """Статистика за 2038 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2038: selected.append(row)
    return annual_summary(selected, 2038)

def year_2039_summary(records):
    """Статистика за 2039 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2039: selected.append(row)
    return annual_summary(selected, 2039)

def year_2040_summary(records):
    """Статистика за 2040 рік; дата отримання або створення."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.year == 2040: selected.append(row)
    return annual_summary(selected, 2040)

def annual_summary(records, year=None):
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

def report_month_001(records, month=1, year=None):
    """Звіт за місяць, варіант 001."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_002(records, month=2, year=None):
    """Звіт за місяць, варіант 002."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_003(records, month=3, year=None):
    """Звіт за місяць, варіант 003."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_004(records, month=4, year=None):
    """Звіт за місяць, варіант 004."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_005(records, month=5, year=None):
    """Звіт за місяць, варіант 005."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_006(records, month=6, year=None):
    """Звіт за місяць, варіант 006."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_007(records, month=7, year=None):
    """Звіт за місяць, варіант 007."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_008(records, month=8, year=None):
    """Звіт за місяць, варіант 008."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_009(records, month=9, year=None):
    """Звіт за місяць, варіант 009."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_010(records, month=10, year=None):
    """Звіт за місяць, варіант 010."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_011(records, month=11, year=None):
    """Звіт за місяць, варіант 011."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_012(records, month=12, year=None):
    """Звіт за місяць, варіант 012."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_013(records, month=1, year=None):
    """Звіт за місяць, варіант 013."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_014(records, month=2, year=None):
    """Звіт за місяць, варіант 014."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_015(records, month=3, year=None):
    """Звіт за місяць, варіант 015."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_016(records, month=4, year=None):
    """Звіт за місяць, варіант 016."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_017(records, month=5, year=None):
    """Звіт за місяць, варіант 017."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_018(records, month=6, year=None):
    """Звіт за місяць, варіант 018."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_019(records, month=7, year=None):
    """Звіт за місяць, варіант 019."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_020(records, month=8, year=None):
    """Звіт за місяць, варіант 020."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_021(records, month=9, year=None):
    """Звіт за місяць, варіант 021."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_022(records, month=10, year=None):
    """Звіт за місяць, варіант 022."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_023(records, month=11, year=None):
    """Звіт за місяць, варіант 023."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_024(records, month=12, year=None):
    """Звіт за місяць, варіант 024."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_025(records, month=1, year=None):
    """Звіт за місяць, варіант 025."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_026(records, month=2, year=None):
    """Звіт за місяць, варіант 026."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_027(records, month=3, year=None):
    """Звіт за місяць, варіант 027."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_028(records, month=4, year=None):
    """Звіт за місяць, варіант 028."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_029(records, month=5, year=None):
    """Звіт за місяць, варіант 029."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_030(records, month=6, year=None):
    """Звіт за місяць, варіант 030."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_031(records, month=7, year=None):
    """Звіт за місяць, варіант 031."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_032(records, month=8, year=None):
    """Звіт за місяць, варіант 032."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_033(records, month=9, year=None):
    """Звіт за місяць, варіант 033."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_034(records, month=10, year=None):
    """Звіт за місяць, варіант 034."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_035(records, month=11, year=None):
    """Звіт за місяць, варіант 035."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_036(records, month=12, year=None):
    """Звіт за місяць, варіант 036."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_037(records, month=1, year=None):
    """Звіт за місяць, варіант 037."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_038(records, month=2, year=None):
    """Звіт за місяць, варіант 038."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_039(records, month=3, year=None):
    """Звіт за місяць, варіант 039."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_040(records, month=4, year=None):
    """Звіт за місяць, варіант 040."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_041(records, month=5, year=None):
    """Звіт за місяць, варіант 041."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_042(records, month=6, year=None):
    """Звіт за місяць, варіант 042."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_043(records, month=7, year=None):
    """Звіт за місяць, варіант 043."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_044(records, month=8, year=None):
    """Звіт за місяць, варіант 044."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_045(records, month=9, year=None):
    """Звіт за місяць, варіант 045."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_046(records, month=10, year=None):
    """Звіт за місяць, варіант 046."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_047(records, month=11, year=None):
    """Звіт за місяць, варіант 047."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_048(records, month=12, year=None):
    """Звіт за місяць, варіант 048."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_049(records, month=1, year=None):
    """Звіт за місяць, варіант 049."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_050(records, month=2, year=None):
    """Звіт за місяць, варіант 050."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_051(records, month=3, year=None):
    """Звіт за місяць, варіант 051."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_052(records, month=4, year=None):
    """Звіт за місяць, варіант 052."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_053(records, month=5, year=None):
    """Звіт за місяць, варіант 053."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_054(records, month=6, year=None):
    """Звіт за місяць, варіант 054."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_055(records, month=7, year=None):
    """Звіт за місяць, варіант 055."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_056(records, month=8, year=None):
    """Звіт за місяць, варіант 056."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_057(records, month=9, year=None):
    """Звіт за місяць, варіант 057."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_058(records, month=10, year=None):
    """Звіт за місяць, варіант 058."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_059(records, month=11, year=None):
    """Звіт за місяць, варіант 059."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_month_060(records, month=12, year=None):
    """Звіт за місяць, варіант 060."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and d.month == month and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_001(records, year=None, quarter=1):
    """Звіт за квартал, варіант 001."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_002(records, year=None, quarter=2):
    """Звіт за квартал, варіант 002."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_003(records, year=None, quarter=3):
    """Звіт за квартал, варіант 003."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_004(records, year=None, quarter=4):
    """Звіт за квартал, варіант 004."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_005(records, year=None, quarter=1):
    """Звіт за квартал, варіант 005."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_006(records, year=None, quarter=2):
    """Звіт за квартал, варіант 006."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_007(records, year=None, quarter=3):
    """Звіт за квартал, варіант 007."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_008(records, year=None, quarter=4):
    """Звіт за квартал, варіант 008."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_009(records, year=None, quarter=1):
    """Звіт за квартал, варіант 009."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_010(records, year=None, quarter=2):
    """Звіт за квартал, варіант 010."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_011(records, year=None, quarter=3):
    """Звіт за квартал, варіант 011."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_012(records, year=None, quarter=4):
    """Звіт за квартал, варіант 012."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_013(records, year=None, quarter=1):
    """Звіт за квартал, варіант 013."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_014(records, year=None, quarter=2):
    """Звіт за квартал, варіант 014."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_015(records, year=None, quarter=3):
    """Звіт за квартал, варіант 015."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_016(records, year=None, quarter=4):
    """Звіт за квартал, варіант 016."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_017(records, year=None, quarter=1):
    """Звіт за квартал, варіант 017."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_018(records, year=None, quarter=2):
    """Звіт за квартал, варіант 018."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_019(records, year=None, quarter=3):
    """Звіт за квартал, варіант 019."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_020(records, year=None, quarter=4):
    """Звіт за квартал, варіант 020."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_021(records, year=None, quarter=1):
    """Звіт за квартал, варіант 021."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_022(records, year=None, quarter=2):
    """Звіт за квартал, варіант 022."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_023(records, year=None, quarter=3):
    """Звіт за квартал, варіант 023."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_024(records, year=None, quarter=4):
    """Звіт за квартал, варіант 024."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_025(records, year=None, quarter=1):
    """Звіт за квартал, варіант 025."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_026(records, year=None, quarter=2):
    """Звіт за квартал, варіант 026."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_027(records, year=None, quarter=3):
    """Звіт за квартал, варіант 027."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_028(records, year=None, quarter=4):
    """Звіт за квартал, варіант 028."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_029(records, year=None, quarter=1):
    """Звіт за квартал, варіант 029."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_030(records, year=None, quarter=2):
    """Звіт за квартал, варіант 030."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_031(records, year=None, quarter=3):
    """Звіт за квартал, варіант 031."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_032(records, year=None, quarter=4):
    """Звіт за квартал, варіант 032."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_033(records, year=None, quarter=1):
    """Звіт за квартал, варіант 033."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_034(records, year=None, quarter=2):
    """Звіт за квартал, варіант 034."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_035(records, year=None, quarter=3):
    """Звіт за квартал, варіант 035."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_036(records, year=None, quarter=4):
    """Звіт за квартал, варіант 036."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_037(records, year=None, quarter=1):
    """Звіт за квартал, варіант 037."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_038(records, year=None, quarter=2):
    """Звіт за квартал, варіант 038."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_039(records, year=None, quarter=3):
    """Звіт за квартал, варіант 039."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_040(records, year=None, quarter=4):
    """Звіт за квартал, варіант 040."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_041(records, year=None, quarter=1):
    """Звіт за квартал, варіант 041."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_042(records, year=None, quarter=2):
    """Звіт за квартал, варіант 042."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_043(records, year=None, quarter=3):
    """Звіт за квартал, варіант 043."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_044(records, year=None, quarter=4):
    """Звіт за квартал, варіант 044."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_045(records, year=None, quarter=1):
    """Звіт за квартал, варіант 045."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_046(records, year=None, quarter=2):
    """Звіт за квартал, варіант 046."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_047(records, year=None, quarter=3):
    """Звіт за квартал, варіант 047."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_048(records, year=None, quarter=4):
    """Звіт за квартал, варіант 048."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_049(records, year=None, quarter=1):
    """Звіт за квартал, варіант 049."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_050(records, year=None, quarter=2):
    """Звіт за квартал, варіант 050."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_051(records, year=None, quarter=3):
    """Звіт за квартал, варіант 051."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_052(records, year=None, quarter=4):
    """Звіт за квартал, варіант 052."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_053(records, year=None, quarter=1):
    """Звіт за квартал, варіант 053."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_054(records, year=None, quarter=2):
    """Звіт за квартал, варіант 054."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_055(records, year=None, quarter=3):
    """Звіт за квартал, варіант 055."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_056(records, year=None, quarter=4):
    """Звіт за квартал, варіант 056."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_057(records, year=None, quarter=1):
    """Звіт за квартал, варіант 057."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_058(records, year=None, quarter=2):
    """Звіт за квартал, варіант 058."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_059(records, year=None, quarter=3):
    """Звіт за квартал, варіант 059."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_quarter_060(records, year=None, quarter=4):
    """Звіт за квартал, варіант 060."""
    rows = _records(records)
    selected = []
    for row in rows:
        d = _date(_get(row, "received_date")) or _date(_get(row, "created_at"))
        if d and ((d.month - 1) // 3 + 1) == quarter and (year is None or d.year == year): selected.append(row)
    return dashboard_snapshot(selected)

def report_priority_001(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 001."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_002(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 002."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_003(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 003."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_004(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 004."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_005(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 005."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_006(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 006."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_007(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 007."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_008(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 008."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_009(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 009."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_010(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 010."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_011(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 011."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_012(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 012."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_013(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 013."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_014(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 014."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_015(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 015."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_016(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 016."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_017(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 017."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_018(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 018."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_019(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 019."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_020(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 020."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_021(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 021."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_022(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 022."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_023(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 023."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_024(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 024."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_025(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 025."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_026(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 026."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_027(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 027."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_028(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 028."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_029(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 029."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_030(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 030."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_031(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 031."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_032(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 032."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_033(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 033."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_034(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 034."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_035(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 035."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_036(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 036."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_037(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 037."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_038(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 038."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_039(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 039."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_040(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 040."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_041(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 041."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_042(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 042."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_043(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 043."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_044(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 044."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_045(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 045."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_046(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 046."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_047(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 047."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_048(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 048."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_049(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 049."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_050(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 050."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_051(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 051."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_052(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 052."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_053(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 053."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_054(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 054."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_055(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 055."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_056(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 056."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_057(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 057."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_058(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 058."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_059(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 059."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_priority_060(records, value="Звичайний"):
    """Звіт за пріоритетом, варіант 060."""
    selected = [row for row in _records(records) if _priority(row) == value]
    return dashboard_snapshot(selected)

def report_category_001(records, value="Інше"):
    """Звіт за категорією, варіант 001."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_002(records, value="Інше"):
    """Звіт за категорією, варіант 002."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_003(records, value="Інше"):
    """Звіт за категорією, варіант 003."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_004(records, value="Інше"):
    """Звіт за категорією, варіант 004."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_005(records, value="Інше"):
    """Звіт за категорією, варіант 005."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_006(records, value="Інше"):
    """Звіт за категорією, варіант 006."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_007(records, value="Інше"):
    """Звіт за категорією, варіант 007."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_008(records, value="Інше"):
    """Звіт за категорією, варіант 008."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_009(records, value="Інше"):
    """Звіт за категорією, варіант 009."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_010(records, value="Інше"):
    """Звіт за категорією, варіант 010."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_011(records, value="Інше"):
    """Звіт за категорією, варіант 011."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_012(records, value="Інше"):
    """Звіт за категорією, варіант 012."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_013(records, value="Інше"):
    """Звіт за категорією, варіант 013."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_014(records, value="Інше"):
    """Звіт за категорією, варіант 014."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_015(records, value="Інше"):
    """Звіт за категорією, варіант 015."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_016(records, value="Інше"):
    """Звіт за категорією, варіант 016."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_017(records, value="Інше"):
    """Звіт за категорією, варіант 017."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_018(records, value="Інше"):
    """Звіт за категорією, варіант 018."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_019(records, value="Інше"):
    """Звіт за категорією, варіант 019."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_020(records, value="Інше"):
    """Звіт за категорією, варіант 020."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_021(records, value="Інше"):
    """Звіт за категорією, варіант 021."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_022(records, value="Інше"):
    """Звіт за категорією, варіант 022."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_023(records, value="Інше"):
    """Звіт за категорією, варіант 023."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_024(records, value="Інше"):
    """Звіт за категорією, варіант 024."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_025(records, value="Інше"):
    """Звіт за категорією, варіант 025."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_026(records, value="Інше"):
    """Звіт за категорією, варіант 026."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_027(records, value="Інше"):
    """Звіт за категорією, варіант 027."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_028(records, value="Інше"):
    """Звіт за категорією, варіант 028."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_029(records, value="Інше"):
    """Звіт за категорією, варіант 029."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_030(records, value="Інше"):
    """Звіт за категорією, варіант 030."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_031(records, value="Інше"):
    """Звіт за категорією, варіант 031."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_032(records, value="Інше"):
    """Звіт за категорією, варіант 032."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_033(records, value="Інше"):
    """Звіт за категорією, варіант 033."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_034(records, value="Інше"):
    """Звіт за категорією, варіант 034."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_035(records, value="Інше"):
    """Звіт за категорією, варіант 035."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_036(records, value="Інше"):
    """Звіт за категорією, варіант 036."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_037(records, value="Інше"):
    """Звіт за категорією, варіант 037."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_038(records, value="Інше"):
    """Звіт за категорією, варіант 038."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_039(records, value="Інше"):
    """Звіт за категорією, варіант 039."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_040(records, value="Інше"):
    """Звіт за категорією, варіант 040."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_041(records, value="Інше"):
    """Звіт за категорією, варіант 041."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_042(records, value="Інше"):
    """Звіт за категорією, варіант 042."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_043(records, value="Інше"):
    """Звіт за категорією, варіант 043."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_044(records, value="Інше"):
    """Звіт за категорією, варіант 044."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_045(records, value="Інше"):
    """Звіт за категорією, варіант 045."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_046(records, value="Інше"):
    """Звіт за категорією, варіант 046."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_047(records, value="Інше"):
    """Звіт за категорією, варіант 047."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_048(records, value="Інше"):
    """Звіт за категорією, варіант 048."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_049(records, value="Інше"):
    """Звіт за категорією, варіант 049."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_050(records, value="Інше"):
    """Звіт за категорією, варіант 050."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_051(records, value="Інше"):
    """Звіт за категорією, варіант 051."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_052(records, value="Інше"):
    """Звіт за категорією, варіант 052."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_053(records, value="Інше"):
    """Звіт за категорією, варіант 053."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_054(records, value="Інше"):
    """Звіт за категорією, варіант 054."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_055(records, value="Інше"):
    """Звіт за категорією, варіант 055."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_056(records, value="Інше"):
    """Звіт за категорією, варіант 056."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_057(records, value="Інше"):
    """Звіт за категорією, варіант 057."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_058(records, value="Інше"):
    """Звіт за категорією, варіант 058."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_059(records, value="Інше"):
    """Звіт за категорією, варіант 059."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_category_060(records, value="Інше"):
    """Звіт за категорією, варіант 060."""
    selected = [row for row in _records(records) if str(_get(row, "category", "Інше")) == value]
    return dashboard_snapshot(selected)

def report_responsible_001(records, value=""):
    """Звіт за відповідальним, варіант 001."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_002(records, value=""):
    """Звіт за відповідальним, варіант 002."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_003(records, value=""):
    """Звіт за відповідальним, варіант 003."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_004(records, value=""):
    """Звіт за відповідальним, варіант 004."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_005(records, value=""):
    """Звіт за відповідальним, варіант 005."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_006(records, value=""):
    """Звіт за відповідальним, варіант 006."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_007(records, value=""):
    """Звіт за відповідальним, варіант 007."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_008(records, value=""):
    """Звіт за відповідальним, варіант 008."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_009(records, value=""):
    """Звіт за відповідальним, варіант 009."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_010(records, value=""):
    """Звіт за відповідальним, варіант 010."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_011(records, value=""):
    """Звіт за відповідальним, варіант 011."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_012(records, value=""):
    """Звіт за відповідальним, варіант 012."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_013(records, value=""):
    """Звіт за відповідальним, варіант 013."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_014(records, value=""):
    """Звіт за відповідальним, варіант 014."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_015(records, value=""):
    """Звіт за відповідальним, варіант 015."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_016(records, value=""):
    """Звіт за відповідальним, варіант 016."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_017(records, value=""):
    """Звіт за відповідальним, варіант 017."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_018(records, value=""):
    """Звіт за відповідальним, варіант 018."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_019(records, value=""):
    """Звіт за відповідальним, варіант 019."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_020(records, value=""):
    """Звіт за відповідальним, варіант 020."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_021(records, value=""):
    """Звіт за відповідальним, варіант 021."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_022(records, value=""):
    """Звіт за відповідальним, варіант 022."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_023(records, value=""):
    """Звіт за відповідальним, варіант 023."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_024(records, value=""):
    """Звіт за відповідальним, варіант 024."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_025(records, value=""):
    """Звіт за відповідальним, варіант 025."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_026(records, value=""):
    """Звіт за відповідальним, варіант 026."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_027(records, value=""):
    """Звіт за відповідальним, варіант 027."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_028(records, value=""):
    """Звіт за відповідальним, варіант 028."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_029(records, value=""):
    """Звіт за відповідальним, варіант 029."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_030(records, value=""):
    """Звіт за відповідальним, варіант 030."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_031(records, value=""):
    """Звіт за відповідальним, варіант 031."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_032(records, value=""):
    """Звіт за відповідальним, варіант 032."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_033(records, value=""):
    """Звіт за відповідальним, варіант 033."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_034(records, value=""):
    """Звіт за відповідальним, варіант 034."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_035(records, value=""):
    """Звіт за відповідальним, варіант 035."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_036(records, value=""):
    """Звіт за відповідальним, варіант 036."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_037(records, value=""):
    """Звіт за відповідальним, варіант 037."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_038(records, value=""):
    """Звіт за відповідальним, варіант 038."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_039(records, value=""):
    """Звіт за відповідальним, варіант 039."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_040(records, value=""):
    """Звіт за відповідальним, варіант 040."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_041(records, value=""):
    """Звіт за відповідальним, варіант 041."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_042(records, value=""):
    """Звіт за відповідальним, варіант 042."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_043(records, value=""):
    """Звіт за відповідальним, варіант 043."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_044(records, value=""):
    """Звіт за відповідальним, варіант 044."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_045(records, value=""):
    """Звіт за відповідальним, варіант 045."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_046(records, value=""):
    """Звіт за відповідальним, варіант 046."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_047(records, value=""):
    """Звіт за відповідальним, варіант 047."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_048(records, value=""):
    """Звіт за відповідальним, варіант 048."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_049(records, value=""):
    """Звіт за відповідальним, варіант 049."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_050(records, value=""):
    """Звіт за відповідальним, варіант 050."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_051(records, value=""):
    """Звіт за відповідальним, варіант 051."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_052(records, value=""):
    """Звіт за відповідальним, варіант 052."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_053(records, value=""):
    """Звіт за відповідальним, варіант 053."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_054(records, value=""):
    """Звіт за відповідальним, варіант 054."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_055(records, value=""):
    """Звіт за відповідальним, варіант 055."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_056(records, value=""):
    """Звіт за відповідальним, варіант 056."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_057(records, value=""):
    """Звіт за відповідальним, варіант 057."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_058(records, value=""):
    """Звіт за відповідальним, варіант 058."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_059(records, value=""):
    """Звіт за відповідальним, варіант 059."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_responsible_060(records, value=""):
    """Звіт за відповідальним, варіант 060."""
    selected = [row for row in _records(records) if str(_get(row, "responsible", "")) == value]
    return dashboard_snapshot(selected)

def report_tag_001(records, value=""):
    """Звіт за міткою, варіант 001."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_002(records, value=""):
    """Звіт за міткою, варіант 002."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_003(records, value=""):
    """Звіт за міткою, варіант 003."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_004(records, value=""):
    """Звіт за міткою, варіант 004."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_005(records, value=""):
    """Звіт за міткою, варіант 005."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_006(records, value=""):
    """Звіт за міткою, варіант 006."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_007(records, value=""):
    """Звіт за міткою, варіант 007."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_008(records, value=""):
    """Звіт за міткою, варіант 008."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_009(records, value=""):
    """Звіт за міткою, варіант 009."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_010(records, value=""):
    """Звіт за міткою, варіант 010."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_011(records, value=""):
    """Звіт за міткою, варіант 011."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_012(records, value=""):
    """Звіт за міткою, варіант 012."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_013(records, value=""):
    """Звіт за міткою, варіант 013."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_014(records, value=""):
    """Звіт за міткою, варіант 014."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_015(records, value=""):
    """Звіт за міткою, варіант 015."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_016(records, value=""):
    """Звіт за міткою, варіант 016."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_017(records, value=""):
    """Звіт за міткою, варіант 017."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_018(records, value=""):
    """Звіт за міткою, варіант 018."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_019(records, value=""):
    """Звіт за міткою, варіант 019."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_020(records, value=""):
    """Звіт за міткою, варіант 020."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_021(records, value=""):
    """Звіт за міткою, варіант 021."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_022(records, value=""):
    """Звіт за міткою, варіант 022."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_023(records, value=""):
    """Звіт за міткою, варіант 023."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_024(records, value=""):
    """Звіт за міткою, варіант 024."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_025(records, value=""):
    """Звіт за міткою, варіант 025."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_026(records, value=""):
    """Звіт за міткою, варіант 026."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_027(records, value=""):
    """Звіт за міткою, варіант 027."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_028(records, value=""):
    """Звіт за міткою, варіант 028."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_029(records, value=""):
    """Звіт за міткою, варіант 029."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_030(records, value=""):
    """Звіт за міткою, варіант 030."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_031(records, value=""):
    """Звіт за міткою, варіант 031."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_032(records, value=""):
    """Звіт за міткою, варіант 032."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_033(records, value=""):
    """Звіт за міткою, варіант 033."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_034(records, value=""):
    """Звіт за міткою, варіант 034."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_035(records, value=""):
    """Звіт за міткою, варіант 035."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_036(records, value=""):
    """Звіт за міткою, варіант 036."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_037(records, value=""):
    """Звіт за міткою, варіант 037."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_038(records, value=""):
    """Звіт за міткою, варіант 038."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_039(records, value=""):
    """Звіт за міткою, варіант 039."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_040(records, value=""):
    """Звіт за міткою, варіант 040."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_041(records, value=""):
    """Звіт за міткою, варіант 041."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_042(records, value=""):
    """Звіт за міткою, варіант 042."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_043(records, value=""):
    """Звіт за міткою, варіант 043."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_044(records, value=""):
    """Звіт за міткою, варіант 044."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_045(records, value=""):
    """Звіт за міткою, варіант 045."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_046(records, value=""):
    """Звіт за міткою, варіант 046."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_047(records, value=""):
    """Звіт за міткою, варіант 047."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_048(records, value=""):
    """Звіт за міткою, варіант 048."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_049(records, value=""):
    """Звіт за міткою, варіант 049."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_050(records, value=""):
    """Звіт за міткою, варіант 050."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_051(records, value=""):
    """Звіт за міткою, варіант 051."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_052(records, value=""):
    """Звіт за міткою, варіант 052."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_053(records, value=""):
    """Звіт за міткою, варіант 053."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_054(records, value=""):
    """Звіт за міткою, варіант 054."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_055(records, value=""):
    """Звіт за міткою, варіант 055."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_056(records, value=""):
    """Звіт за міткою, варіант 056."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_057(records, value=""):
    """Звіт за міткою, варіант 057."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_058(records, value=""):
    """Звіт за міткою, варіант 058."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_059(records, value=""):
    """Звіт за міткою, варіант 059."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_tag_060(records, value=""):
    """Звіт за міткою, варіант 060."""
    selected = [row for row in _records(records) if value.lower() in str(_get(row, "tags", "")).lower()]
    return dashboard_snapshot(selected)

def report_status_001(records, value="progress"):
    """Звіт за статусом, варіант 001."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_002(records, value="progress"):
    """Звіт за статусом, варіант 002."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_003(records, value="progress"):
    """Звіт за статусом, варіант 003."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_004(records, value="progress"):
    """Звіт за статусом, варіант 004."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_005(records, value="progress"):
    """Звіт за статусом, варіант 005."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_006(records, value="progress"):
    """Звіт за статусом, варіант 006."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_007(records, value="progress"):
    """Звіт за статусом, варіант 007."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_008(records, value="progress"):
    """Звіт за статусом, варіант 008."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_009(records, value="progress"):
    """Звіт за статусом, варіант 009."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_010(records, value="progress"):
    """Звіт за статусом, варіант 010."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_011(records, value="progress"):
    """Звіт за статусом, варіант 011."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_012(records, value="progress"):
    """Звіт за статусом, варіант 012."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_013(records, value="progress"):
    """Звіт за статусом, варіант 013."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_014(records, value="progress"):
    """Звіт за статусом, варіант 014."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_015(records, value="progress"):
    """Звіт за статусом, варіант 015."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_016(records, value="progress"):
    """Звіт за статусом, варіант 016."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_017(records, value="progress"):
    """Звіт за статусом, варіант 017."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_018(records, value="progress"):
    """Звіт за статусом, варіант 018."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_019(records, value="progress"):
    """Звіт за статусом, варіант 019."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_020(records, value="progress"):
    """Звіт за статусом, варіант 020."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_021(records, value="progress"):
    """Звіт за статусом, варіант 021."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_022(records, value="progress"):
    """Звіт за статусом, варіант 022."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_023(records, value="progress"):
    """Звіт за статусом, варіант 023."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_024(records, value="progress"):
    """Звіт за статусом, варіант 024."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_025(records, value="progress"):
    """Звіт за статусом, варіант 025."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_026(records, value="progress"):
    """Звіт за статусом, варіант 026."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_027(records, value="progress"):
    """Звіт за статусом, варіант 027."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_028(records, value="progress"):
    """Звіт за статусом, варіант 028."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_029(records, value="progress"):
    """Звіт за статусом, варіант 029."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_030(records, value="progress"):
    """Звіт за статусом, варіант 030."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_031(records, value="progress"):
    """Звіт за статусом, варіант 031."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_032(records, value="progress"):
    """Звіт за статусом, варіант 032."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_033(records, value="progress"):
    """Звіт за статусом, варіант 033."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_034(records, value="progress"):
    """Звіт за статусом, варіант 034."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_035(records, value="progress"):
    """Звіт за статусом, варіант 035."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_036(records, value="progress"):
    """Звіт за статусом, варіант 036."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_037(records, value="progress"):
    """Звіт за статусом, варіант 037."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_038(records, value="progress"):
    """Звіт за статусом, варіант 038."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_039(records, value="progress"):
    """Звіт за статусом, варіант 039."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_040(records, value="progress"):
    """Звіт за статусом, варіант 040."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_041(records, value="progress"):
    """Звіт за статусом, варіант 041."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_042(records, value="progress"):
    """Звіт за статусом, варіант 042."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_043(records, value="progress"):
    """Звіт за статусом, варіант 043."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_044(records, value="progress"):
    """Звіт за статусом, варіант 044."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_045(records, value="progress"):
    """Звіт за статусом, варіант 045."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_046(records, value="progress"):
    """Звіт за статусом, варіант 046."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_047(records, value="progress"):
    """Звіт за статусом, варіант 047."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_048(records, value="progress"):
    """Звіт за статусом, варіант 048."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_049(records, value="progress"):
    """Звіт за статусом, варіант 049."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_050(records, value="progress"):
    """Звіт за статусом, варіант 050."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_051(records, value="progress"):
    """Звіт за статусом, варіант 051."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_052(records, value="progress"):
    """Звіт за статусом, варіант 052."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_053(records, value="progress"):
    """Звіт за статусом, варіант 053."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_054(records, value="progress"):
    """Звіт за статусом, варіант 054."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_055(records, value="progress"):
    """Звіт за статусом, варіант 055."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_056(records, value="progress"):
    """Звіт за статусом, варіант 056."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_057(records, value="progress"):
    """Звіт за статусом, варіант 057."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_058(records, value="progress"):
    """Звіт за статусом, варіант 058."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_059(records, value="progress"):
    """Звіт за статусом, варіант 059."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)

def report_status_060(records, value="progress"):
    """Звіт за статусом, варіант 060."""
    selected = [row for row in _records(records) if _status(row) == value]
    return dashboard_snapshot(selected)



def engine_info():
    """Метадані локального двигуна для сторінки стану системи."""
    return {"version": APP_VERSION, "name": ENGINE_NAME, "network": False, "storage": "локальна файлова система", "database": "SQLite"}


def health_check(workspace):
    """Перевірка локального робочого середовища без мережевих викликів."""
    root = Path(workspace).resolve()
    return {"workspace_exists": root.exists(), "workspace_writable": root.exists() and root.is_dir(), "database_exists": (root / "database.db").exists(), "orders_exists": (root / "Розпорядження").exists(), "backups_exists": (root / "Резервні копії").exists()}


__all__ = [name for name in globals() if name.startswith("metric_") or name.startswith("deadline_metric_") or name.startswith("report_")] + ["annual_summary", "monthly_comparison", "priority_load", "response_statistics", "document_statistics", "responsible_statistics", "category_statistics", "tag_statistics", "workload_index", "urgency_index", "search_score", "rank_records", "completion_by_period", "average_completion_days", "sla_rate", "dashboard_snapshot", "engine_info", "health_check"]
