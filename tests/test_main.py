import pytest
from unittest.mock import patch, MagicMock, call
import sys
import os
from io import StringIO

# Добавляем путь к src для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import BankTransactionProcessor, main


class TestBankTransactionProcessor:
    """Тесты для основного класса обработки транзакций."""

    @pytest.fixture
    def processor(self):
        return BankTransactionProcessor()

    @pytest.fixture
    def sample_transactions(self):
        return [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00",
                "operationAmount": {
                    "amount": "100.0",
                    "currency": {"code": "RUB", "name": "руб."}
                },
                "description": "Перевод организации",
                "from": "Счет 1234567890123456",
                "to": "Счет 9876543210987654"
            },
            {
                "id": 2,
                "state": "CANCELED",
                "date": "2023-01-02T14:30:00",
                "operationAmount": {
                    "amount": "50.0",
                    "currency": {"code": "USD", "name": "USD"}
                },
                "description": "Покупка в магазине",
                "from": "Visa 1234 5678 9012 3456",
                "to": "Магазин ABC"
            }
        ]

    def test_initialization(self, processor):
        """Тестируем инициализацию процессора."""
        assert processor.transactions == []
        assert processor.filtered_transactions == []

    @patch('src.main.load_json_data')
    def test_load_transactions_from_json_success(self, mock_load, processor):
        """Тестируем успешную загрузку из JSON."""
        mock_load.return_value = [{"id": 1}]
        result = processor.load_transactions_from_json("test.json")
        assert result is True
        assert processor.transactions == [{"id": 1}]

    @patch('src.main.load_json_data')
    def test_load_transactions_from_json_failure(self, mock_load, processor):
        """Тестируем неудачную загрузку из JSON."""
        mock_load.return_value = []
        result = processor.load_transactions_from_json("test.json")
        assert result is False
        assert processor.transactions == []

    @patch('src.main.read_csv_file')
    @patch('src.main.convert_transaction_format')
    def test_load_transactions_from_csv_success(self, mock_convert, mock_read, processor):
        """Тестируем успешную загрузку из CSV."""
        mock_read.return_value = [{"id": 1}]
        mock_convert.return_value = [{"id": 1, "converted": True}]
        result = processor.load_transactions_from_csv("test.csv")
        assert result is True
        assert processor.transactions == [{"id": 1, "converted": True}]

    @patch('src.main.read_excel_file')
    @patch('src.main.convert_transaction_format')
    def test_load_transactions_from_excel_success(self, mock_convert, mock_read, processor):
        """Тестируем успешную загрузку из Excel."""
        mock_read.return_value = [{"id": 1}]
        mock_convert.return_value = [{"id": 1, "converted": True}]
        result = processor.load_transactions_from_excel("test.xlsx")
        assert result is True
        assert processor.transactions == [{"id": 1, "converted": True}]

    @patch('builtins.input')
    def test_filter_by_status_valid(self, mock_input, processor, sample_transactions):
        """Тестируем фильтрацию по валидному статусу."""
        mock_input.return_value = "EXECUTED"
        processor.transactions = sample_transactions
        result = processor.filter_by_status()
        assert result is True
        assert len(processor.filtered_transactions) == 1
        assert processor.filtered_transactions[0]["state"] == "EXECUTED"

    @patch('builtins.input')
    def test_filter_by_status_invalid_then_valid(self, mock_input, processor, sample_transactions):
        """Тестируем фильтрацию с невалидным, затем валидным статусом."""
        mock_input.side_effect = ["INVALID", "EXECUTED"]
        processor.transactions = sample_transactions
        result = processor.filter_by_status()
        assert result is True
        assert len(processor.filtered_transactions) == 1

    @patch('builtins.input')
    def test_ask_yes_no_question_yes_variants(self, mock_input, processor):
        """Тестируем варианты ответа 'Да'."""
        for yes_variant in ["да", "д", "yes", "y"]:
            mock_input.return_value = yes_variant
            result = processor.ask_yes_no_question("Test?")
            assert result is True

    @patch('builtins.input')
    def test_ask_yes_no_question_no_variants(self, mock_input, processor):
        """Тестируем варианты ответа 'Нет'."""
        for no_variant in ["нет", "н", "no", "n"]:
            mock_input.return_value = no_variant
            result = processor.ask_yes_no_question("Test?")
            assert result is False

    @patch('builtins.input')
    def test_ask_yes_no_question_invalid_then_valid(self, mock_input, processor):
        """Тестируем невалидный, затем валидный ответ."""
        mock_input.side_effect = ["maybe", "да"]
        result = processor.ask_yes_no_question("Test?")
        assert result is True

    @patch('builtins.input')
    def test_ask_sort_direction_ascending(self, mock_input, processor):
        """Тестируем выбор сортировки по возрастанию."""
        for asc_variant in ["по возрастанию", "возрастание", "asc", "ascending"]:
            mock_input.return_value = asc_variant
            result = processor.ask_sort_direction()
            assert result is False

    @patch('builtins.input')
    def test_ask_sort_direction_descending(self, mock_input, processor):
        """Тестируем выбор сортировки по убыванию."""
        for desc_variant in ["по убыванию", "убывание", "desc", "descending"]:
            mock_input.return_value = desc_variant
            result = processor.ask_sort_direction()
            assert result is True

    def test_format_transaction_full_data(self, processor):
        """Тестируем форматирование транзакции с полными данными."""
        transaction = {
            "date": "2023-01-01T12:00:00",
            "description": "Перевод организации",
            "from": "Счет 1234567890123456",
            "to": "Счет 9876543210987654",
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "RUB", "name": "руб."}
            }
        }
        result = processor.format_transaction(transaction)
        assert "01.01.2023" in result
        assert "Перевод организации" in result
        assert "Счет **3456" in result
        assert "Счет **7654" in result
        assert "100.0 руб. (RUB)" in result

    def test_format_transaction_missing_fields(self, processor):
        """Тестируем форматирование транзакции с отсутствующими полями."""
        transaction = {
            "date": "2023-01-01T12:00:00",
            "description": "Перевод",
            "operationAmount": {
                "amount": "100.0",
                "currency": {"code": "USD"}
            }
        }
        result = processor.format_transaction(transaction)
        assert "01.01.2023" in result
        assert "Перевод" in result
        assert "100.0 USD" in result

    @patch('builtins.print')
    def test_print_transactions_empty(self, mock_print, processor):
        """Тестируем вывод пустого списка транзакций."""
        processor.filtered_transactions = []
        processor.print_transactions()
        mock_print.assert_called_with("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    @patch('builtins.print')
    def test_print_transactions_with_data(self, mock_print, processor, sample_transactions):
        """Тестируем вывод списка транзакций."""
        processor.filtered_transactions = sample_transactions
        processor.print_transactions()
        assert mock_print.called

    @patch('src.main.BankTransactionProcessor')
    def test_main_function(self, mock_processor):
        """Тестируем основную функцию."""
        mock_instance = mock_processor.return_value
        with patch('builtins.print'):
            main()
            mock_instance.run.assert_called_once()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_method_file_selection(self, mock_print, mock_input, processor):
        """Тестируем выбор файла в методе run."""
        mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "нет"]

        with patch('src.main.load_json_data') as mock_load:
            mock_load.return_value = [{"id": 1}]
            processor.run()

            assert mock_print.called
            assert "Для обработки выбран JSON-файл" in str(mock_print.call_args_list)


class TestIntegration:
    """Интеграционные тесты."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_full_workflow(self, mock_print, mock_input):
        """Тестируем полный рабочий процесс."""
        mock_input.side_effect = [
            "1",  # Выбор JSON
            "EXECUTED",  # Статус
            "нет",  # Сортировка по дате? Нет
            "нет",  # Только рублевые? Нет
            "нет"  # Фильтр по слову? Нет
        ]

        processor = BankTransactionProcessor()

        with patch('src.main.load_json_data') as mock_load:
            mock_load.return_value = [
                {
                    "id": 1,
                    "state": "EXECUTED",
                    "date": "2023-01-01T12:00:00",
                    "operationAmount": {
                        "amount": "100.0",
                        "currency": {"code": "RUB", "name": "руб."}
                    },
                    "description": "Перевод",
                    "from": "Счет 1234",
                    "to": "Счет 5678"
                }
            ]

            processor.run()

            # Проверяем, что транзакции были загружены и обработаны
            assert len(processor.transactions) == 1
            assert len(processor.filtered_transactions) == 1
