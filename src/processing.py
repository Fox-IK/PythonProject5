from typing import Any


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
