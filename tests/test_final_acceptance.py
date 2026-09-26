from datetime import date
from pathlib import Path

from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.storage import LocalStorage


def make_app(tmp_path: Path):
    paths = AppPaths.from_root(tmp_path / "data")
    paths.ensure()
    db = Database(paths.database)
    storage = LocalStorage(paths)
    return paths, db, storage, OrderService(db, storage)


def test_100_orders_search_and_status(tmp_path):
    paths, db, storage, service = make_app(tmp_path)
    for i in range(100):
        service.create(number=f"ТЕСТ-{i:04d}", received=date(2026, 1, 1), deadline=date(2026, 12, 31), description=f"Короткий опис розпорядження для перевірки {i}", file_name=f"document_{i}.txt", file_bytes=f"Документ {i}".encode("utf-8"), responsible=f"Відповідальний {i % 5}", tags="контроль тест")
    rows = [dict(r) for r in db.get_orders()]
    assert len(rows) == 100
    assert any("ТЕСТ-0042" in r["number"] for r in rows)
    assert sum(service.status(r, date(2026, 1, 1)) == "progress" for r in rows) == 100
    assert storage.validate() == []


def test_attachments_response_trash_restore_and_purge(tmp_path):
    paths, db, storage, service = make_app(tmp_path)
    order_id = service.create(number="АТТ-1", received=date(2026, 1, 1), deadline=date(2026, 1, 20), description="Перевірка додатків", file_name="order.pdf", file_bytes=b"pdf")
    source = tmp_path / "attachment.xlsx"; source.write_bytes(b"xlsx")
    aid = service.add_attachment(order_id, source)
    assert aid > 0
    assert (paths.orders / "АТТ-1" / "Додатки").exists()
    row = db.get_order(order_id)
    rid = service.add_response(row, response_date=date(2026, 1, 5), outgoing="ВИХ-1", comment="Готово", file_name="response.pdf", file_bytes=b"response")
    assert rid > 0
    response_folder = paths.orders / "АТТ-1" / "Відповідь"
    assert response_folder.exists()
    service.add_response_attachment(order_id, rid, source)
    assert (response_folder / "Додатки").exists()
    assert any(p.name == "attachment.xlsx" for p in (response_folder / "Додатки").iterdir())
    service.move_to_trash(db.get_order(order_id))
    assert db.get_order(order_id) is None
    assert db.get_order(order_id, include_deleted=True) is not None
    service.restore(order_id)
    assert db.get_order(order_id) is not None
    service.move_to_trash(db.get_order(order_id))
    service.purge(order_id)
    assert db.get_order(order_id, include_deleted=True) is None


def test_deadline_validation(tmp_path):
    _, _, _, service = make_app(tmp_path)
    try:
        service.create(number="BAD", received=date(2026, 2, 2), deadline=date(2026, 2, 1), description="x", file_name="x.txt", file_bytes=b"x")
    except ValueError as exc:
        assert "раніше" in str(exc)
    else:
        raise AssertionError("Некоректний термін не був відхилений")
