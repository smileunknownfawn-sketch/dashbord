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
        if left < 0:
            return f"прострочено на {abs(left)} дн."
        if left == 0:
            return "термін сьогодні"
        if left == 1:
            return "залишився 1 день"
        return f"залишилось {left} дн."

    def create(self, *, number: str, received: date, deadline: date, description: str,
               file_name: str, file_bytes: bytes, mime: str = "",
               priority: str = "Звичайний", responsible: str = "",
               category: str = "Інше", tags: str = "") -> int:
        number, description = number.strip(), description.strip()
        if not number:
            raise ValueError("Вкажіть номер розпорядження")
        if not description:
            raise ValueError("Вкажіть короткий опис розпорядження")
        if deadline < received:
            raise ValueError("Дата виконання не може бути раніше дати отримання")

        folder_name = self.storage.clean_name(number)
        folder = self.storage.paths.orders / folder_name
        counter = 2
        while folder.exists():
            folder = self.storage.paths.orders / f"{folder_name}_{counter}"
            counter += 1
        folder.mkdir(parents=True, exist_ok=True)

        document = self.storage.save_bytes(folder, file_name, file_bytes)
        mime = mime or mimetypes.guess_type(document.name)[0] or "application/octet-stream"
        now = datetime.now().isoformat(timespec="seconds")
        oid = self.db.execute(
            "INSERT INTO orders(number,deadline,description,folder,filename,path,mime,status,priority,responsible,category,received_date,tags,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (number, deadline.isoformat(), description, folder.name, document.name,
             str(document.relative_to(self.storage.paths.root)), mime, "progress", priority,
             responsible.strip(), category, received.isoformat(), tags.strip(), now, now),
        )
        self.db.log(oid, "Створено", f"№ {number}")
        return oid

    def update(self, order_id: int, *, number: str, deadline: date, description: str,
               priority: str, responsible: str, category: str, tags: str) -> None:
        if not number.strip() or not description.strip():
            raise ValueError("Номер і короткий опис є обов'язковими")
        self.db.execute(
            "UPDATE orders SET number=?,deadline=?,description=?,priority=?,responsible=?,category=?,tags=?,updated_at=? WHERE id=?",
            (number.strip(), deadline.isoformat(), description.strip(), priority,
             responsible.strip(), category, tags.strip(), datetime.now().isoformat(timespec="seconds"), order_id),
        )
        self.db.log(order_id, "Змінено", "Оновлено реквізити розпорядження")

    def _response_folder(self, order: Any) -> Path:
        base = self.storage.paths.orders / order["folder"]
        folder = base / "Відповідь"
        counter = 2
        while folder.exists():
            folder = base / f"Відповідь_{counter}"
            counter += 1
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def add_response(self, order: Any, *, response_date: date, outgoing: str,
                     comment: str, file_name: str, file_bytes: bytes,
                     mime: str = "", final: bool = False) -> int:
        folder = self._response_folder(order)
        document = self.storage.save_bytes(folder, file_name, file_bytes)
        mime = mime or mimetypes.guess_type(document.name)[0] or "application/octet-stream"
        rid = self.db.execute(
            "INSERT INTO responses(order_id,response_date,outgoing,comment,filename,path,mime,is_final,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (order["id"], response_date.isoformat(), outgoing.strip(), comment.strip(),
             document.name, str(document.relative_to(self.storage.paths.root)), mime,
             int(final), datetime.now().isoformat(timespec="seconds")),
        )
        self.db.log(order["id"], "Додано відповідь", outgoing.strip() or "Без вихідного номера")
        if final:
            self.db.execute(
                "UPDATE orders SET status='done',completion_outgoing=?,updated_at=? WHERE id=?",
                (outgoing.strip(), datetime.now().isoformat(timespec="seconds"), order["id"]),
            )
            self.db.log(order["id"], "Виконано", outgoing.strip() or "Відповідь без вихідного номера")
        return rid

    def add_attachment(self, order_id: int, source: Path, *, response_id: int = 0) -> int:
        order = self.db.get_order(order_id, include_deleted=True)
        if not order:
            raise ValueError("Розпорядження не знайдено")
        if not source.exists() or not source.is_file():
            raise FileNotFoundError("Файл додатка не знайдено")

        if response_id:
            responses = [r for r in self.db.get_responses(order_id) if int(r["id"]) == int(response_id)]
            if not responses:
                raise ValueError("Відповідь не знайдено")
            response_path = self.storage.safe(responses[0]["path"])
            folder = response_path.parent / "Додатки"
        else:
            folder = self.storage.paths.orders / order["folder"] / "Додатки"

        document = self.storage.save_bytes(folder, source.name, source.read_bytes())
        mime = mimetypes.guess_type(document.name)[0] or "application/octet-stream"
        aid = self.db.execute(
            "INSERT INTO attachments(order_id,response_id,filename,path,mime,created_at) VALUES(?,?,?,?,?,?)",
            (order_id, response_id, document.name,
             str(document.relative_to(self.storage.paths.root)), mime,
             datetime.now().isoformat(timespec="seconds")),
        )
        self.db.log(order_id, "Додано додаток", document.name)
        return aid

    def add_response_attachment(self, order_id: int, response_id: int, source: Path) -> int:
        return self.add_attachment(order_id, source, response_id=response_id)

    def reopen(self, order_id: int) -> None:
        self.db.execute(
            "UPDATE orders SET status='progress',completion_outgoing='',updated_at=? WHERE id=?",
            (datetime.now().isoformat(timespec="seconds"), order_id),
        )
        self.db.log(order_id, "Статус змінено", "Розпорядження повернуто в роботу")

    def mark_done(self, order_id: int, outgoing: str = "") -> None:
        self.db.execute(
            "UPDATE orders SET status='done',completion_outgoing=?,updated_at=? WHERE id=?",
            (outgoing.strip(), datetime.now().isoformat(timespec="seconds"), order_id),
        )
        self.db.log(order_id, "Виконано", outgoing.strip())

    def move_to_trash(self, order: Any) -> Path:
        source = self.storage.paths.orders / order["folder"]
        if not source.exists():
            raise FileNotFoundError("Папку розпорядження не знайдено")
        target = self.storage.paths.trash / f"{datetime.now():%Y%m%d_%H%M%S}_{self.storage.clean_name(order['number'])}"
        counter = 2
        while target.exists():
            target = self.storage.paths.trash / f"{target.name}_{counter}"
            counter += 1
        source.rename(target)
        self.db.move_to_trash(order["id"], str(target.relative_to(self.storage.paths.root)))
        return target

    def restore(self, order_id: int) -> Path:
        order = self.db.get_order(order_id, include_deleted=True)
        if not order or not order["deleted_at"]:
            raise ValueError("Розпорядження не перебуває у кошику")
        source = self.storage.safe(order["deleted_path"])
        if not source.exists():
            raise FileNotFoundError("Файли розпорядження у кошику не знайдено")
        target = self.storage.paths.orders / order["folder"]
        if target.exists():
            target = self.storage.paths.orders / f"{order['folder']}_відновлено"
        source.rename(target)
        self.db.restore_from_trash(order_id)
        return target

    def purge(self, order_id: int) -> None:
        order = self.db.get_order(order_id, include_deleted=True)
        if not order:
            return
        if order["deleted_path"]:
            path = self.storage.safe(order["deleted_path"])
            if path.exists():
                import shutil
                shutil.rmtree(path, ignore_errors=True)
        self.db.purge_order(order_id)
