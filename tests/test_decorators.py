import os
import tempfile
import pytest
from src.decorators import log


def test_log_to_console(capsys):
    """Тестируем логирование в консоль."""

    @log()
    def test_func(x, y):
        return x + y

    # Вызываем функцию
    result = test_func(1, 2)

    # Проверяем результат
    assert result == 3

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "test_func ok" in captured.out


def test_log_to_file():
    """Тестируем логирование в файл."""

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
        temp_filename = f.name

    try:
        @log(filename=temp_filename)
        def test_func(x, y):
            return x + y

        # Вызываем функцию
        result = test_func(1, 2)

        # Проверяем результат
        assert result == 3

        # Проверяем запись в файл
        with open(temp_filename, "r", encoding="utf-8") as f:
            content = f.read()
            assert "test_func ok" in content

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_error_to_console(capsys):
    """Тестируем логирование ошибок в консоль."""

    @log()
    def test_func(x, y):
        raise ValueError("Test error")

    # Проверяем, что исключение пробрасывается
    with pytest.raises(ValueError):
        test_func(1, 2)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "test_func error: ValueError" in captured.out
    assert "Inputs: (1, 2), {}" in captured.out


def test_log_error_to_file():
    """Тестируем логирование ошибок в файл."""

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8") as f:
        temp_filename = f.name

    try:
        @log(filename=temp_filename)
        def test_func(x, y):
            raise ValueError("Test error")

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ValueError):
            test_func(1, 2)

        # Проверяем запись в файл
        with open(temp_filename, "r", encoding="utf-8") as f:
            content = f.read()
            assert "test_func error: ValueError" in content
            assert "Inputs: (1, 2), {}" in content

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_with_kwargs(capsys):
    """Тестируем логирование с ключевыми аргументами."""

    @log()
    def test_func(x, y=0):
        return x + y

    # Вызываем функцию с ключевыми аргументами
    result = test_func(1, y=2)

    # Проверяем результат
    assert result == 3

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "test_func ok" in captured.out


def test_log_with_kwargs_error(capsys):
    """Тестируем логирование ошибок с ключевыми аргументами."""

    @log()
    def test_func(x, y=0):
        raise ValueError("Test error")

    # Проверяем, что исключение пробрасывается
    with pytest.raises(ValueError):
        test_func(1, y=2)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "test_func error: ValueError" in captured.out
    assert "Inputs: (1,), {'y': 2}" in captured.out


def test_log_function_name(capsys):
    """Тестируем, что декоратор сохраняет имя функции."""

    @log()
    def some_function():
        return "result"

    # Проверяем, что имя функции сохранено
    assert some_function.__name__ == "some_function"

    # Вызываем функцию
    result = some_function()

    # Проверяем результат
    assert result == "result"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "some_function ok" in captured.out
