import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

# Настройка логгера для модуля
logger = logging.getLogger("file_reader")
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler("logs/file_reader.log", mode="w")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    :param file_path: Путь к CSV-файлу
    :return: Список словарей с транзакциями
    """
    try:
        path = Path(file_path)

        if not path.exists():
            logger.error(f"CSV файл не найден: {file_path}")
            return []

        if not path.is_file():
            logger.error(f"Указанный путь ведет к директории: {file_path}")
            return []

        if path.stat().st_size == 0:
            logger.error(f"CSV файл пустой: {file_path}")
            return []

        # Чтение CSV файла
        df = pd.read_csv(file_path)

        # Преобразование DataFrame в список словарей
        transactions = df.to_dict('records')

        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV: {file_path}")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла {file_path}: {str(e)}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.

    :param file_path: Путь к Excel-файлу
    :return: Список словарей с транзакциями
    """
    try:
        path = Path(file_path)

        if not path.exists():
            logger.error(f"Excel файл не найден: {file_path}")
            return []

        if not path.is_file():
            logger.error(f"Указанный путь ведет к директории: {file_path}")
            return []

        if path.stat().st_size == 0:
            logger.error(f"Excel файл пустой: {file_path}")
            return []

        # Чтение Excel файла
        df = pd.read_excel(file_path)

        # Преобразование DataFrame в список словарей
        transactions = df.to_dict('records')

        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel: {file_path}")
        return transactions

    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла {file_path}: {str(e)}")
        return []


def convert_transaction_format(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Конвертирует транзакции в единый формат (опционально).

    :param transactions: Список транзакций в исходном формате
    :return: Список транзакций в стандартном формате
    """
    converted = []

    for transaction in transactions:
        try:
            # Преобразование в стандартный формат
            converted_transaction = {
                "id": transaction.get("id"),
                "state": transaction.get("state", "UNKNOWN"),
                "date": transaction.get("date", ""),
                "operationAmount": {
                    "amount": str(transaction.get("amount", transaction.get("operationAmount", ""))),
                    "currency": {
                        "name": transaction.get("currency", transaction.get("currency_name", "")),
                        "code": transaction.get("currency_code", transaction.get("currency", ""))
                    }
                },
                "description": transaction.get("description", ""),
                "from": transaction.get("from", ""),
                "to": transaction.get("to", "")
            }
            converted.append(converted_transaction)
        except Exception as e:
            logger.warning(f"Ошибка при конвертации транзакции: {e}")
            continue

    return converted
