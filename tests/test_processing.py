import pytest
from src.processing import (
    count_transactions_by_type,
    count_transactions_by_status,
    count_transactions_by_currency,
    filter_by_state,
    sort_by_date,
    process_bank_search,
    process_bank_operations,
    filter_by_currency_code,
)


class TestTransactionCounting:
    """Тесты для функций подсчета транзакций."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с примером транзакций."""
        return [
            {
                "id": 1,
                "state": "EXECUTED",
                "description": "Перевод организации",
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {"code": "RUB", "name": "руб."}
                }
            },
            {
                "id": 2,
                "state": "EXECUTED",
                "description": "Перевод организации",
                "operationAmount": {
                    "amount": "50.0",
                    "currency": {"code": "USD", "name": "USD"}
                }
            },
            {
                "id": 3,
                "state": "CANCELED",
                "description": "Покупка в магазине",
                "operationAmount": {
                    "amount": "200.0",
                    "currency": {"code": "RUB", "name": "руб."}
                }
            },
            {
                "id": 4,
                "state": "EXECUTED",
                "description": "Покупка в магазине",
                "operationAmount": {
                    "amount": "300.0",
                    "currency": {"code": "EUR", "name": "EUR"}
                }
            }
        ]

    def test_count_transactions_by_type_description(self, sample_transactions):
        """Тестируем подсчет по описанию операций."""
        result = count_transactions_by_type(sample_transactions, "description")

        expected = {
            "Перевод организации": 2,
            "Покупка в магазине": 2
        }
        assert result == expected

    def test_count_transactions_by_type_state(self, sample_transactions):
        """Тестируем подсчет по статусу операций."""
        result = count_transactions_by_type(sample_transactions, "state")

        expected = {
            "EXECUTED": 3,
            "CANCELED": 1
        }
        assert result == expected

    def test_count_transactions_by_status(self, sample_transactions):
        """Тестируем специализированную функцию подсчета по статусу."""
        result = count_transactions_by_status(sample_transactions)

        expected = {
            "EXECUTED": 3,
            "CANCELED": 1
        }
        assert result == expected

    def test_count_transactions_by_currency(self, sample_transactions):
        """Тестируем подсчет по валюте операций."""
        result = count_transactions_by_currency(sample_transactions)

        expected = {
            "RUB": 2,
            "USD": 1,
            "EUR": 1
        }
        assert result == expected

    def test_count_transactions_empty_list(self):
        """Тестируем подсчет для пустого списка транзакций."""
        result = count_transactions_by_type([])
        assert result == {}

    def test_count_transactions_missing_field(self, sample_transactions):
        """Тестируем подсчет по отсутствующему полю."""
        result = count_transactions_by_type(sample_transactions, "nonexistent_field")
        assert result == {}

    def test_count_transactions_with_none_values(self):
        """Тестируем подсчет транзакций с None значениями."""
        transactions = [
            {"description": "Type A"},
            {"description": None},
            {"description": "Type A"},
            {"description": "Type B"},
            {}  # Транзакция без поля description
        ]

        result = count_transactions_by_type(transactions, "description")

        expected = {
            "Type A": 2,
            "Type B": 1
        }
        assert result == expected


def test_counter_advanced_features():
    """Тестируем расширенные возможности Counter."""
    from collections import Counter

    # Создаем Counter напрямую для демонстрации
    transactions = ["Перевод", "Покупка", "Перевод", "Оплата", "Перевод"]
    counter = Counter(transactions)

    # Проверяем основные методы Counter
    assert dict(counter) == {"Перевод": 3, "Покупка": 1, "Оплата": 1}
    assert counter.most_common(1) == [("Перевод", 3)]
    assert counter["Перевод"] == 3
    assert counter["Несуществующий"] == 0  # Не вызывает KeyError


@pytest.mark.parametrize("field,expected", [
    ("description", {"Перевод": 2, "Покупка": 1}),
    ("state", {"EXECUTED": 2, "PENDING": 1}),
    ("amount", {100: 1, 200: 1, 300: 1}),
])
def test_count_transactions_parametrized(field, expected):
    """Параметризованный тест для разных полей группировки."""
    transactions = [
        {"description": "Перевод", "state": "EXECUTED", "amount": 100},
        {"description": "Перевод", "state": "EXECUTED", "amount": 200},
        {"description": "Покупка", "state": "PENDING", "amount": 300},
    ]

    result = count_transactions_by_type(transactions, field)
    assert result == expected


@pytest.mark.parametrize("state_value,expected_ids", [
    ("EXECUTED", [1, 2, 4]),
    ("CANCELED", [3]),
    ("PENDING", []),
    ("UNKNOWN", []),
    ("", []),
])
def test_filter_by_state(state_value, expected_ids):
    """Тестируем фильтрацию по статусу операций."""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "CANCELED"},
        {"id": 4, "state": "EXECUTED"},
    ]

    filtered = filter_by_state(transactions, state_value)
    assert [t["id"] for t in filtered] == expected_ids


def test_filter_by_state_default():
    """Тестируем фильтрацию по статусу со значением по умолчанию."""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELED"},
    ]

    filtered = filter_by_state(transactions)
    assert len(filtered) == 1
    assert filtered[0]["id"] == 1


def test_filter_by_state_missing_field():
    """Тестируем фильтрацию по статусу при отсутствии поля state."""
    transactions = [
        {"id": 1, "description": "Transaction 1"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "description": "Transaction 3"},
    ]

    filtered = filter_by_state(transactions, "EXECUTED")
    assert len(filtered) == 1
    assert filtered[0]["id"] == 2


@pytest.mark.parametrize("reverse,expected_ids", [
    (True, [3, 2, 1]),  # по убыванию
    (False, [1, 2, 3]),  # по возрастанию
])
def test_sort_by_date(reverse, expected_ids):
    """Тестируем сортировку по дате."""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-01-03"},
        {"id": 3, "date": "2023-01-05"},
    ]

    sorted_transactions = sort_by_date(transactions, reverse=reverse)
    assert [t["id"] for t in sorted_transactions] == expected_ids


def test_sort_by_date_same_dates():
    """Тестируем сортировку с одинаковыми датами (должна сохранять порядок)."""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-01-01"},
        {"id": 3, "date": "2023-01-01"},
    ]

    sorted_transactions = sort_by_date(transactions, reverse=False)
    # При одинаковых датах порядок должен сохраниться (стабильная сортировка)
    assert [t["id"] for t in sorted_transactions] == [1, 2, 3]


def test_sort_by_date_invalid_formats():
    """Тестируем сортировку с некорректными форматами дат."""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "invalid-date"},
        {"id": 3, "date": "2023-01-03"},
    ]

    # Сортировка должна работать, некорректные даты будут в конце (при reverse=False)
    sorted_transactions = sort_by_date(transactions, reverse=False)
    # Проверяем, что транзакция с некорректной датой оказалась в конце
    assert sorted_transactions[-1]["id"] == 2


def test_sort_by_date_missing_field():
    """Тестируем сортировку при отсутствии поля date."""
    transactions = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "description": "No date field"},
        {"id": 3, "date": "2023-01-03"},
    ]

    sorted_transactions = sort_by_date(transactions, reverse=False)
    # Транзакция без даты должна быть в начале (пустая строка)
    assert sorted_transactions[0]["id"] == 2


class TestNewProcessingFunctions:
    """Тесты для новых функций обработки."""

    @pytest.fixture
    def bank_data(self):
        """Фикстура с банковскими операциями."""
        return [
            {
                "id": 1,
                "description": "Перевод организации",
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {"code": "RUB"}
                }
            },
            {
                "id": 2,
                "description": "Покупка в магазине",
                "operationAmount": {
                    "amount": "50.0",
                    "currency": {"code": "USD"}
                }
            },
            {
                "id": 3,
                "description": "Перевод другу",
                "operationAmount": {
                    "amount": "200.0",
                    "currency": {"code": "RUB"}
                }
            },
            {
                "id": 4,
                "description": "Оплата услуг",
                "operationAmount": {
                    "amount": "300.0",
                    "currency": {"code": "EUR"}
                }
            }
        ]

    def test_process_bank_search_basic(self, bank_data):
        """Тестируем базовый поиск по описанию."""
        result = process_bank_search(bank_data, "Перевод")
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_process_bank_search_case_insensitive(self, bank_data):
        """Тестируем поиск без учета регистра."""
        result = process_bank_search(bank_data, "перевод")
        assert len(result) == 2

    def test_process_bank_search_no_matches(self, bank_data):
        """Тестируем поиск без совпадений."""
        result = process_bank_search(bank_data, "Кредит")
        assert len(result) == 0

    def test_process_bank_search_empty_input(self, bank_data):
        """Тестируем поиск с пустым запросом."""
        result = process_bank_search(bank_data, "")
        assert len(result) == 0

        result = process_bank_search([], "Перевод")
        assert len(result) == 0

    def test_process_bank_search_special_regex_chars(self, bank_data):
        """Тестируем поиск с специальными символами regex."""
        # Добавляем транзакцию с специальными символами
        special_transaction = {
            "id": 5,
            "description": "Payment [Special]",
            "operationAmount": {"amount": "400.0", "currency": {"code": "USD"}}
        }
        extended_data = bank_data + [special_transaction]

        result = process_bank_search(extended_data, "[Special]")
        assert len(result) == 1
        assert result[0]["id"] == 5

    def test_process_bank_operations_basic(self, bank_data):
        """Тестируем подсчет операций по категориям."""
        categories = ["Перевод", "Покупка", "Оплата"]
        result = process_bank_operations(bank_data, categories)

        expected = {
            "Перевод": 2,
            "Покупка": 1,
            "Оплата": 1
        }
        assert result == expected

    def test_process_bank_operations_case_insensitive(self, bank_data):
        """Тестируем подсчет операций без учета регистра."""
        categories = ["перевод", "покупка"]
        result = process_bank_operations(bank_data, categories)

        expected = {
            "перевод": 2,
            "покупка": 1
        }
        assert result == expected

    def test_process_bank_operations_no_matches(self, bank_data):
        """Тестируем подсчет операций без совпадений."""
        categories = ["Кредит", "Депозит"]
        result = process_bank_operations(bank_data, categories)

        expected = {
            "Кредит": 0,
            "Депозит": 0
        }
        assert result == expected

    def test_process_bank_operations_empty_input(self, bank_data):
        """Тестируем подсчет операций с пустыми входными данными."""
        result = process_bank_operations([], ["Перевод"])
        assert result == {}

        result = process_bank_operations(bank_data, [])
        assert result == {}

    def test_process_bank_operations_partial_matches(self, bank_data):
        """Тестируем подсчет операций с частичными совпадениями."""
        categories = ["орган", "магазин", "услуг"]
        result = process_bank_operations(bank_data, categories)

        expected = {
            "орган": 1,  # "Перевод организации"
            "магазин": 1,  # "Покупка в магазине"
            "услуг": 1  # "Оплата услуг"
        }
        assert result == expected

    def test_filter_by_currency_code_rub(self, bank_data):
        """Тестируем фильтрацию по рублевым операциям."""
        result = filter_by_currency_code(bank_data, "RUB")
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3

    def test_filter_by_currency_code_usd(self, bank_data):
        """Тестируем фильтрацию по долларовым операциям."""
        result = filter_by_currency_code(bank_data, "USD")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_filter_by_currency_code_empty_result(self, bank_data):
        """Тестируем фильтрацию по валюте без совпадений."""
        result = filter_by_currency_code(bank_data, "GBP")
        assert len(result) == 0

    def test_filter_by_currency_code_default(self, bank_data):
        """Тестируем фильтрацию по валюте со значением по умолчанию (RUB)."""
        result = filter_by_currency_code(bank_data)
        assert len(result) == 2
        assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)

    def test_filter_by_currency_code_invalid_structure(self):
        """Тестируем фильтрацию при некорректной структуре данных."""
        invalid_data = [
            {"id": 1, "operationAmount": "invalid"},
            {"id": 2, "operationAmount": {"currency": "invalid"}},
            {"id": 3, "operationAmount": {"currency": {"code": "RUB"}}},
        ]

        result = filter_by_currency_code(invalid_data, "RUB")
        assert len(result) == 1
        assert result[0]["id"] == 3


def test_edge_cases():
    """Тестируем крайние случаи для всех функций."""

    # Пустые данные
    assert count_transactions_by_type([]) == {}
    assert filter_by_state([]) == []
    assert sort_by_date([]) == []
    assert process_bank_search([], "test") == []
    assert process_bank_operations([], ["test"]) == {}
    assert filter_by_currency_code([]) == []

    # None значения
    assert count_transactions_by_type(None) == {}
    # Другие функции должны корректно обрабатывать None через проверки в коде
