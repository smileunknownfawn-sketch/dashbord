from __future__ import annotations

from datetime import date
from pathlib import Path

from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.storage import LocalStorage


def test_order_and_response_files_use_order_folder(tmp_path: Path):
    paths = AppPaths.from_root(tmp_path / "Дані")
    paths.ensure()
    db = Database(paths.database)
    storage = LocalStorage(paths)
    service = OrderService(db, storage)

    order_id = service.create(
        number="1111",
        received=date(2026, 9, 26),
        deadline=date(2026, 10, 1),
        description="Тестове розпорядження",
        file_name="order.pdf",
        file_bytes=b"order",
    )
    order = db.get_order(order_id)
    assert (paths.orders / "1111" / "order.pdf").is_file()

    response_id = service.add_response(
        order,
        response_date=date(2026, 9, 26),
        outgoing="В-01",
        comment="Виконано",
        file_name="response.pdf",
        file_bytes=b"response",
        final=True,
    )
    responses = db.get_responses(order_id)
    response = next(row for row in responses if int(row["id"]) == response_id)
    assert Path(response["path"]).parts[-2] == "Відповідь"
    assert (paths.orders / "1111" / "Відповідь" / "response.pdf").is_file()

    attachment = tmp_path / "додаток.pdf"
    attachment.write_bytes(b"attachment")
    service.add_response_attachment(order_id, response_id, attachment)
    assert (paths.orders / "1111" / "Відповідь" / "Додатки" / "додаток.pdf").is_file()
