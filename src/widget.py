from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_str: str) -> str :
    words = input_str.split()
    # Если в строке меньше двух частей, возвращаем исходную строку
    if len(words) < 2 :
        return input_str

    # Извлечение номера (последнее слово) и названия (все слова, кроме последнего)
    number_str = words[-1]
    name = " ".join(words[:-1])

    # Определение типа и маскировка
    if name == "Счет" :
        masked_number = get_mask_account(number_str)
    else :
        masked_number = get_mask_card_number(number_str)

    return f"{name} {masked_number}"


def get_date(date_str: str) -> str :
    """Преобразует дату из формата ISO в формат DD.MM.YYYY."""
    try :
        date_part = date_str.split("T")[0]
        year , month , day = date_part.split("-")
        return f"{day}.{month}.{year}"
    except (IndexError , ValueError) :
        return date_str
