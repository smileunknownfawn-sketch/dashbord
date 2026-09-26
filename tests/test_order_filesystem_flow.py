from __future__ import annotations

from datetime import date
from pathlib import Path

from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.storage import LocalStorage


def test_order_response_and_attachments_are_stored_in_order_folder(tmp_path: Path):
    paths = AppPaths.from_root(tmp_path)
    paths.ensure()
    db = Database(paths.database)
    storage = LocalStorage(paths)
    service = OrderService(db, storage)

    order_id = service.create(
        number="1111",
        received=date(2026, 9, 25),
        deadline=date(2026, 10, 1),
        description="Тестове розпорядження",
        file_name="rozporyadzhennia.pdf",
        file_bytes=b"order",
    )
    order = db.get_order(order_id)
    order_dir = paths.orders / order["folder"]
    assert order_dir.is_dir()
    assert (order_dir / "rozporyadzhennia.pdf").is_file()

    response_id = service.add_response(
        order,
        response_date=date(2026, 9, 26),
        outgoing="В-1111",
        comment="Відповідь",
        file_name="vidpovid.pdf",
        file_bytes=b"response",
        final=False,
    )
    response_dir = order_dir / "Відповідь"
    assert (response_dir / "vidpovid.pdf").is_file()

    source = tmp_path / "dod.pdf"
    source.write_bytes(b"attachment")
    service.add_response_attachment(order_id, response_id, source)
    assert (response_dir / "Додатки" / "dod.pdf").is_file()

    order_source = tmp_path / "dod_order.pdf"
    order_source.write_bytes(b"order attachment")
    service.add_attachment(order_id, order_source)
    assert (order_dir / "Додатки" / "dod_order.pdf").is_file()
