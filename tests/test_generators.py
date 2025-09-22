from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Фикстура с тестовыми данными транзакций
@pytest.fixture
def sample_transactions() -> List[Dict[str , Any]] :
    return [
        {
            "id" : 939719570 ,
            "state" : "EXECUTED" ,
            "date" : "2018-06-30T02:08:58.425572" ,
            "operationAmount" : {
                "amount" : "9824.07" ,
                "currency" : {"name" : "USD" , "code" : "USD"}
            } ,
            "description" : "Перевод организации" ,
            "from" : "Счет 75106830613657916952" ,
            "to" : "Счет 11776614605963066702"
        } ,
        {
            "id" : 142264268 ,
            "state" : "EXECUTED" ,
            "date" : "2019-04-04T23:20:05.206878" ,
            "operationAmount" : {
                "amount" : "79114.93" ,
                "currency" : {"name" : "USD" , "code" : "USD"}
            } ,
            "description" : "Перевод со счета на счет" ,
            "from" : "Счет 19708645243227258542" ,
            "to" : "Счет 75651667383060284188"
        } ,
        {
            "id" : 873106923 ,
            "state" : "EXECUTED" ,
            "date" : "2019-03-23T01:09:46.296404" ,
            "operationAmount" : {
                "amount" : "43318.34" ,
                "currency" : {"name" : "руб." , "code" : "RUB"}
            } ,
            "description" : "Перевод со счета на счет" ,
            "from" : "Счет 44812258784861134719" ,
            "to" : "Счет 74489636417521191160"
        } ,
        {
            "id" : 895315941 ,
            "state" : "EXECUTED" ,
            "date" : "2018-08-19T04:27:37.904916" ,
            "operationAmount" : {
                "amount" : "56883.54" ,
                "currency" : {"name" : "USD" , "code" : "USD"}
            } ,
            "description" : "Перевод с карты на карту" ,
            "from" : "Visa Classic 6831982476737658" ,
            "to" : "Visa Platinum 8990922113665229"
        } ,
        {
            "id" : 594226727 ,
            "state" : "CANCELED" ,
            "date" : "2018-09-12T21:27:25.241689" ,
            "operationAmount" : {
                "amount" : "67314.70" ,
                "currency" : {"name" : "руб." , "code" : "RUB"}
            } ,
            "description" : "Перевод организации" ,
            "from" : "Visa Platinum 1246377376343588" ,
            "to" : "Счет 14211924144426031657"
        }
    ]


# Тесты для filter_by_currency
@pytest.mark.parametrize("currency,expected_count,expected_ids" , [
    ("USD" , 3 , [939719570 , 142264268 , 895315941]) ,
    ("RUB" , 2 , [873106923 , 594226727]) ,
    ("EUR" , 0 , []) ,
    ("" , 0 , [])
])
def test_filter_by_currency(sample_transactions: List[Dict[str , Any]] ,
                            currency: str , expected_count: int , expected_ids: List[int]) :
    """Проверяем фильтрацию транзакций по валюте"""
    filtered_transactions = list(filter_by_currency(sample_transactions , currency))

    # Проверяем количество отфильтрованных транзакций
    assert len(filtered_transactions) == expected_count

    # Проверяем, что все транзакции имеют правильную валюту
    for transaction in filtered_transactions :
        assert transaction["operationAmount"]["currency"]["code"] == currency

    # Проверяем ID транзакций
    transaction_ids = [t["id"] for t in filtered_transactions]
    assert transaction_ids == expected_ids


def test_filter_by_currency_empty_input() :
    """Проверяем обработку пустого списка транзакций"""
    assert list(filter_by_currency([] , "USD")) == []


def test_filter_by_currency_no_matching_currency(sample_transactions: List[Dict[str , Any]]) :
    """Проверяем обработку случая, когда нет транзакций в указанной валюте"""
    result = list(filter_by_currency(sample_transactions , "JPY"))
    assert len(result) == 0


# Тесты для transaction_descriptions
@pytest.mark.parametrize("index,expected_description" , [
    (0 , "Перевод организации") ,
    (1 , "Перевод со счета на счет") ,
    (2 , "Перевод со счета на счет") ,
    (3 , "Перевод с карты на карту") ,
    (4 , "Перевод организации")
])
def test_transaction_descriptions(sample_transactions: List[Dict[str , Any]] ,
                                  index: int , expected_description: str) :
    """Проверяем извлечение описаний транзакций"""
    gen = transaction_descriptions(sample_transactions)

    # Пропускаем первые index элементов
    for i in range(index) :
        next(gen)

    # Проверяем description текущего элемента
    assert next(gen) == expected_description


def test_transaction_descriptions_empty_input() :
    """Проверяем обработку пустого списка транзакций"""
    gen = transaction_descriptions([])
    assert next(gen , None) is None


def test_transaction_descriptions_all_descriptions(sample_transactions: List[Dict[str , Any]]) :
    """Проверяем извлечение всех описаний транзакций"""
    gen = transaction_descriptions(sample_transactions)
    all_descriptions = list(gen)

    expected_descriptions = [
        "Перевод организации" ,
        "Перевод со счета на счет" ,
        "Перевод со счета на счет" ,
        "Перевод с карты на карту" ,
        "Перевод организации"
    ]

    assert all_descriptions == expected_descriptions


# Тесты для card_number_generator
@pytest.mark.parametrize("start,end,expected_count,expected_first,expected_last" , [
    (1 , 5 , 5 , "0000 0000 0000 0001" , "0000 0000 0000 0005") ,
    (9999999999999995 , 9999999999999999 , 5 , "9999 9999 9999 9995" , "9999 9999 9999 9999") ,
    (1 , 1 , 1 , "0000 0000 0000 0001" , "0000 0000 0000 0001") ,
    (0 , 0 , 1 , "0000 0000 0000 0000" , "0000 0000 0000 0000")
])
def test_card_number_generator(start: int , end: int , expected_count: int ,
                               expected_first: str , expected_last: str) :
    """Проверяем генерацию номеров карт в заданном диапазоне"""
    numbers = list(card_number_generator(start , end))

    # Проверяем количество сгенерированных номеров
    assert len(numbers) == expected_count

    # Проверяем первый и последний номера
    assert numbers[0] == expected_first
    assert numbers[-1] == expected_last


@pytest.mark.parametrize("number" , [
    "0000 0000 0000 0001" ,
    "1234 5678 9012 3456" ,
    "9999 9999 9999 9999"
])
def test_card_number_format(number: str) :
    """Проверяем форматирование номеров карт"""
    parts = number.split()

    # Проверяем, что номер состоит из 4 частей
    assert len(parts) == 4

    # Проверяем, что каждая часть состоит из 4 цифр
    for part in parts :
        assert len(part) == 4
        assert part.isdigit()


def test_card_number_generator_invalid_range():
    """Проверяем обработку неверного диапазона (start > end)"""
    with pytest.raises(ValueError, match="Начальное значение не может быть больше конечного"):
        list(card_number_generator(10 , 5))


def test_card_number_generator_large_range() :
    """Проверяем генерацию большого диапазона номеров карт"""
    # Генерируем 10 номеров карт
    numbers = list(card_number_generator(1 , 10))

    # Проверяем количество
    assert len(numbers) == 10

    # Проверяем, что все номера уникальны
    assert len(set(numbers)) == 10

    # Проверяем формат каждого номера
    for number in numbers :
        parts = number.split()
        assert len(parts) == 4
        for part in parts :
            assert len(part) == 4
            assert part.isdigit()


# Дополнительные тесты для проверки крайних случаев
def test_filter_by_currency_missing_operation_amount(sample_transactions: List[Dict[str , Any]]) :
    """Проверяем обработку транзакций с отсутствующим operationAmount"""
    # Создаем копию транзакции без operationAmount
    transaction_without_amount = sample_transactions[0].copy()
    del transaction_without_amount["operationAmount"]

    modified_transactions = [transaction_without_amount]

    # Транзакция без operationAmount не должна быть включена в результат
    result = list(filter_by_currency(modified_transactions , "USD"))
    assert len(result) == 0


def test_filter_by_currency_missing_currency(sample_transactions: List[Dict[str , Any]]) :
    """Проверяем обработку транзакций с отсутствующим currency"""
    # Создаем копию транзакции без currency
    transaction_without_currency = sample_transactions[0].copy()
    del transaction_without_currency["operationAmount"]["currency"]

    modified_transactions = [transaction_without_currency]

    # Транзакция без currency не должна быть включена в результат
    result = list(filter_by_currency(modified_transactions , "USD"))
    assert len(result) == 0


def test_transaction_descriptions_missing_description(sample_transactions: List[Dict[str , Any]]) :
    """Проверяем обработку транзакций с отсутствующим description"""
    # Создаем копию транзакции без description
    transaction_without_description = sample_transactions[0].copy()
    del transaction_without_description["description"]

    modified_transactions = [transaction_without_description]

    # Транзакция без description должна вернуть пустую строку
    gen = transaction_descriptions(modified_transactions)
    assert next(gen) == ""
