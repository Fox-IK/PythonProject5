# Добавляем к существующим тестам

def test_convert_amount_missing_operation_amount():
    """Тестируем обработку отсутствия operationAmount в транзакции."""
    transaction = {}
    result = convert_amount(transaction)
    assert result is None


def test_convert_amount_missing_currency_code():
    """Тестируем обработку отсутствия кода валюты в транзакции."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {}
        }
    }
    result = convert_amount(transaction)
    assert result is None


def test_convert_amount_invalid_api_response(mock_env):
    """Тестируем обработку неверного формата ответа от API."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'USD'
            }
        }
    }

    # Мокируем ответ API с неверным форматом
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'invalid': 'response'
    }

    with patch('requests.get', return_value=mock_response):
        result = convert_amount(transaction)
        assert result is None


def test_convert_amount_timeout_error(mock_env):
    """Тестируем обработку таймаута при запросе к API."""
    transaction = {
        'operationAmount': {
            'amount': '100.0',
            'currency': {
                'code': 'USD'
            }
        }
    }

    with patch('requests.get', side_effect=requests.Timeout()):
        result = convert_amount(transaction)
        assert result is None
