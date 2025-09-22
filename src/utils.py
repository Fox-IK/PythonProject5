import json
import logging
import os
from pathlib import Path
from typing import List, Dict, Any

# Создаем папку для логов, если она не существует
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

#  Создан отдельный объект логера для модуля utils
utils_logger = logging.getLogger("utils")

#  Установлен уровень логирования не меньше, чем DEBUG
utils_logger.setLevel(logging.DEBUG)

#  Настроен file_handler для логера модуля utils
file_handler = logging.FileHandler("logs/utils.log", mode="w")
file_handler.setLevel(logging.DEBUG)

#  Настроен file_formatter для логера модуля utils
#  Формат записи логов включает метку времени, название модуля, уровень серьезности и сообщение
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

#  Установлен форматер для логера модуля utils
file_handler.setFormatter(file_formatter)

#  Добавлен handler для логера модуля utils
utils_logger.addHandler(file_handler)


def load_json_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные из JSON-файла и возвращает список словарей.
    """
    try:
        path = Path(file_path)

        if not path.exists():
            #  Логирование ошибочных случаев с уровнем не ниже ERROR
            utils_logger.error("Файл не найден: %s", file_path)
            return []

        if not path.is_file():
            utils_logger.error("Указанный путь ведет к директории: %s", file_path)
            return []

        if path.stat().st_size == 0:
            utils_logger.error("Файл пустой: %s", file_path)
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            if not isinstance(data, list):
                utils_logger.error("Данные в файле не являются списком: %s", file_path)
                return []

            # Логирование включено в успешные случаи использования функций
            utils_logger.info("Успешно загружено %d записей из файла: %s", len(data), file_path)
            return data

    except json.JSONDecodeError as e:
        utils_logger.error("Ошибка декодирования JSON: %s", str(e))
        return []
    except Exception as e:
        utils_logger.error("Неожиданная ошибка: %s", str(e))
        return []

