"""Українські назви технічних полів та повідомлень інтерфейсу."""
from __future__ import annotations

FIELD_LABELS_UA = {
    "id": "Ідентифікатор", "number": "Номер", "received_date": "Дата отримання",
    "deadline": "Термін виконання", "description": "Короткий опис", "status": "Статус",
    "priority": "Пріоритет", "responsible": "Відповідальний", "category": "Категорія",
    "tags": "Мітки", "outgoing": "Вихідний номер", "completion_outgoing": "Вихідний номер",
    "completion_date": "Дата виконання", "filename": "Файл", "response_date": "Дата відповіді",
    "comment": "Зміст відповіді", "response_text": "Текст відповіді", "created_at": "Дата створення",
    "deleted_at": "Дата видалення", "event_type": "Подія", "details": "Деталі",
}

PLACEHOLDERS_UA = {
    "number": "Введіть номер розпорядження",
    "description": "Введіть короткий опис розпорядження",
    "responsible": "Введіть прізвище та ініціали відповідального",
    "category": "Оберіть категорію",
    "priority": "Оберіть пріоритет",
    "tags": "Введіть мітки через кому",
    "outgoing": "Введіть вихідний номер, якщо він є",
    "comment": "Введіть зміст відповіді",
    "search": "Пошук за номером, словами, відповідальним, мітками або файлами…",
}

MESSAGES_UA = {
    "saved": "Зміни успішно збережено.",
    "deleted": "Розпорядження переміщено до кошика.",
    "restored": "Розпорядження відновлено.",
    "backup_created": "Резервну копію створено.",
    "no_results": "За вашим запитом нічого не знайдено.",
    "offline": "Автономний режим — дані зберігаються лише на цьому комп’ютері.",
}

def label(field: str) -> str:
    return FIELD_LABELS_UA.get(field, field)

def placeholder(field: str) -> str:
    return PLACEHOLDERS_UA.get(field, "Введіть значення")
