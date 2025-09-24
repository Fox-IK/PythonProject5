from masks import get_mask_account, get_mask_card_number
from src.file_reader import read_csv_file, read_excel_file
from widget import get_date, mask_account_card

print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361

print(get_mask_account("73654108430135874305"))  # **4305

print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361

print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024

# Чтение CSV файла
csv_transactions = read_csv_file('data/transactions.csv')
print(f"Загружено {len(csv_transactions)} транзакций из CSV")

# Чтение Excel файла
excel_transactions = read_excel_file('data/transactions_excel.xlsx')
print(f"Загружено {len(excel_transactions)} транзакций из Excel")
