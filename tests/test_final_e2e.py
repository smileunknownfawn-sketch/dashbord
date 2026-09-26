from datetime import date, timedelta
from pathlib import Path

from core.config import AppPaths
from core.database import Database
from core.orders import OrderService
from core.storage import LocalStorage
from core.search_service import search_rows


def make_service(tmp_path: Path):
    paths = AppPaths.from_root(tmp_path)
    paths.ensure()
    db = Database(paths.database)
    storage = LocalStorage(paths)
    return paths, db, storage, OrderService(db, storage)


def test_full_order_lifecycle_with_attachments_and_response(tmp_path):
    paths, db, storage, service = make_service(tmp_path)
    source = tmp_path / "1111.pdf"
    source.write_bytes(b"order")
    attachment = tmp_path / "appendix.pdf"
    attachment.write_bytes(b"appendix")
    response = tmp_path / "response.pdf"
    response.write_bytes(b"response")
    response_attachment = tmp_path / "response_appendix.pdf"
    response_attachment.write_bytes(b"response appendix")

    oid = service.create(
        number="1111", received=date.today(), deadline=date.today() + timedelta(days=5),
        description="Тестове розпорядження", file_name=source.name,
        file_bytes=source.read_bytes(), responsible="Командир", category="Документація",
        tags="тест, важливе"
    )
    order = db.get_order(oid)
    assert (paths.orders / order["folder"] / source.name).exists()

    service.add_attachment(oid, attachment)
    assert (paths.orders / order["folder"] / "Додатки" / attachment.name).exists()

    rid = service.add_response(order, response_date=date.today(), outgoing="В-01", comment="Виконано", file_name=response.name, file_bytes=response.read_bytes(), final=True)
    response_row = [r for r in db.get_responses(oid) if int(r["id"]) == rid][0]
    service.add_response_attachment(oid, rid, response_attachment)
    response_dir = paths.root / Path(response_row["path"]).parent
    assert (response_dir / response_attachment.name).exists()
    assert (response_dir / "Додатки" / response_attachment.name).exists()
    assert service.status(db.get_order(oid)) == "done"

    results = search_rows([dict(db.get_order(oid))], "важливе")
    assert results and results[0].row["number"] == "1111"

    service.move_to_trash(db.get_order(oid))
    assert not (paths.orders / order["folder"]).exists()
    service.restore(oid)
    assert (paths.orders / order["folder"]).exists()
    service.move_to_trash(db.get_order(oid))
    service.purge(oid)
    assert db.get_order(oid, include_deleted=True) is None


def test_all_required_config_is_ukrainian_and_versioned():
    from core.config import APP_VERSION, DEVELOPER
    assert APP_VERSION == "1.0.1"
    assert DEVELOPER == "В.О.М."
