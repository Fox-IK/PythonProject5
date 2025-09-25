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
        # Удаляем все нецифровые символы для поддержки разных форматов
        cleaned = ''.join(filter(str.isdigit, card_number))

        if len(cleaned) != 16 or not cleaned.isdigit():
            error_msg = f"Invalid card number format: {card_number}"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        # Форматирование номера
        masked = f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
        masks_logger.info(f"Card number masked successfully: {card_number} -> {masked}")
        return masked

    except Exception as e:
        error_msg = f"Error masking card number {card_number}: {e}"
        masks_logger.error(error_msg)
        raise


def get_mask_account_number(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    try:
        # Удаляем все нецифровые символы
        cleaned = ''.join(filter(str.isdigit, account_number))

        if len(cleaned) < 4 or not cleaned.isdigit():
            error_msg = f"Invalid account number format: {account_number}"
            masks_logger.error(error_msg)
            raise ValueError(error_msg)

        masked = f"**{cleaned[-4:]}"
        masks_logger.info(f"Account number masked successfully: {account_number} -> {masked}")
        return masked

    except Exception as e:
        error_msg = f"Error masking account number {account_number}: {e}"
        masks_logger.error(error_msg)
        raise


# Алиас для обратной совместимости с тестами
get_mask_account = get_mask_account_number
