

def test_load_json_data_directory_instead_of_file():
    """Тестируем загрузку, когда путь ведет к директории, а не файлу."""
    # Создаем временную директорию
    with tempfile.TemporaryDirectory() as temp_dir:
        result = load_json_data(temp_dir)
        assert result == []


def test_load_json_data_permission_error(monkeypatch):
    """Тестируем обработку ошибки прав доступа."""

    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)

    with tempfile.NamedTemporaryFile() as f:
        result = load_json_data(f.name)
        assert result == []
