def filter_by_state(data: list[dict], state_value: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'

    :param data: Список словарей для обработки
    :param state_value: Значение для фильтрации (по умолчанию 'EXECUTED')
    :return: Отфильтрованный список словарей
    """
    return [ item for item in data if item.get("state") == state_value ]


def sort_by_date ( data: list [ dict ],reverse: bool = True ) -> list [ dict ] :
    """
    Сортирует список словарей по ключу 'date'

    :param data: Список словарей для сортировки
    :param reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)
    :return: Отсортированный список словарей
    """
    return sorted(data,key=lambda x : x [ "date" ],reverse=reverse)

