def filter_by_state(data: list[dict], state_value: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state'
    """
    return [ item for item in data if item.get("state") == state_value ]
