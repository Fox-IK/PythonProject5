def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты в формате XXXX XX** **** XXXX"""
    cleaned = card_number.replace(" ", "")
    if len(cleaned) != 16 or not cleaned.isdigit():
        raise ValueError("Invalid card number format")

    return f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета в формате **XXXX"""
    cleaned = account_number.replace(" ", "")
    if len(cleaned) < 4 or not cleaned.isdigit():
        raise ValueError("Invalid account number format")

    return f"**{cleaned[-4:]}"
