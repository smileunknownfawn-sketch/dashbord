from datetime import date, timedelta
from pathlib import Path

from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.search_service import search_rows
from core.storage import LocalStorage


def build_service(tmp_path):
    paths = AppPaths.from_root(tmp_path)
    paths.ensure()
    db = Database(paths.database)
    storage = LocalStorage(paths)
    return db, storage, OrderService(db, storage), paths


def test_full_document_lifecycle(tmp_path):
    db, storage, service, paths = build_service(tmp_path)
    order_id = service.create(
        number="1111",
        received=date.today(),
        deadline=date.today() + timedelta(days=3),
        description="Перевірка бойової готовності",
        file_name="order.pdf",
        file_bytes=b"order",
        responsible="Іваненко",
        category="Бойова підготовка",
        tags="готовність тест",
    )
    order = db.get_order(order_id)
    assert order is not None
    assert (paths.orders / "1111" / "order.pdf").exists()

    attachment = tmp_path / "appendix.pdf"
    attachment.write_bytes(b"appendix")
    service.add_attachment(order_id, attachment)
    assert (paths.orders / "1111" / "Додатки" / "appendix.pdf").exists()

    response = tmp_path / "answer.pdf"
    response.write_bytes(b"answer")
    response_id = service.add_response(
        order,
        response_date=date.today(),
        outgoing="42/01",
        comment="Виконано",
        file_name=response.name,
        file_bytes=response.read_bytes(),
        final=True,
    )
    assert response_id > 0
    assert (paths.orders / "1111" / "Відповідь" / "answer.pdf").exists()
    assert db.get_order(order_id)["status"] == "done"

    response_attachment = tmp_path / "answer_appendix.pdf"
    response_attachment.write_bytes(b"response appendix")
    service.add_response_attachment(order_id, response_id, response_attachment)
    assert (paths.orders / "1111" / "Відповідь" / "Додатки" / "answer_appendix.pdf").exists()

    service.reopen(order_id)
    assert db.get_order(order_id)["status"] == "progress"
    service.mark_done(order_id)
    assert db.get_order(order_id)["status"] == "done"

    rows = [dict(r) for r in db.get_orders()]
    assert search_rows(rows, "бойової")
    assert search_rows(rows, "Іваненко")
    assert search_rows(rows, "готовність")
    assert search_rows(rows, "1111")

    target = service.move_to_trash(db.get_order(order_id))
    assert target.exists()
    assert not (paths.orders / "1111").exists()
    service.restore(order_id)
    assert (paths.orders / "1111").exists()

    service.move_to_trash(db.get_order(order_id))
    service.purge(order_id)
    assert db.get_order(order_id, include_deleted=True) is None
