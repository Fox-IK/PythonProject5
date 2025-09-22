import logging
from pathlib import Path

# Создаем папку для логов, если она не существует
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

#  Создан отдельный объект логера для модуля masks
masks_logger = logging.getLogger("masks")

#  Установлен уровень логирования не меньше, чем DEBUG
masks_logger.setLevel(logging.DEBUG)

#  Настроен file_handler для логера модуля masks
file_handler = logging.FileHandler("logs/masks.log", mode="w")
file_handler.setLevel(logging.DEBUG)

# Настроен file_formatter для логера модуля masks
# Формат записи логов включает метку времени, название модуля, уровень серьезности и сообщение
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Установлен форматер для логера модуля masks
file_handler.setFormatter(file_formatter)

# Добавлен handler для логера модуля masks
masks_logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    try:
        cleaned = card_number.replace(" ", "")
        if len(cleaned) != 16 or not cleaned.isdigit():
            error_msg = f"Invalid card number format: {card_number}"
            # ✅ Логирование ошибочных случаев с уровнем не ниже ERROR
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        masked_number = f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
        # Логирование включено в успешные случаи использования функций
        masks_logger.info("Card number masked successfully: %s -> %s", card_number, masked_number)
        return masked_number

    except Exception as e:
        masks_logger.error("Error masking card number %s: %s", card_number, str(e))
        raise


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    try:
        cleaned = account_number.replace(" ", "")
        if len(cleaned) < 4 or not cleaned.isdigit():
            error_msg = f"Invalid account number format: {account_number}"
            #  Логирование ошибочных случаев с уровнем не ниже ERROR
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        masked_number = f"**{cleaned[-4:]}"
        #  Логирование включено в успешные случаи использования функций
        masks_logger.info("Account number masked successfully: %s -> %s", account_number, masked_number)
        return masked_number

    except Exception as e:
        masks_logger.error("Error masking account number %s: %s", account_number, str(e))
        raise
