import pytest

from src.widget import get_date, mask_account_card


# Параметризованные тесты для mask_account_card
@pytest.mark.parametrize("input_str, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
    ("МИР 1111222233334444", "МИР 1111 22** **** 4444"),
])
def test_mask_account_card(input_str, expected):
    """Тестируем маскирование карт и счетов с различными входными данными."""
    assert mask_account_card(input_str) == expected


# Параметризованные тесты для get_date
@pytest.mark.parametrize("input_date, expected", [
    ("2019-07-03T18:35:29.512364", "03.07.2019"),
    ("2018-06-30T02:08:58.425572", "30.06.2018"),
    ("2020-01-01T00:00:00.000000", "01.01.2020"),
    ("1999-12-31T23:59:59.999999", "31.12.1999"),
])
def test_get_date(input_date, expected):
    """Тестируем форматирование даты с различными входными данными."""
    assert get_date(input_date) == expected


def test_mask_account_card_edge_cases():
    """Тестируем крайние случаи маскирования карт/счетов."""
    # Пустая строка
    assert mask_account_card("") == "Некорректные данные"

    # Только тип без номера
    assert mask_account_card("Счет") == "Некорректные данные"

    # None
    assert mask_account_card(None) == "Некорректные данные"

    # Не строка
    assert mask_account_card(123) == "Некорректные данные"

    # Номер с недостаточным количеством цифр
    assert mask_account_card("Счет 123") == "Некорректные данные"


def test_get_date_edge_cases():
    """Тестируем крайние случаи форматирования даты."""
    # Неполная дата
    assert get_date("2023-01") == "Некорректная дата"

    # Пустая строка
    assert get_date("") == "Некорректная дата"

    # None
    assert get_date(None) == "Некорректная дата"

    # Неправильный формат
    assert get_date("invalid-date") == "Некорректная дата"

    # Дата без времени
    assert get_date("2023-01-01") == "01.01.2023"
