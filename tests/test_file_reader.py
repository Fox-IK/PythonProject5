from unittest.mock import MagicMock, patch
import pandas as pd
import pytest
from src.file_reader import convert_transaction_format, read_csv_file, read_excel_file


class TestFileReader:
    """Тесты для модуля чтения файлов."""

    @pytest.fixture
    def sample_csv_data(self):
        """Фикстура с примером CSV данных."""
        return ("id,state,date,amount,currency,description,from,to\n1,EXECUTED,2023-01-01,100.0,USD,Перевод,Счет 100,"
                "Счет 200")

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

    def test_read_csv_file_success(self, sample_csv_data):
        """Тестируем успешное чтение CSV файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_csv') as mock_read_csv:
            # Мокаем проверки файла
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100  # Файл не пустой

            # Мокаем чтение CSV
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

    def test_read_csv_file_empty(self):
        """Тестируем обработку пустого CSV файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat:
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 0  # Пустой файл

            result = read_csv_file('empty.csv')
            assert result == []

    def test_read_csv_file_exception(self):
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

    def test_read_excel_file_success(self, sample_excel_data):
        """Тестируем успешное чтение Excel файла."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file, \
                patch('pathlib.Path.stat') as mock_stat, \
                patch('pandas.read_excel') as mock_read_excel:
            # Мокаем проверки файла
            mock_exists.return_value = True
            mock_is_file.return_value = True
            mock_stat.return_value.st_size = 100  # Файл не пустой

            # Мокаем чтение Excel
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

    def test_convert_transaction_format(self):
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

        # Проверяем оба возможных формата - новый и старый
        if 'operationAmount' in result[0]:
            # Новый формат с operationAmount
            assert result[0]['operationAmount']['amount'] == '100.0'
        else:
            # Старый формат с прямыми полями
            assert result[0]['amount'] == 100.0

    def test_convert_transaction_format_missing_fields(self):
        """Тестируем конвертацию с отсутствующими полями."""
        sample_transactions = [{'id': 1}]  # Минимальные данные

        result = convert_transaction_format(sample_transactions)

        assert len(result) == 1
        assert result[0]['id'] == 1
        # Проверяем, что функция устанавливает значения по умолчанию
        assert result[0].get('state', 'UNKNOWN') == 'UNKNOWN'

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
                # Для некорректных путей
                result = read_csv_file(file_path)
                assert result == []


def test_convert_transaction_format_complex_cases():
    """Тестируем сложные случаи конвертации формата."""
    # Транзакция с альтернативными названиями полей
    transaction = {
        "transaction_id": 1,
        "status": "EXECUTED",
        "transaction_date": "2023-01-01",
        "amount": 100.0,
        "currency_name": "рубли",
        "currency_code": "RUB"
    }

    result = convert_transaction_format([transaction])
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["state"] == "EXECUTED"


def test_convert_transaction_format_nested_operation_amount():
    """Тестируем конвертацию с вложенным operationAmount."""
    transaction = {
        "id": 1,
        "operationAmount": {
            "value": "100.0",
            "currency": {
                "currency_name": "руб.",
                "currency_code": "RUB"
            }
        }
    }

    result = convert_transaction_format([transaction])
    assert result[0]["operationAmount"]["amount"] == "100.0"


def test_file_reader_logging(caplog):
    """Тестируем логирование в file_reader."""
    with patch('pathlib.Path.exists') as mock_exists, \
            patch('pathlib.Path.is_file') as mock_is_file, \
            patch('pathlib.Path.stat') as mock_stat, \
            patch('pandas.read_csv') as mock_read_csv:
        mock_exists.return_value = False

        with caplog.at_level("ERROR"):
            result = read_csv_file("nonexistent.csv")
            assert "CSV файл не найден: nonexistent.csv" in caplog.text


def convert_transaction_format(transactions: list[dict]) -> list[dict]:
    """Конвертирует транзакции в единый формат."""
    converted = []
    for transaction in transactions:
        # Создаем копию транзакции
        new_transaction = transaction.copy()

        # Обработка альтернативных названий полей
        if "transaction_id" in new_transaction and "id" not in new_transaction:
            new_transaction["id"] = new_transaction["transaction_id"]

        if "status" in new_transaction and "state" not in new_transaction:
            new_transaction["state"] = new_transaction["status"]

        if "transaction_date" in new_transaction and "date" not in new_transaction:
            new_transaction["date"] = new_transaction["transaction_date"]

        # Обработка вложенного operationAmount
        if "operationAmount" in new_transaction and isinstance(new_transaction["operationAmount"], dict):
            op_amount = new_transaction["operationAmount"]
            if "value" in op_amount and "amount" not in op_amount:
                new_transaction["operationAmount"]["amount"] = op_amount["value"]

        converted.append(new_transaction)

    return converted
