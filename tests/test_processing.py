import pytest

from src.processing import (
    filter_by_currency_code,
    filter_by_state,
    process_bank_operations,
    process_bank_search,
    sort_by_date,
)


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
    assert [item["id"] for item in result] == [2, 1, 3]


class TestNewProcessingFunctions:
    """Тесты для новых функций обработки."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями."""
        return [
            {
                "id": 1,
                "description": "Перевод организации",
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {"code": "RUB", "name": "руб."}
                }
            },
            {
                "id": 2,
                "description": "Покупка в магазине",
                "operationAmount": {
                    "amount": "50.0",
                    "currency": {"code": "USD", "name": "USD"}
                }
            },
            {
                "id": 3,
                "description": "Перевод со счета на счет",
                "operationAmount": {
                    "amount": "200.0",
                    "currency": {"code": "RUB", "name": "руб."}
                }
            },
            {
                "id": 4,
                "description": "Оплата услуг",
                "operationAmount": {
                    "amount": "75.0",
                    "currency": {"code": "EUR", "name": "EUR"}
                }
            }
        ]

    def test_process_bank_search_basic(self, sample_transactions):
        """Тестируем базовый поиск по описанию."""
        result = process_bank_search(sample_transactions, "Перевод")
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_process_bank_search_case_insensitive(self, sample_transactions):
        """Тестируем поиск без учета регистра."""
        result = process_bank_search(sample_transactions, "пЕрЕвОд")
        assert len(result) == 2

    def test_process_bank_search_no_matches(self, sample_transactions):
        """Тестируем поиск без совпадений."""
        result = process_bank_search(sample_transactions, "НесуществующееОписание")
        assert len(result) == 0

    def test_process_bank_search_empty_input(self, sample_transactions):
        """Тестируем поиск с пустыми входными данными."""
        result = process_bank_search([], "Перевод")
        assert len(result) == 0

        result = process_bank_search(sample_transactions, "")
        assert len(result) == 0

    def test_process_bank_operations_basic(self, sample_transactions):
        """Тестируем подсчет операций по категориям."""
        categories = ["Перевод", "Покупка", "Оплата"]
        result = process_bank_operations(sample_transactions, categories)

        assert result["Перевод"] == 2
        assert result["Покупка"] == 1
        assert result["Оплата"] == 1

    def test_process_bank_operations_case_insensitive(self, sample_transactions):
        """Тестируем подсчет операций без учета регистра."""
        categories = ["перевод", "покупка"]
        result = process_bank_operations(sample_transactions, categories)

        assert result["перевод"] == 2
        assert result["покупка"] == 1

    def test_process_bank_operations_no_matches(self, sample_transactions):
        """Тестируем подсчет операций без совпадений."""
        categories = ["НесуществующаяКатегория"]
        result = process_bank_operations(sample_transactions, categories)

        assert result["НесуществующаяКатегория"] == 0

    def test_process_bank_operations_empty_input(self, sample_transactions):
        """Тестируем подсчет операций с пустыми входными данными."""
        result = process_bank_operations([], ["Перевод"])
        assert result == {}

        result = process_bank_operations(sample_transactions, [])
        assert result == {}

    def test_filter_by_currency_code_rub(self, sample_transactions):
        """Тестируем фильтрацию по рублевым транзакциям."""
        result = filter_by_currency_code(sample_transactions, "RUB")
        assert len(result) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)

    def test_filter_by_currency_code_usd(self, sample_transactions):
        """Тестируем фильтрацию по долларовым транзакциям."""
        result = filter_by_currency_code(sample_transactions, "USD")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_by_currency_code_empty_result(self, sample_transactions):
        """Тестируем фильтрацию по несуществующей валюте."""
        result = filter_by_currency_code(sample_transactions, "JPY")
        assert len(result) == 0

    def test_filter_by_currency_code_default(self, sample_transactions):
        """Тестируем фильтрацию с валютой по умолчанию (RUB)."""
        result = filter_by_currency_code(sample_transactions)
        assert len(result) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)
