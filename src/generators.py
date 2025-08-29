from typing import Iterator,Dict,Any,List


def filter_by_currency(transactions: List[Dict[str,Any]],currency_code: str) -> Iterator[Dict[str,Any]]:
    """
    Фильтрует транзакции по валюте операции.

    :param transactions: Список словарей с транзакциями
    :param currency_code: Код валюты для фильтрации
    :return: Итератор транзакций в указанной валюте
    """
    for transaction in transactions:
        operation_amount=transaction.get("operationAmount",{})
        currency=operation_amount.get("currency",{})
        if currency.get("code")==currency_code:
            yield transaction
    pass

def transaction_descriptions(transactions: List[Dict[str,Any]]) -> Iterator[str]:
    """
    Извлекает описания транзакций.

    :param transactions: Список словарей с транзакциями
    :return: Итератор описаний транзакций
    """
    for transaction in transactions:
        yield transaction.get("description","")
    pass

def card_number_generator(start: int,end: int) -> Iterator[str]:
    """
    Генерирует номера банковских карт в заданном диапазоне.

    :param start: Начальный номер карты
    :param end: Конечный номер карты
    :return: Итератор номеров карт в формате "XXXX XXXX XXXX XXXX"
    """
    for num in range(start,end + 1):
        num_str=str(num).zfill(16)
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
    pass
