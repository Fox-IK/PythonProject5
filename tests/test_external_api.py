import os
from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_amount


@pytest.fixture
def mock_env():
    """Фикстура для мокирования переменных окружения."""
    with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'}):
        yield


def test_convert_amount_rub():
    """Тестируем конвертацию рублей (должна возвращать ту же сумму)."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'RUB'
            }
        }
    }

    result = convert_amount(transaction)
    assert result == 100.0


def test_convert_amount_usd(mock_env):
    """Тестируем конвертацию USD в RUB с мокированием API."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'USD'
            }
        }
    }

    # Мокируем ответ API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'rates': {
            'RUB': 75.0
        }
    }

    with patch('requests.get', return_value=mock_response) as mock_get:
        result = convert_amount(transaction)

        # Проверяем результат
        assert result == 7500.0  # 100 * 75

        # Проверяем, что запрос был выполнен с правильными параметрами
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/latest?base=USD&symbols=RUB",
            headers={"apikey": "test_api_key"}
        )


def test_convert_amount_eur(mock_env):
    """Тестируем конвертацию EUR в RUB с мокированием API."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'EUR'
            }
        }
    }

    # Мокируем ответ API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'rates': {
            'RUB': 85.0
        }
    }

    with patch('requests.get', return_value=mock_response):
        result = convert_amount(transaction)
        assert result == 8500.0  # 100 * 85


def test_convert_amount_api_error(mock_env):
    """Тестируем обработку ошибки API."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'USD'
            }
        }
    }

    # Мокируем ошибку API
    mock_response = Mock()
    mock_response.status_code = 500

    with patch('requests.get', return_value=mock_response):
        with pytest.raises(Exception, match="Ошибка при запросе курса валют: 500"):
            convert_amount(transaction)


def test_convert_amount_missing_api_key():
    """Тестируем обработку отсутствия API ключа."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'USD'
            }
        }
    }

    # Убеждаемся, что переменная окружения не установлена
    if 'EXCHANGE_RATE_API_KEY' in os.environ:
        del os.environ['EXCHANGE_RATE_API_KEY']

    with pytest.raises(ValueError, match="API ключ не найден в переменных окружения"):
        convert_amount(transaction)


def test_convert_amount_invalid_amount():
    """Тестируем обработку невалидной суммы."""
    transaction = {
        'operationAmount': {
            'amount': 'invalid',
            'currency': {
                'code': 'USD'
            }
        }
    }

    with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_api_key'}):
        with pytest.raises(ValueError):
            convert_amount(transaction)
