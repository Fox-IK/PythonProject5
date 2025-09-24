import json
import os
import tempfile

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


def test_load_json_data_permission_error(monkeypatch):
    """Тестируем обработку ошибки прав доступа."""

    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)
    result = load_json_data("test.json")
    assert result == []


def test_load_json_data_unicode_error(monkeypatch):
    """Тестируем обработку ошибки кодирования."""

    def mock_open(*args, **kwargs):
        raise UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid byte")

    monkeypatch.setattr("builtins.open", mock_open)
    result = load_json_data("test.json")
    assert result == []


def test_load_json_data_large_file():
    """Тестируем загрузку большого файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        # Создаем файл с большим количеством данных
        data = [{"id": i, "amount": i * 100} for i in range(1000)]
        json.dump(data, f)
        temp_filename = f.name

    try:
        result = load_json_data(temp_filename)
        assert len(result) == 1000
        assert result[0]["id"] == 0
        assert result[-1]["id"] == 999
    finally:
        os.unlink(temp_filename)
