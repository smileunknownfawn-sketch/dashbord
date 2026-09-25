"""Тимчасова точка запуску для перевірки інтерфейсу перед автономною EXE-збіркою."""

import traceback
from pathlib import Path

import streamlit as st


# Внутрішні назви БД залишаються технічними, але користувачеві вони ніколи
# не повинні показуватися як id, number, deadline, status тощо.
_DISPLAY_NAMES = {
    "id": "Ідентифікатор",
    "number": "Номер",
    "received_date": "Дата отримання",
    "deadline": "Термін виконання",
    "description": "Короткий опис",
    "status": "Статус",
    "priority": "Пріоритет",
    "responsible": "Відповідальний",
    "category": "Категорія",
    "tags": "Мітки",
    "completion_outgoing": "Вихідний номер",
    "completion_date": "Дата виконання",
    "folder": "Папка",
    "filename": "Файл",
    "mime": "Тип файлу",
    "path": "Шлях до файлу",
    "order_id": "Розпорядження",
    "response_date": "Дата відповіді",
    "outgoing": "Вихідний номер",
    "comment": "Зміст відповіді",
    "is_final": "Виконано",
    "created_at": "Дата створення",
    "deleted_at": "Дата видалення",
    "event_type": "Подія",
    "details": "Деталі",
}


def _ukrainian_dataframe(data):
    """Повертає копію табличних даних із людськими українськими заголовками."""
    try:
        import pandas as pd
        if isinstance(data, pd.DataFrame):
            result = data.copy()
            result.rename(columns=_DISPLAY_NAMES, inplace=True)
            return result
        if isinstance(data, list) and data and isinstance(data[0], dict):
            return [{_DISPLAY_NAMES.get(str(k), str(k)): v for k, v in row.items()} for row in data]
    except Exception:
        pass
    return data


_original_dataframe = st.dataframe


def _localized_dataframe(data=None, *args, **kwargs):
    return _original_dataframe(_ukrainian_dataframe(data), *args, **kwargs)


st.dataframe = _localized_dataframe

from app_v3 import main


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log_dir = Path(__file__).resolve().parent / "data"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "last_error.log"
        log_file.write_text(traceback.format_exc(), encoding="utf-8")
        st.error("Виникла внутрішня помилка програми. Дані не видалено.")
        st.info("Технічний журнал збережено локально у папці data/last_error.log.")
