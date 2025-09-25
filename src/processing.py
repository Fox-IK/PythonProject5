import re
from typing import Any, Dict, List
from collections import Counter


def count_transactions_by_type(
    transactions: List[Dict[str, Any]],
    transaction_type_field: str = "description"
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по типам с использованием Counter.

    Args:
        transactions: Список транзакций
        transaction_type_field: Поле, по которому группировать операции

    Returns:
        Словарь с количеством операций каждого типа
    """
    if not transactions:
        return {}

    # Извлекаем значения поля для группировки
    type_values = []
    for transaction in transactions:
        transaction_type = transaction.get(transaction_type_field)
        if transaction_type is not None:
            type_values.append(transaction_type)

    # Используем Counter для эффективного подсчета
    type_counter = Counter(type_values)
    return dict(type_counter)


def count_transactions_by_status(transactions: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Специализированная функция для подсчета операций по статусу.

    Args:
        transactions: Список транзакций

    Returns:
        Словарь с количеством операций каждого статуса
    """
    return count_transactions_by_type(transactions, "state")


def count_transactions_by_currency(transactions: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Специализированная функция для подсчета операций по валюте.

    Args:
        transactions: Список транзакций

    Returns:
        Словарь с количеством операций каждой валюты
    """
    currency_values = []
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        if isinstance(operation_amount, dict):
            currency_info = operation_amount.get("currency", {})
            if isinstance(currency_info, dict):
                currency_code = currency_info.get("code")
                if currency_code:
                    currency_values.append(currency_code)

    return dict(Counter(currency_values))


def filter_by_state(
    data: List[Dict[str, Any]],
    state_value: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'

    Args:
        data: Список словарей для обработки
        state_value: Значение для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список словарей
    """
    return [item for item in data if item.get("state") == state_value]


def sort_by_date(
    data: List[Dict[str, Any]],
    reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по ключу 'date'

    Args:
        data: Список словарей для сортировки
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        Отсортированный список словарей
    """
    return sorted(data, key=lambda x: x.get("date", ""), reverse=reverse)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по строке поиска в описании.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании операций

    Returns:
        Отфильтрованный список операций
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


def process_bank_operations(
    data: List[Dict[str, Any]],
    categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством операций по категориям
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


def filter_by_currency_code(
    data: List[Dict[str, Any]],
    currency_code: str = "RUB"
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты.

    Args:
        data: Список словарей с транзакциями
        currency_code: Код валюты для фильтрации

    Returns:
        Отфильтрованный список транзакций
    """
    filtered_data = []

    for transaction in data:
        operation_amount = transaction.get("operationAmount", {})
        if isinstance(operation_amount, dict):
            currency = operation_amount.get("currency", {})
            if isinstance(currency, dict) and currency.get("code") == currency_code:
                filtered_data.append(transaction)

    return filtered_data
