from datetime import date

from services.calendar_service import DeadlineItem, deadline_label, deadline_state, days_left, month_days, upcoming, overdue
from services.notification_service import build_notifications, counts
from services.report_service import summarize, by_month, completion_by_month


def test_deadline_calculations():
    today = date(2026, 9, 25)
    assert days_left("2026-09-25", today) == 0
    assert deadline_label("2026-09-25", today) == "Термін сьогодні"
    assert deadline_state("2026-09-24") == "overdue"
    assert deadline_state("2026-09-26") == "soon"


def test_calendar_month():
    assert len(month_days(2026, 2)) == 28
    assert month_days(2024, 2)[-1].day == 29


def test_upcoming_and_overdue():
    today = date(2026, 9, 25)
    items = [
        DeadlineItem(1, "1", date(2026, 9, 24), "У РОБОТІ", "Критичний"),
        DeadlineItem(2, "2", date(2026, 9, 26), "У РОБОТІ", "Важливий"),
        DeadlineItem(3, "3", date(2026, 10, 20), "У РОБОТІ", "Звичайний"),
    ]
    assert [x.order_id for x in overdue(items, today)] == [1]
    assert [x.order_id for x in upcoming(items, 7, today)] == [2]


def test_notifications():
    today = date(2026, 9, 25)
    items = [
        DeadlineItem(1, "1", date(2026, 9, 24), "У РОБОТІ", "Критичний"),
        DeadlineItem(2, "2", today, "У РОБОТІ", "Важливий"),
        DeadlineItem(3, "3", date(2026, 9, 27), "У РОБОТІ", "Звичайний"),
        DeadlineItem(4, "4", today, "ВИКОНАНО", "Критичний"),
    ]
    notes = build_notifications(items, today)
    assert counts(notes) == {"critical": 1, "warning": 1, "info": 1}
    assert all(n.order_id != 4 for n in notes)


def test_report_summary():
    rows = [
        {"status": "ВИКОНАНО", "due_date": "2026-09-20"},
        {"status": "У РОБОТІ", "due_date": "2026-09-24"},
        {"status": "У РОБОТІ", "due_date": "2026-09-25"},
        {"status": "У РОБОТІ", "due_date": "2026-09-28"},
    ]
    result = summarize(rows, date(2026, 9, 25))
    assert result.total == 4
    assert result.completed == 1
    assert result.active == 3
    assert result.overdue == 1
    assert result.due_today == 1
    assert result.completion_rate == 25.0


def test_report_grouping():
    rows = [
        {"received_date": "2026-01-10", "status": "ВИКОНАНО"},
        {"received_date": "2026-01-20", "status": "У РОБОТІ"},
        {"received_date": "2026-02-01", "status": "У РОБОТІ"},
    ]
    assert by_month(rows) == {"2026-01": 2, "2026-02": 1}
    grouped = completion_by_month(rows)
    assert grouped["2026-01"]["отримано"] == 2
    assert grouped["2026-01"]["виконано"] == 1
