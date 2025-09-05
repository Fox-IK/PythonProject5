# Проект обработки банковских операций

## Цель проекта
Обработка и анализ банковских транзакций с фильтрацией по статусу и сортировкой по дате.

## Установка
1. Склонируйте репозиторий:
```bash
git clone https://github.com/ваш-аккаунт/ваш-репозиторий.git
```
## Проверка по тестам
1. Установить pytest командой
```bash
pip install pytest coverage
```
2. Скопировать и вставить в командную строку
```bash
pytest tests
```

## Модуль generators

Модуль предоставляет инструменты для работы с большими объемами данных через генераторы.

### Функции

#### `filter_by_currency(transactions, currency_code)`
Фильтрует транзакции по валюте операции.

Пример:
```bash
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(transaction["id"], transaction["operationAmount"]["amount"])
```
## Генерация отчета покрытия тестами

Для генерации отчета о покрытии тестами выполните:

```bash
pytest tests/test_generators.py --cov=src.generators --cov-report=html