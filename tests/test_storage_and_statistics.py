from datetime import date
from pathlib import Path

from services.storage_service import inside, safe_child
from services.statistics_service import status_counts, workload_by_category, workload_by_responsible, completion_rate


def test_inside_rejects_escape(tmp_path: Path):
    assert inside(tmp_path, tmp_path / "orders" / "111")
    assert not inside(tmp_path, tmp_path.parent / "outside")


def test_safe_child_sanitizes_name(tmp_path: Path):
    root = tmp_path / "orders"
    root.mkdir()
    result = safe_child(root, "1111/../../evil")
    assert result.parent == root
    assert ".." not in result.name


def test_status_counts_uses_deadline():
    rows = [
        {"status": "done", "deadline": "2026-09-01"},
        {"status": "progress", "deadline": "2026-09-20"},
        {"status": "progress", "deadline": date.today().isoformat()},
    ]
    result = status_counts(rows)
    assert result["виконано"] == 1
    assert sum(result.values()) == 3


def test_workload_groups_values():
    rows = [{"responsible": "Іваненко", "category": "Навчання"}, {"responsible": "Іваненко", "category": "Інше"}]
    assert workload_by_responsible(rows)["Іваненко"] == 2
    assert workload_by_category(rows)["Навчання"] == 1


def test_completion_rate():
    rows = [{"status": "done"}, {"status": "progress"}, {"status": "виконано"}, {"status": "progress"}]
    assert completion_rate(rows) == 50.0
