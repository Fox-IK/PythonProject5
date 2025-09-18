import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


def convert_amount(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Конвертирует сумму транзакции в рубли.

    :param transaction: Словарь с данными о транзакции
    :return: Сумма транзакции в рублях (float) или None в случае ошибки
    """
    try:
        # Проверяем наличие необходимых ключей
        if 'operationAmount' not in transaction:
            return None

        operation_amount = transaction['operationAmount']
        if 'amount' not in operation_amount or 'currency' not in operation_amount:
            return None

        if 'code' not in operation_amount['currency']:
            return None

        # Получаем сумму и валюту из транзакции
        amount = float(operation_amount['amount'])
        currency = operation_amount['currency']['code']

        # Если валюта уже рубли, возвращаем как есть
        if currency == 'RUB':
            return amount

        # Получаем API ключ из переменных окружения
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        if not api_key:
            raise ValueError("API ключ не найден в переменных окружения")

        # Формируем URL для запроса курса валют
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"

        # Выполняем запрос к API
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers, timeout=10)

        # Проверяем успешность запроса
        if response.status_code != 200:
            raise Exception(f"Ошибка при запросе курса валют: {response.status_code}")

        # Получаем курс из ответа
        data = response.json()

        if 'rates' not in data or 'RUB' not in data['rates']:
            raise Exception("Неверный формат ответа от API")

        rate = data['rates']['RUB']

        # Конвертируем сумму
        return amount * rate

    except (ValueError, KeyError, requests.RequestException, Exception) as e:
        # Логируем ошибку, но не прерываем выполнение программы
        print(f"Ошибка при конвертации валюты: {e}")
        return None
