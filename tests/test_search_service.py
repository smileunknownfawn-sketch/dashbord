from core.search_service import search_rows, tokenize


def rows():
    return [
        {"number": "1111", "description": "Постачання майна підрозділу", "responsible": "Коваленко", "category": "Матеріальне", "priority": "Важливий", "tags": "майно склад"},
        {"number": "2210", "description": "Організація навчання", "responsible": "Петренко", "category": "Навчання", "priority": "Звичайний", "tags": "підготовка"},
        {"number": "3315", "description": "Ремонт автомобільної техніки", "responsible": "Коваленко", "category": "Матеріальне", "priority": "Терміновий", "tags": "ремонт техніка"},
    ]


def test_tokenize_ignores_short_stop_words():
    assert tokenize("про майно і склад") == ["майно", "склад"]


def test_search_by_description_word():
    result = search_rows(rows(), "майно")
    assert result[0].row["number"] == "1111"


def test_search_by_partial_word():
    result = search_rows(rows(), "автомоб")
    assert result[0].row["number"] == "3315"


def test_search_multiple_words_requires_all_words():
    result = search_rows(rows(), "майно склад")
    assert [item.row["number"] for item in result] == ["1111"]


def test_search_by_responsible():
    result = search_rows(rows(), "Коваленко")
    assert {item.row["number"] for item in result} == {"1111", "3315"}


def test_search_by_tag():
    result = search_rows(rows(), "підготовка")
    assert result[0].row["number"] == "2210"


def test_exact_number_has_priority():
    result = search_rows(rows(), "1111")
    assert result[0].row["number"] == "1111"
    assert result[0].score >= 250
