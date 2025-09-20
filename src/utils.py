import json
from typing import List, Dict, Any
from pathlib import Path


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные из JSON-файла и возвращает список словарей.

    :param file_path: Путь до JSON-файла
    :return: Список словарей с данными о финансовых транзакциях
    """
    try:
        # Проверяем существование файла
        if not Path(file_path).exists():
            return []

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if not isinstance(data, list):
                return []

            return data

    except (json.JSONDecodeError, IOError):
        # В случае ошибки декодирования JSON или ошибки ввода-вывода
        return []
