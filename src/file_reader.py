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


def convert_transaction_format(transactions: list[dict]) -> list[dict]:
    """Конвертирует транзакции в единый формат."""
    converted = []
    for transaction in transactions:
        # Создаем копию транзакции
        new_transaction = transaction.copy()

        # Обработка альтернативных названий полей
        if "transaction_id" in new_transaction:
            new_transaction["id"] = new_transaction["transaction_id"]

        if "status" in new_transaction:
            new_transaction["state"] = new_transaction["status"]

        if "transaction_date" in new_transaction:
            new_transaction["date"] = new_transaction["transaction_date"]

        # Обработка вложенного operationAmount
        if "operationAmount" in new_transaction and isinstance(new_transaction["operationAmount"], dict):
            op_amount = new_transaction["operationAmount"]
            if "value" in op_amount:
                # Создаем копию operationAmount с правильной структурой
                new_op_amount = op_amount.copy()
                new_op_amount["amount"] = op_amount["value"]
                # Сохраняем валюту, если она есть
                if "currency" in op_amount:
                    new_op_amount["currency"] = op_amount["currency"]
                new_transaction["operationAmount"] = new_op_amount

        # Обработка простых полей amount и currency
        elif "amount" in new_transaction:
            # Создаем структуру operationAmount из простых полей
            new_transaction["operationAmount"] = {
                "amount": str(new_transaction["amount"]),
                "currency": {
                    "code": new_transaction.get("currency", ""),
                    "name": new_transaction.get("currency_name", "")
                }
            }

        converted.append(new_transaction)

    return converted
