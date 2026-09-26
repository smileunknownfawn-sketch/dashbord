from datetime import date, timedelta

from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.search_service import search_rows
from core.storage import LocalStorage


def test_100_documents_create_search_and_status(tmp_path):
    paths = AppPaths.from_root(tmp_path / "data")
    paths.ensure()
    db = Database(paths.database)
    storage = LocalStorage(paths)
    service = OrderService(db, storage)
    for i in range(100):
        service.create(number=f"TEST-{i:04d}", received=date.today(), deadline=date.today() + timedelta(days=(i % 7) + 1), description=f"Тестове забезпечення майном номер {i}", file_name=f"document_{i:04d}.txt", file_bytes=f"Тестовий документ {i}".encode("utf-8"), responsible="Тестовий відповідальний", category="Матеріальне", tags="тест майно")
    rows = [dict(r) for r in db.get_orders()]
    assert len(rows) == 100
    assert len(search_rows(rows, "забезпечення майном")) == 100
    assert len(search_rows(rows, "TEST-0099")) == 1
    service.mark_done(rows[0]["id"], "TEST/100")
    assert service.status(db.get_order(rows[0]["id"])) == "done"
    service.move_to_trash(db.get_order(rows[1]["id"]))
    assert len(db.get_trash()) == 1
    service.restore(rows[1]["id"])
    assert len(db.get_trash()) == 0
