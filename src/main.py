import os
import sys
from typing import List, Dict, Any

# Добавляем путь к src для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.file_reader import read_csv_file, read_excel_file, convert_transaction_format
from src.processing import filter_by_state, sort_by_date, process_bank_search, filter_by_currency_code
from src.utils import load_json_data
from src.widget import get_date, mask_account_card


class BankTransactionProcessor:
    """Класс для обработки банковских транзакций."""

    def __init__(self):
        self.transactions: List[Dict[str, Any]] = []
        self.filtered_transactions: List[Dict[str, Any]] = []

    def load_transactions_from_json(self, file_path: str) -> bool:
        """Загружает транзакции из JSON-файла."""
        print("Для обработки выбран JSON-файл.")
        self.transactions = load_json_data(file_path)
        return bool(self.transactions)

    def load_transactions_from_csv(self, file_path: str) -> bool:
        """Загружает транзакции из CSV-файла."""
        print("Для обработки выбран CSV-файл.")
        raw_transactions = read_csv_file(file_path)
        self.transactions = convert_transaction_format(raw_transactions)
        return bool(self.transactions)

    def load_transactions_from_excel(self, file_path: str) -> bool:
        """Загружает транзакции из Excel-файла."""
        print("Для обработки выбран XLSX-файл.")
        raw_transactions = read_excel_file(file_path)
        self.transactions = convert_transaction_format(raw_transactions)
        return bool(self.transactions)

    def filter_by_status(self) -> bool:
        """Фильтрует транзакции по статусу с повторным запросом при ошибке."""
        valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

        while True:
            print("Введите статус, по которому необходимо выполнить фильтрацию.")
            print(f"Доступные для фильтрации статусы: {', '.join(valid_statuses)}")

            user_input = input("> ").strip().upper()

            if user_input in valid_statuses:
                self.filtered_transactions = filter_by_state(self.transactions, user_input)
                print(f"Операции отфильтрованы по статусу \"{user_input}\"")
                return True
            else:
                print(f"Статус операции \"{user_input}\" недоступен.")

    def ask_yes_no_question(self, question: str) -> bool:
        """Задает вопрос Да/Нет и возвращает булево значение."""
        while True:
            print(question)
            user_input = input("> ").strip().lower()

            if user_input in ["да", "д", "yes", "y"]:
                return True
            elif user_input in ["нет", "н", "no", "n"]:
                return False
            else:
                print("Пожалуйста, ответьте 'Да' или 'Нет'.")

    def ask_sort_direction(self) -> bool:
        """Спрашивает направление сортировки."""
        while True:
            print("Отсортировать по возрастанию или по убыванию?")
            user_input = input("> ").strip().lower()

            if user_input in ["по возрастанию", "возрастание", "asc", "ascending"]:
                return False  # reverse=False для возрастания
            elif user_input in ["по убыванию", "убывание", "desc", "descending"]:
                return True  # reverse=True для убывания
            else:
                print("Пожалуйста, укажите 'по возрастанию' или 'по убыванию'.")

    def apply_filters(self) -> None:
        """Применяет все фильтры к транзакциям."""
        # Копируем отфильтрованные по статусу транзакции
        working_transactions = self.filtered_transactions.copy()

        # Сортировка по дате
        if self.ask_yes_no_question("Отсортировать операции по дате? Да/Нет"):
            reverse = self.ask_sort_direction()
            working_transactions = sort_by_date(working_transactions, reverse)

        # Фильтрация по валюте
        if self.ask_yes_no_question("Выводить только рублевые транзакции? Да/Нет"):
            working_transactions = filter_by_currency_code(working_transactions, "RUB")

        # Фильтрация по слову в описании
        if self.ask_yes_no_question("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
            print("Введите слово для поиска в описании:")
            search_word = input("> ").strip()
            if search_word:
                working_transactions = process_bank_search(working_transactions, search_word)

        self.filtered_transactions = working_transactions

    def format_transaction(self, transaction: Dict[str, Any]) -> str:
        """Форматирует транзакцию для вывода."""
        date_str = get_date(transaction.get("date", ""))
        description = transaction.get("description", "")

        # Форматируем отправителя и получателя
        from_account = mask_account_card(transaction.get("from", "")) if transaction.get("from") else ""
        to_account = mask_account_card(transaction.get("to", "")) if transaction.get("to") else ""

        # Получаем сумму и валюту
        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "")
        currency = operation_amount.get("currency", {})
        currency_name = currency.get("name", "")
        currency_code = currency.get("code", "")

        # Формируем строку суммы
        amount_str = f"{amount} {currency_name} ({currency_code})" if currency_name else f"{amount} {currency_code}"

        # Собираем результат
        result = f"{date_str} {description}\n"

        if from_account and to_account:
            result += f"{from_account} -> {to_account}\n"
        elif to_account:
            result += f"{to_account}\n"

        result += f"Сумма: {amount_str}\n"

        return result

    def print_transactions(self) -> None:
        """Выводит отфильтрованные транзакции."""
        if not self.filtered_transactions:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            return

        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(self.filtered_transactions)}\n")

        for i, transaction in enumerate(self.filtered_transactions, 1):
            print(f"{i}. {self.format_transaction(transaction)}")

    def run(self) -> None:
        """Основной метод запуска программы."""
        print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        while True:
            choice = input("> ").strip()

            file_paths = {
                "1": ("data/operations.json", self.load_transactions_from_json),
                "2": ("data/transactions.csv", self.load_transactions_from_csv),
                "3": ("data/transactions_excel.xlsx", self.load_transactions_from_excel)
            }

            if choice in file_paths:
                file_path, loader = file_paths[choice]
                if loader(file_path):
                    break
                else:
                    print(f"Не удалось загрузить данные из файла {file_path}. Попробуйте снова.")
            else:
                print("Неверный выбор. Пожалуйста, введите 1, 2 или 3.")

        # Фильтрация по статусу
        self.filter_by_status()

        # Применение дополнительных фильтров
        self.apply_filters()

        # Вывод результатов
        self.print_transactions()


def main():
    """Точка входа в программу."""
    try:
        processor = BankTransactionProcessor()
        processor.run()
    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
