import pytest

from src.masks import get_mask_account_number, get_mask_card_number


def test_get_mask_card_number_valid():
    """Тестируем маскирование валидного номера карты."""
    assert get_mask_card_number("1234567812345678") == "1234 56** **** 5678"
    assert get_mask_card_number("1234 5678 1234 5678") == "1234 56** **** 5678"


def test_get_mask_card_number_invalid():
    """Тестируем обработку невалидных номеров карт."""
    with pytest.raises(ValueError):
        get_mask_card_number("1234")  # Слишком короткий номер

    with pytest.raises(ValueError):
        get_mask_card_number("123456781234567a")  # Не цифры


def test_get_mask_account_number_valid():
    """Тестируем маскирование валидного номера счета."""
    assert get_mask_account_number("1234567890123456") == "**3456"
    assert get_mask_account_number("1234 5678 9012 3456") == "**3456"


def test_get_mask_account_number_invalid():
    """Тестируем обработку невалидных номеров счетов."""
    with pytest.raises(ValueError):
        get_mask_account_number("123")  # Слишком короткий номер

    with pytest.raises(ValueError):
        get_mask_account_number("12a")  # После очистки "12" - слишком короткий

    with pytest.raises(ValueError):
        get_mask_account_number("abc")  # После очистки "" - пустая строка


def test_get_mask_card_number_edge_cases():
    """Тестируем крайние случаи маскирования карт."""
    # Карта с пробелами
    assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"

    # Карта с разными разделителями - должна обрабатываться корректно
    # так как функция удаляет все нецифровые символы
    assert get_mask_card_number("1234-5678-9012-3456") == "1234 56** **** 3456"


def test_get_mask_account_number_edge_cases():
    """Тестируем крайние случаи маскирования счетов."""
    # Счет с пробелами
    assert get_mask_account_number("1234 5678 9012 3456") == "**3456"

    # Счет с минимальной длиной (4 цифры)
    assert get_mask_account_number("1234") == "**1234"


def test_get_mask_card_number_special_characters():
    """Тестируем обработку специальных символов в номерах карт."""
    # Должно работать, так как функция фильтрует только цифры
    assert get_mask_card_number("1234abcd5678efgh9012ijkl3456") == "1234 56** **** 3456"


def test_get_mask_account_number_special_characters():
    """Тестируем обработку специальных символов в номерах счетов."""
    # Должно работать, так как функция фильтрует только цифры
    assert get_mask_account_number("1234abcd5678efgh9012ijkl3456") == "**3456"


def test_get_mask_card_number_logging(caplog):
    """Тестируем логирование при маскировании карт."""
    with caplog.at_level("INFO"):
        # Убрали присваивание неиспользуемой переменной
        get_mask_card_number("1234567812345678")
        assert "Card number masked successfully" in caplog.text


def test_get_mask_account_number_logging(caplog):
    """Тестируем логирование при маскировании счетов."""
    with caplog.at_level("INFO"):
        # Убрали присваивание неиспользуемой переменной
        get_mask_account_number("1234567890123456")
        assert "Account number masked successfully" in caplog.text


def test_get_mask_account_number_valid_with_special_chars():
    """Тестируем валидные номера счетов со специальными символами."""
    # Эти случаи должны работать, так как после очистки остаются валидные номера
    assert get_mask_account_number("12345678901234ab") == "**1234"
    assert get_mask_account_number("1234-5678-9012-3456") == "**3456"
