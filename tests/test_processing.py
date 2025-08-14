import pytest
from datetime import datetime
from src.processing import filter_by_state, sort_by_date

# Фикстура для тестовых данных
@pytest.fixture
def sample_data():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-15T12:00:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2023-01-10T08:30:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-20T18:45:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2023-01-05T10:15:00.000000"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-25T09:00:00.000000"},
    ]

# Параметризация для тестов фильтрации
@pytest.mark.parametrize("state,expected_ids", [
    ("EXECUTED", [1, 3, 5]),
    ("CANCELED", [2]),
    ("PENDING", [4]),
    ("UNKNOWN", []),  # Несуществующий статус
    ("", []),  # Пустой статус
])
def test_filter_by_state(sample_data, state, expected_ids):
    result = filter_by_state(sample_data, state)
    assert [item["id"] for item in result] == expected_ids

# Параметризация для тестов сортировки
@pytest.mark.parametrize("reverse,expected_ids", [
    (True, [5, 3, 1, 2, 4]),  # По убыванию (новые сначала)
    (False, [4, 2, 1, 3, 5]),  # По возрастанию (старые сначала)
])
def test_sort_by_date(sample_data, reverse, expected_ids):
    result = sort_by_date(sample_data, reverse)
    assert [item["id"] for item in result] == expected_ids

# Тест на обработку одинаковых дат
def test_sort_by_date_same_dates():
    data = [
        {"id": 1, "date": "2023-01-15T12:00:00.000000"},
        {"id": 2, "date": "2023-01-15T12:00:00.000000"},
        {"id": 3, "date": "2023-01-15T12:00:00.000000"},
    ]
    result = sort_by_date(data)
    # Проверяем что все элементы остаются в исходном порядке (стабильность сортировки)
    assert [item["id"] for item in result] == [1, 2, 3]

# Тест на некорректные форматы дат
def test_sort_by_date_invalid_formats():
    data = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "invalid-date"},
        {"id": 3, "date": "15-01-2023"},
    ]
    result = sort_by_date(data)
    # Ожидаем что функция не упадет и вернет данные в исходном порядке
    assert [item["id"] for item in result] == [1, 2, 3]