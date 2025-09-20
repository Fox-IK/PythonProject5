import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


def convert_amount(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    :param transaction: Словарь с данными о транзакции
    :return: Сумма транзакции в рублях (float)
    """
    # Получаем сумму и валюту из транзакции
    amount = float(transaction['operationAmount']['amount'])
    currency = transaction['operationAmount']['currency']['code']

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
    response = requests.get(url, headers=headers)

    # Проверяем успешность запроса
    if response.status_code != 200:
        raise Exception(f"Ошибка при запросе курса валют: {response.status_code}")

    # Получаем курс из ответа
    data = response.json()
    rate = data['rates']['RUB']

    # Конвертируем сумму
    return amount * rate
