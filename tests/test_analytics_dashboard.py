from datetime import date

from core.analytics import distribution, metrics, monthly


def test_monthly_and_metrics_are_calculated_from_order_dates():
    rows = [
        {"id": 1, "received_date": "2026-01-05", "deadline": "2026-01-20", "status": "done", "priority": "Звичайний", "category": "Навчання", "responsible": "А"},
        {"id": 2, "received_date": "2026-01-08", "deadline": "2026-01-25", "status": "progress", "priority": "Терміновий", "category": "Навчання", "responsible": "Б"},
        {"id": 3, "received_date": "2026-02-02", "deadline": "2026-02-05", "status": "progress", "priority": "Критичний", "category": "Матеріальне", "responsible": "Б"},
    ]
    data = monthly(rows, 2026)
    assert data[0]["отримано"] == 2
    assert data[0]["виконано"] == 1
    assert data[1]["отримано"] == 1
    assert distribution(rows, "category")["Навчання"] == 2
    m = metrics(rows, date(2026, 1, 15))
    assert m.total == 3
    assert m.completed == 1
    assert m.active == 2


def test_selected_workspace_is_the_root_of_all_paths(tmp_path):
    from core.config import AppPaths

    paths = AppPaths.from_root(tmp_path)
    paths.ensure()
    assert paths.root == tmp_path.resolve()
    assert paths.orders.parent == paths.root
    assert paths.database.parent == paths.root
    assert paths.backups.parent == paths.root
    assert paths.trash.parent == paths.root
    assert paths.exports.parent == paths.root
