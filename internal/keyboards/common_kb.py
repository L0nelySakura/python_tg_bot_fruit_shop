from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> InlineKeyboardMarkup:
    """
    Главное меню с двумя кнопками: Директор и Торговый представитель
    """
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Директор", callback_data="director")],
        [InlineKeyboardButton(text="Торговый представитель", callback_data="representative")]
    ])
    return kb
