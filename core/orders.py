from __future__ import annotations

import mimetypes
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .database import Database
from .storage import LocalStorage

DONE = {"done", "виконано", "completed"}


class OrderService:
    def __init__(self, db: Database, storage: LocalStorage):
        self.db = db
        self.storage = storage

    @staticmethod
    def status(row: Any, today: date | None = None) -> str:
        if str(row["status"]).lower() in DONE:
            return "done"
        anchor = today or date.today()
        try:
            deadline = date.fromisoformat(str(row["deadline"]))
        except (TypeError, ValueError):
            return "progress"
        if deadline < anchor:
            return "overdue"
        if deadline == anchor:
            return "today"
        return "progress"

    @staticmethod
    def remaining(value: Any, today: date | None = None) -> str:
        try:
            left = (date.fromisoformat(str(value)) - (today or date.today())).days
        except (TypeError, ValueError):
            return "Термін не вказано"
        if left < 0: return f"прострочено на {abs(left)} дн."
        if left == 0: return "термін сьогодні"
        if left == 1: return "залишився 1 день"
        return f"залишилось {left} дн."

    def create(self, *, number: str, received: date, deadline: date, description: str, file_name: str, file_bytes: bytes, mime: str = "", priority: str = "Звичайний", responsible: str = "", category: str = "Інше", tags: str = "") -> int:
        number, description = number.strip(), description.strip()
        if not number: raise ValueError("Вкажіть номер розпорядження")
        if not description: raise ValueError("Вкажіть короткий опис розпорядження")
        if deadline < received: raise ValueError("Дата виконання не може бути раніше дати отримання")
        folder_name = self.storage.clean_name(number)
        folder = self.storage.paths.orders / folder_name
        counter = 2
        while folder.exists():
            folder = self.storage.paths.orders / f"{folder_name}_{counter}"; counter += 1
        folder.mkdir(parents=True, exist_ok=True)
        document = self.storage.save_bytes(folder, file_name, file_bytes)
        mime = mime or mimetypes.guess_type(document.name)[0] or "application/octet-stream"
        now = datetime.now().isoformat(timespec="seconds")
        oid = self.db.execute("INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,priority,responsible,category,received_date,tags,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (number, deadline.isoformat(), description, folder.name, document.name, str(document.relative_to(self.storage.paths.root)), mime, "progress", priority, responsible.strip(), category, received.isoformat(), tags.strip(), now, now))
        self.db.log(oid, "Створено", f"№ {number}")
        return oid

    def update(self, order_id: int, *, number: str, deadline: date, description: str, priority: str, responsible: str, category: str, tags: str) -> None:
        if not number.strip() or not description.strip(): raise ValueError("Номер і короткий опис є обов'язковими")
        self.db.execute("UPDATE orders SET number=?,deadline=?,description=?,priority=?,responsible=?,category=?,tags=?,updated_at=? WHERE id=?", (number.strip(), deadline.isoformat(), description.strip(), priority, responsible.strip(), category, tags.strip(), datetime.now().isoformat(timespec="seconds"), order_id))
        self.db.log(order_id, "Змінено", "Оновлено реквізити розпорядження")

    def add_response(self, order: Any, *, response_date: date, outgoing: str, comment: str, file_name: str, file_bytes: bytes, mime: str = "", final: bool = False) -> int:
        folder = self.storage.paths.orders / order["folder"] / "Відповіді"
        document = self.storage.save_bytes(folder, file_name, file_bytes)
        mime = mime or mimetypes.guess_type(document.name)[0] or "application/octet-stream"
        rid = self.db.execute("INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at) VALUES(?,?,?,?,?,?,?,?,?)", (order["id"], response_date.isoformat(), outgoing.strip(), comment.strip(), document.name, str(document.relative_to(self.storage.paths.root)), mime, int(final), datetime.now().isoformat(timespec="seconds")))
        self.db.log(order["id"], "Додано відповідь", outgoing.strip() or "Без вихідного номера")
        if final:
            self.db.execute("UPDATE orders SET status='done',completion_outgoing=?,updated_at=? WHERE id=?", (outgoing.strip(), datetime.now().isoformat(timespec="seconds"), order["id"]))
            self.db.log(order["id"], "Виконано", outgoing.strip() or "Відповідь без вихідного номера")
        return rid

    def reopen(self, order_id: int) -> None:
        self.db.execute("UPDATE orders SET status='progress',completion_outgoing='',updated_at=? WHERE id=?", (datetime.now().isoformat(timespec="seconds"), order_id))
        self.db.log(order_id, "Статус змінено", "Розпорядження повернуто в роботу")

    def mark_done(self, order_id: int, outgoing: str = "") -> None:
        self.db.execute("UPDATE orders SET status='done',completion_outgoing=?,updated_at=? WHERE id=?", (outgoing.strip(), datetime.now().isoformat(timespec="seconds"), order_id))
        self.db.log(order_id, "Виконано", outgoing.strip())

    def move_to_trash(self, order: Any) -> Path:
        source = self.storage.paths.orders / order["folder"]
        if not source.exists(): raise FileNotFoundError("Папку розпорядження не знайдено")
        target = self.storage.paths.trash / f"{datetime.now():%Y%m%d_%H%M%S}_{self.storage.clean_name(order['number'])}"
        counter = 2
        while target.exists(): target = self.storage.paths.trash / f"{target.name}_{counter}"; counter += 1
        source.rename(target)
        self.db.move_to_trash(order["id"])
        return target

    def restore(self, order_id: int) -> Path:
        order = self.db.get_order(order_id, include_deleted=True)
        if not order or not order["deleted_at"]: raise ValueError("Розпорядження не перебуває у кошику")
        trash_root = self.storage.paths.trash
        candidates = [p for p in trash_root.iterdir() if p.is_dir() and self.storage.clean_name(order["number"]) in p.name]
        if not candidates: raise FileNotFoundError("Файли розпорядження у кошику не знайдено")
        source = sorted(candidates)[-1]
        target = self.storage.paths.orders / order["folder"]
        if target.exists(): target = self.storage.paths.orders / f"{order['folder']}_відновлено"
        source.rename(target)
        self.db.restore_from_trash(order_id)
        return target

    def purge(self, order_id: int) -> None:
        order = self.db.get_order(order_id, include_deleted=True)
        if not order: return
        for p in self.storage.paths.trash.glob(f"*_{self.storage.clean_name(order['number'])}*"):
            if p.is_dir():
                import shutil; shutil.rmtree(p, ignore_errors=True)
        self.db.purge_order(order_id)
