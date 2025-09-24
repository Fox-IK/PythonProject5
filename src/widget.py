import logging
from datetime import datetime

from src.masks import get_mask_account_number, get_mask_card_number

# Настройка логгера для модуля widget
logger = logging.getLogger(__name__)


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета."""
    if not account_info or not isinstance(account_info, str):
        return "Некорректные данные"

    try:
        # Разделяем строку на слова
        parts = account_info.split()
        if len(parts) < 2:
            return "Некорректные данные"

        # Последняя часть - это номер
        number_str = parts[-1]

        # Определяем тип: счет или карта
        account_type = ' '.join(parts[:-1]).lower()

        if "счет" in account_type:
            masked_number = get_mask_account_number(number_str)
        else:
            masked_number = get_mask_card_number(number_str)

        # Собираем результат
        masked_result = f"{' '.join(parts[:-1])} {masked_number}"
        return masked_result

    except Exception as e:
        logger.error(f"Error masking account/card: {e}")
        return "Некорректные данные"


def get_date(date_str: str) -> str:
    """Форматирует дату в формате DD.MM.YYYY."""
    if not date_str:
        return "Некорректная дата"

    try:
        # Пытаемся разобрать дату в различных форматах
        formats = [
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d"
        ]

        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str, fmt)
                formatted_date = date_obj.strftime("%d.%m.%Y")
                return formatted_date
            except ValueError:
                continue

        return "Некорректная дата"
    except Exception as e:
        logger.error(f"Error formatting date: {e}")
        return "Некорректная дата"
