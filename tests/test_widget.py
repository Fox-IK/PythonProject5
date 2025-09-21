import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("input_str, expected", [
    ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
    ("Счет 73654108430135874305", "Счет **4305"),
    ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
    ("МИР 1111222233334444", "МИР 1111 22** **** 4444"),
])
def test_mask_account_card(input_str, expected):
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("date_str, expected", [
    ("2019-07-03T18:35:29.512364", "03.07.2019"),
    ("2018-06-30T02:08:58.425572", "30.06.2018"),
    ("2020-01-01T00:00:00.000000", "01.01.2020"),
])
def test_get_date(date_str, expected):
    assert get_date(date_str) == expected


def test_get_date_invalid():
    assert get_date("invalid-date") == "Некорректная дата"
    assert get_date("") == "Некорректная дата"
