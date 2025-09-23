import pytest
import pandas as pd
import logging
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.file_reader import read_csv_file, read_excel_file, convert_transaction_format, logger


class TestFileReader:
    """Тесты для модуля чтения файлов."""

    @pytest.fixture
    def sample_csv_data(self):
        """Фикстура с примером CSV данных."""
        return "id,state,date,amount,currency,description,from,to\n1,EXECUTED,2023-01-01,100.0,USD,Перевод,Счет 100,Счет 200"

    @pytest.fixture
    def sample_excel_data(self):
        """Фикстура с примером данных для Excel."""
        return pd.DataFrame({
            'id': [1, 2],
            'state': ['EXECUTED', 'CANCELED'],
            'date': ['2023-01-01', '2023-01-02'],
            'amount': [100.0, 200.0],
            'currency': ['USD', 'EUR'],
            'description': ['Перевод', 'Оплата'],
            'from': ['Счет 100', 'Счет 200'],
            'to': ['Счет 300', 'Счет 400']
        })

    # Тесты для read_csv_file
    def test_read_csv_file_success(self, sample_csv_data):
        """Тестируем успешное чтение CSV файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_csv') as mock_read_csv:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100

            mock_df = MagicMock()
            mock_df.to_dict.return_value = [
                {'id': 1, 'state': 'EXECUTED', 'amount': 100.0, 'currency': 'USD'}
            ]
            mock_read_csv.return_value = mock_df

            result = read_csv_file('test.csv')

            assert len(result) == 1
            assert result[0]['id'] == 1
            mock_read_csv.assert_called_once_with('test.csv')

    def test_read_csv_file_not_found(self):
        """Тестируем обработку отсутствующего CSV файла."""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            result = read_csv_file('nonexistent.csv')
            assert result == []

    def test_read_csv_file_is_directory(self):
        """Тестируем обработку случая, когда путь ведет к директории."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file:
            mock_exists.return_value = True
            mock_is_file.return_value = False

            result = read_csv_file('some_directory')
            assert result == []

    def test_read_csv_file_empty(self):
        """Тестируем обработку пустого CSV файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 0

            result = read_csv_file('empty.csv')
            assert result == []

    def test_read_csv_file_pandas_exception(self):
        """Тестируем обработку исключения при чтении CSV."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_csv') as mock_read_csv:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100
            mock_read_csv.side_effect = Exception("Read error")

            result = read_csv_file('error.csv')
            assert result == []

    def test_read_csv_file_unicode_error(self):
        """Тестируем обработку ошибки кодирования."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_csv') as mock_read_csv:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100
            mock_read_csv.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid byte")

            result = read_csv_file('encoding_error.csv')
            assert result == []

    # Тесты для read_excel_file
    def test_read_excel_file_success(self, sample_excel_data):
        """Тестируем успешное чтение Excel файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_excel') as mock_read_excel:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100

            mock_read_excel.return_value = sample_excel_data

            result = read_excel_file('test.xlsx')

            assert len(result) == 2
            assert result[0]['id'] == 1
            assert result[1]['id'] == 2
            mock_read_excel.assert_called_once_with('test.xlsx')

    def test_read_excel_file_not_found(self):
        """Тестируем обработку отсутствующего Excel файла."""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            result = read_excel_file('nonexistent.xlsx')
            assert result == []

    def test_read_excel_file_is_directory(self):
        """Тестируем обработку случая, когда путь ведет к директории."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file:
            mock_exists.return_value = True
            mock_is_file.return_value = False

            result = read_excel_file('some_directory')
            assert result == []

    def test_read_excel_file_empty(self):
        """Тестируем обработку пустого Excel файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 0

            result = read_excel_file('empty.xlsx')
            assert result == []

    def test_read_excel_file_pandas_exception(self):
        """Тестируем обработку исключения при чтении Excel."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_excel') as mock_read_excel:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100
            mock_read_excel.side_effect = Exception("Read error")

            result = read_excel_file('error.xlsx')
            assert result == []

    def test_read_excel_file_value_error(self):
        """Тестируем обработку ValueError при чтении Excel."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_excel') as mock_read_excel:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100
            mock_read_excel.side_effect = ValueError("Invalid file")

            result = read_excel_file('invalid.xlsx')
            assert result == []

    # Тесты для convert_transaction_format
    def test_convert_transaction_format_basic(self):
        """Тестируем конвертацию формата транзакций."""
        sample_transactions = [
            {
                'id': 1,
                'state': 'EXECUTED',
                'date': '2023-01-01',
                'amount': 100.0,
                'currency': 'USD',
                'description': 'Перевод',
                'from': 'Счет 100',
                'to': 'Счет 200'
            }
        ]

        result = convert_transaction_format(sample_transactions)

        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['state'] == 'EXECUTED'
        assert result[0]['operationAmount']['amount'] == '100.0'
        assert result[0]['operationAmount']['currency']['code'] == 'USD'

    def test_convert_transaction_format_missing_fields(self):
        """Тестируем конвертацию с отсутствующими полями."""
        sample_transactions = [{'id': 1}]  # Минимальные данные

        result = convert_transaction_format(sample_transactions)

        assert len(result) == 1
        assert result[0]['id'] == 1
        assert result[0]['state'] == 'UNKNOWN'
        assert result[0]['operationAmount']['amount'] == ''

    def test_convert_transaction_format_with_operation_amount(self):
        """Тестируем конвертацию, когда уже есть operationAmount."""
        sample_transactions = [
            {
                'id': 1,
                'operationAmount': {
                    'amount': 200.0,
                    'currency': {
                        'name': 'USD',
                        'code': 'USD'
                    }
                }
            }
        ]

        result = convert_transaction_format(sample_transactions)

        assert result[0]['operationAmount']['amount'] == '200.0'
        assert result[0]['operationAmount']['currency']['code'] == 'USD'

    def test_convert_transaction_format_alternative_currency_fields(self):
        """Тестируем конвертацию с альтернативными названиями полей валюты."""
        sample_transactions = [
            {
                'id': 1,
                'currency_name': 'Доллары',
                'currency_code': 'USD',
                'amount': 100.0
            }
        ]

        result = convert_transaction_format(sample_transactions)

        assert result[0]['operationAmount']['currency']['name'] == 'Доллары'
        assert result[0]['operationAmount']['currency']['code'] == 'USD'

    def test_convert_transaction_format_empty_list(self):
        """Тестируем конвертацию пустого списка."""
        result = convert_transaction_format([])
        assert result == []

    def test_convert_transaction_format_exception_handling(self):
        """Тестируем обработку исключений при конвертации."""
        # Транзакция с некорректными данными, которые вызовут исключение
        sample_transactions = [{'amount': object()}]  # Несериализуемый объект

        result = convert_transaction_format(sample_transactions)
        # Функция должна обработать исключение и пропустить проблемную транзакцию
        assert len(result) == 0

    # Тесты для логирования
    def test_logger_initialization(self):
        """Тестируем инициализацию логгера."""
        assert logger.name == "file_reader"
        assert logger.level == logging.DEBUG
        assert len(logger.handlers) > 0

    def test_csv_file_logging(self, caplog):
        """Тестируем логирование при работе с CSV файлами."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_csv') as mock_read_csv:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100

            mock_df = MagicMock()
            mock_df.to_dict.return_value = [{'id': 1}]
            mock_read_csv.return_value = mock_df

            with caplog.at_level(logging.INFO):
                read_csv_file('test.csv')
                assert "Успешно загружено 1 транзакций из CSV: test.csv" in caplog.text

    def test_excel_file_error_logging(self, caplog):
        """Тестируем логирование ошибок при работе с Excel файлами."""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False

            with caplog.at_level(logging.ERROR):
                read_excel_file('nonexistent.xlsx')
                assert "Excel файл не найден: nonexistent.xlsx" in caplog.text

    # Параметризованные тесты
    @pytest.mark.parametrize("file_path,expected", [
        ('transactions.csv', True),
        ('data/transactions.csv', True),
        ('transactions.xlsx', True),
        ('', False),
        (None, False)
    ])
    def test_file_paths(self, file_path, expected):
        """Параметризованный тест для различных путей файлов."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_csv') as mock_read_csv, \
                patch('pandas.read_excel') as mock_read_excel:

            mock_exists.return_value = expected
            mock_is_file.return_value = expected
            mock_stat.return_value.st_size = 100 if expected else 0

            mock_df = MagicMock()
            mock_df.to_dict.return_value = []

            if file_path and file_path.endswith('.csv'):
                mock_read_csv.return_value = mock_df
                result = read_csv_file(file_path)
                if expected:
                    assert result == []
                    mock_read_csv.assert_called_once_with(file_path)
                else:
                    assert result == []
            elif file_path and file_path.endswith('.xlsx'):
                mock_read_excel.return_value = mock_df
                result = read_excel_file(file_path)
                if expected:
                    assert result == []
                    mock_read_excel.assert_called_once_with(file_path)
                else:
                    assert result == []
            else:
                result = read_csv_file(file_path)
                assert result == []

    # Тесты для граничных случаев
    def test_read_csv_file_large_file(self):
        """Тестируем обработку большого CSV файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_csv') as mock_read_csv:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 1024 * 1024  # 1MB

            # Создаем mock для большого DataFrame
            mock_df = MagicMock()
            mock_df.to_dict.return_value = [{'id': i} for i in range(1000)]  # 1000 записей
            mock_read_csv.return_value = mock_df

            result = read_csv_file('large.csv')
            assert len(result) == 1000

    def test_read_excel_file_multiple_sheets(self):
        """Тестируем чтение Excel файла с несколькими листами."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_excel') as mock_read_excel:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100

            # Мокаем DataFrame
            mock_df = MagicMock()
            mock_df.to_dict.return_value = [{'id': 1, 'sheet': 'first'}]
            mock_read_excel.return_value = mock_df

            result = read_excel_file('multisheet.xlsx')
            assert len(result) == 1

    def test_convert_transaction_format_special_characters(self):
        """Тестируем конвертацию транзакций со специальными символами."""
        sample_transactions = [
            {
                'id': 1,
                'description': 'Перевод счёта №123/456',
                'from': 'Visa Classic 1234-5678-9012-3456',
                'to': 'Счет **7890',
                'amount': '1000.50'
            }
        ]

        result = convert_transaction_format(sample_transactions)

        assert result[0]['description'] == 'Перевод счёта №123/456'
        assert result[0]['from'] == 'Visa Classic 1234-5678-9012-3456'
        assert result[0]['operationAmount']['amount'] == '1000.50'


# Дополнительные тесты для повышения покрытия
def test_module_level_code_execution():
    """Тестируем выполнение кода на уровне модуля (инициализацию логгера)."""
    # Импортируем модуль заново, чтобы выполнить код инициализации
    import importlib
    import src.file_reader
    importlib.reload(src.file_reader)

    # Проверяем, что логгер был создан
    from src.file_reader import logger
    assert logger is not None


def test_file_reader_imports():
    """Тестируем, что все импорты работают корректно."""
    from src.file_reader import read_csv_file, read_excel_file, convert_transaction_format
    assert callable(read_csv_file)
    assert callable(read_excel_file)
    assert callable(convert_transaction_format)


@pytest.mark.parametrize("input_data,expected_count", [
    ([], 0),
    ([{}], 1),
    ([{}, {}], 2),
    (None, 0),
])
def test_convert_transaction_format_edge_cases(input_data, expected_count):
    """Тестируем граничные случаи для convert_transaction_format."""
    if input_data is None:
        result = convert_transaction_format(None)
    else:
        result = convert_transaction_format(input_data)

    assert len(result) == expected_count
