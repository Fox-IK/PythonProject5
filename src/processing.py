import re
from typing import List, Dict, Any, Optional

def filter_by_state(data: list[dict[str, Any]], state_value: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'

    :param data: Список словарей для обработки
    :param state_value: Значение для фильтрации (по умолчанию 'EXECUTED')
    :return: Отфильтрованный список словарей
    """
    return [item for item in data if item.get("state") == state_value]


def sort_by_date(data: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'

    :param data: Список словарей для сортировки
    :param reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)
    :return: Отсортированный список словарей
    """
    return sorted(data, key=lambda x: x["date"], reverse=reverse)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по строке поиска в описании с использованием регулярных выражений.

    :param data: Список словарей с данными о банковских операциях
    :param search: Строка для поиска в описании операций
    :return: Отфильтрованный список операций
    """
    if not search or not data:
        return []

    try:
        # Создаем регулярное выражение для поиска без учета регистра
        pattern = re.compile(re.escape(search), re.IGNORECASE)
        filtered_data = []

        for transaction in data:
            description = transaction.get("description", "")
            if pattern.search(description):
                filtered_data.append(transaction)

        return filtered_data

    except re.error:
        # В случае ошибки в регулярном выражении возвращаем пустой список
        return []


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    :param data: Список словарей с данными о банковских операциях
    :param categories: Список категорий для подсчета
    :return: Словарь с количеством операций по категориям
    """
    if not data or not categories:
        return {}

    # Приводим категории к нижнему регистру для сравнения без учета регистра
    categories_lower = [cat.lower() for cat in categories]
    result = {category: 0 for category in categories}

    for transaction in data:
        description = transaction.get("description", "").lower()

        for category in categories_lower:
            if category in description:
                # Используем оригинальное название категории из входного списка
                original_category = categories[categories_lower.index(category)]
                result[original_category] += 1

    return result


def filter_by_currency_code(data: List[Dict[str, Any]], currency_code: str = "RUB") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты.

    :param data: Список словарей с транзакциями
    :param currency_code: Код валюты для фильтрации
    :return: Отфильтрованный список транзакций
    """
    filtered_data = []

    for transaction in data:
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        if currency.get("code") == currency_code:
            filtered_data.append(transaction)

    return filtered_data
