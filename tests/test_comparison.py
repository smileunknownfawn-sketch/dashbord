from core.analytics import month_comparison, year_comparison


def test_year_and_month_comparison():
    rows = [
        {"received_date": "2025-01-10", "status": "progress"},
        {"received_date": "2025-01-20", "status": "done"},
        {"received_date": "2026-01-05", "status": "progress"},
        {"received_date": "2026-02-05", "status": "progress"},
    ]
    assert year_comparison(rows, 2025, 2026) == {"year_a": 2, "year_b": 2, "difference": 0}
    assert month_comparison(rows, 2025, 1, 2026, 2) == {"first": 2, "second": 1, "difference": -1}
