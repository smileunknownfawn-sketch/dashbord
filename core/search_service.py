"""Локальний повнотекстовий пошук для реєстру розпоряджень."""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable


STOP_WORDS = {
    "і", "й", "та", "або", "до", "на", "у", "в", "з", "із", "за", "по",
    "для", "про", "що", "як", "це", "не", "а", "але", "від", "при", "такий",
}

SEARCH_FIELDS = (
    "number", "description", "responsible", "category", "priority", "tags",
    "outgoing", "completion_outgoing", "comment", "response_text", "filename",
    "original_filename", "status",
)

FIELD_LABELS = {
    "number": "номер",
    "description": "короткий опис",
    "responsible": "відповідальний",
    "category": "категорія",
    "priority": "пріоритет",
    "tags": "мітки",
    "outgoing": "вихідний номер",
    "completion_outgoing": "вихідний номер",
    "comment": "відповідь",
    "response_text": "відповідь",
    "filename": "файл",
    "original_filename": "файл",
    "status": "статус",
}


def normalize_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.casefold().replace("’", "'").replace("`", "'")
    text = re.sub(r"[^\w\s./-]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def tokenize(query: str) -> list[str]:
    tokens = normalize_text(query).split()
    return [token for token in tokens if len(token) >= 2 and token not in STOP_WORDS]


def _value_text(row: dict[str, Any], field: str) -> str:
    return normalize_text(row.get(field, ""))


def _score_token(token: str, text: str, field: str) -> int:
    if not text:
        return 0
    if token == text:
        return 100
    words = text.split()
    if token in words:
        return 80
    if any(word.startswith(token) for word in words):
        return 55
    if token in text:
        return 30
    return 0


def score_row(row: dict[str, Any], query: str) -> tuple[int, list[str]]:
    tokens = tokenize(query)
    if not tokens:
        return 0, []

    score = 0
    matched: list[str] = []
    for token in tokens:
        token_score = 0
        token_field = None
        for field in SEARCH_FIELDS:
            current = _score_token(token, _value_text(row, field), field)
            if current > token_score:
                token_score = current
                token_field = field
        if token_score:
            score += token_score
            if token_field:
                label = FIELD_LABELS.get(token_field, token_field)
                matched.append(f"{label}: {token}")
        else:
            # Усі слова запиту мають бути представлені у результаті.
            return 0, []

    # Повний збіг у номері отримує додаткову вагу.
    number = _value_text(row, "number")
    if normalize_text(query) == number:
        score += 250
    return score, matched


@dataclass(frozen=True)
class SearchResult:
    row: dict[str, Any]
    score: int
    matches: tuple[str, ...]


def search_rows(rows: Iterable[dict[str, Any]], query: str, limit: int = 100) -> list[SearchResult]:
    query = query.strip()
    if not query:
        return [SearchResult(row, 0, ()) for row in list(rows)[:limit]]

    results: list[SearchResult] = []
    for row in rows:
        score, matches = score_row(row, query)
        if score > 0:
            results.append(SearchResult(row, score, tuple(matches)))
    results.sort(key=lambda item: (-item.score, str(item.row.get("number", ""))))
    return results[:max(1, limit)]


def explain_result(result: SearchResult) -> str:
    if not result.matches:
        return ""
    return " • ".join(result.matches)
