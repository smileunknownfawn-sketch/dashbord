from datetime import date, timedelta
from pathlib import Path

from core.analytics import metrics, monthly, distribution
from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.search_service import search_rows
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
        "filename": "test.pdf",
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


def test_attachments_and_response_attachments(tmp_path):
    paths = AppPaths.from_root(tmp_path)
    db = Database(paths.database)
    storage = LocalStorage(paths)
    service = OrderService(db, storage)
    order_id = service.create(number="ATT-001", received=date.today(), deadline=date.today(), description="Розпорядження з додатками", file_name="main.pdf", file_bytes=b"main")
    order = db.get_order(order_id)
    source = tmp_path / "Додаток 1.xlsx"
    source.write_bytes(b"attachment")
    attachment_id = service.add_attachment(order_id, source)
    assert attachment_id > 0
    assert len(db.get_attachments(order_id)) == 1
    response_file = tmp_path / "response.pdf"
    response_file.write_bytes(b"response")
    response_id = service.add_response(order, response_date=date.today(), outgoing="В-001", comment="Відповідь", file_name=response_file.name, file_bytes=response_file.read_bytes(), final=False)
    response_attachment = tmp_path / "Додаток до відповіді.xlsx"
    response_attachment.write_bytes(b"response attachment")
    service.add_response_attachment(order_id, response_id, response_attachment)
    assert len(db.get_attachments(order_id, response_id)) == 1


def test_search_by_number_words_and_filename():
    rows = [
        row(id=1, number="1234", description="Підготовка майна", responsible="Петро", filename="майно.xlsx"),
        row(id=2, number="5678", description="Навчання особового складу", responsible="Іван", filename="заняття.pdf"),
    ]
    assert [r.row["number"] for r in search_rows(rows, "1234")] == ["1234"]
    assert [r.row["number"] for r in search_rows(rows, "майна")] == ["1234"]
    assert [r.row["number"] for r in search_rows(rows, "майно")] == ["1234"]
    assert [r.row["number"] for r in search_rows(rows, "Петро")] == ["1234"]
    assert [r.row["number"] for r in search_rows(rows, "заняття")] == ["5678"]


def test_100_orders_stability(tmp_path):
    paths = AppPaths.from_root(tmp_path)
    db = Database(paths.database)
    storage = LocalStorage(paths)
    service = OrderService(db, storage)
    for i in range(1, 101):
        service.create(number=f"T-{i:04d}", received=date.today(), deadline=date.today(), description=f"Тестове розпорядження {i}", file_name=f"doc_{i}.txt", file_bytes=f"{i}".encode())
    rows = db.get_orders()
    assert len(rows) == 100
    assert len(search_rows([dict(r) for r in rows], "Тестове розпорядження 050")) == 1
    assert db.get_order(rows[-1]["id"]) is not None
