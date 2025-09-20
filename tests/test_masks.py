import pytest
from src.masks import get_mask_card_number, get_mask_account


# Фикстура для тестовых данных карт
@pytest.fixture(params=[
    ("7000792289606361", "7000 79** **** 6361"),
    ("1234567812345678", "1234 56** **** 5678"),
    ("1111222233334444", "1111 22** **** 4444"),
    ("9999888877776666", "9999 88** **** 6666"),
])


def card_data(request):

    return request.param

# Фикстура для тестовых данных счетов
@pytest.fixture(params=[
    ("73654108430135874305", "**4305"),
    ("12345678901234567890", "**7890"),
    ("11112222333344445555", "**5555"),
])
def account_data(request):

    return request.param


def test_get_mask_card_number(card_data):
    input_card, expected = card_data
    assert get_mask_card_number(input_card) == expected


def test_get_mask_account(account_data):
    input_account, expected = account_data
    assert get_mask_account(input_account) == expected
