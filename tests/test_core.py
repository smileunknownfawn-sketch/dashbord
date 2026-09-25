from datetime import date, timedelta
from pathlib import Path

from core.analytics import metrics, monthly, distribution
from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.storage import LocalStorage, StorageError


def row(**overrides):
    data = {
        "id": 1,
        "number": "1111",
        "deadline": date.today().isoformat(),
        "received_date": date.today().isoformat(),
        "description": "Тест",
        "status": "progress",
        "priority": "Звичайний",
        "responsible": "Тест",
        "category": "Інше",
        "tags": "",
    }
    data.update(overrides)
    return data


def test_metrics():
    rows = [row(), row(id=2, status="done"), row(id=3, deadline=(date.today() - timedelta(days=2)).isoformat())]
    result = metrics(rows)
    assert result.total == 3
    assert result.completed == 1
    assert result.overdue == 1
    assert result.today == 1


def test_monthly():
    rows = [row(received_date="2026-01-02"), row(id=2, received_date="2026-01-10", status="done"), row(id=3, received_date="2026-02-01")]
    result = monthly(rows, 2026)
    assert result[0]["отримано"] == 2
    assert result[0]["виконано"] == 1
    assert result[1]["отримано"] == 1


def test_distribution():
    result = distribution([row(category="А"), row(category="А"), row(category="Б")], "category")
    assert result["А"] == 2
    assert result["Б"] == 1


def test_storage_blocks_escape(tmp_path):
    storage = LocalStorage(AppPaths.from_root(tmp_path))
    try:
        storage.safe("../secret.txt")
    except StorageError:
        pass
    else:
        raise AssertionError("Path traversal was not blocked")


def test_database_migration_and_order_service(tmp_path):
    paths = AppPaths.from_root(tmp_path)
    db = Database(paths.database)
    storage = LocalStorage(paths)
    service = OrderService(db, storage)
    order_id = service.create(number="T-001", received=date.today(), deadline=date.today(), description="Тестове розпорядження", file_name="test.txt", file_bytes=b"test", priority="Важливий")
    order = db.get_order(order_id)
    assert order is not None
    assert order["number"] == "T-001"
    assert (paths.orders / order["folder"] / order["filename"]).exists()
