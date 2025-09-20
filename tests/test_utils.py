import pytest
import json
import tempfile
import os
from pathlib import Path
from src.utils import load_json_data


def test_load_json_data_valid_file():
    """Тестируем загрузку данных из валидного JSON-файла."""
    # Создаем временный файл с валидными данными
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump([{"id": 1, "amount": 100}], f)
        temp_filename = f.name

    try:
        # Загружаем данные
        result = load_json_data(temp_filename)

        # Проверяем результат
        assert result == [{"id": 1, "amount": 100}]
    finally:
        # Удаляем временный файл
        os.unlink(temp_filename)


def test_load_json_data_empty_file():
    """Тестируем загрузку данных из пустого файла."""
    # Создаем временный пустой файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_filename = f.name

    try:
        # Загружаем данные
        result = load_json_data(temp_filename)

        # Проверяем результат
        assert result == []
    finally:
        # Удаляем временный файл
        os.unlink(temp_filename)


def test_load_json_data_invalid_json():
    """Тестируем загрузку данных из файла с невалидным JSON."""
    # Создаем временный файл с невалидным JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json")
        temp_filename = f.name

    try:
        # Загружаем данные
        result = load_json_data(temp_filename)

        # Проверяем результат
        assert result == []
    finally:
        # Удаляем временный файл
        os.unlink(temp_filename)


def test_load_json_data_not_list():
    """Тестируем загрузку данных из файла, где данные не являются списком."""
    # Создаем временный файл с объектом вместо массива
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"id": 1, "amount": 100}, f)
        temp_filename = f.name

    try:
        # Загружаем данные
        result = load_json_data(temp_filename)

        # Проверяем результат
        assert result == []
    finally:
        # Удаляем временный файл
        os.unlink(temp_filename)


def test_load_json_data_nonexistent_file():
    """Тестируем загрузку данных из несуществующего файла."""
    result = load_json_data("nonexistent_file.json")
    assert result == []
