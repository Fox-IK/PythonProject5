import pytest
from src.widget import mask_account_card, get_date


# Фикстура для тестовых данных виджета
@pytest.fixture(params=[
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
    ("МИР 1111222233334444", "МИР 1111 22** **** 4444"),
])
def widget_data(request):
    return request.param


# Фикстура для тестов даты
@pytest.fixture(params=[
    ("2019-07-03T18:35:29.512364", "03.07.2019"),
    ("2018-06-30T02:08:58.425572", "30.06.2018"),
    ("2020-01-01T00:00:00.000000", "01.01.2020"),  # Граничное значение
    ("1999-12-31T23:59:59.999999", "31.12.1999"),  # Граничное значение
])
def date_data(request):

    return request.param


def test_mask_account_card(widget_data):
    input_str, expected = widget_data
    assert mask_account_card(input_str) == expected


def test_get_date(date_data):
    input_date, expected = date_data
    assert get_date(input_date) == expected
