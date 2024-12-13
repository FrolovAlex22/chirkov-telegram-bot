from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)
) -> InlineKeyboardBuilder:

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():

        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


# MAIN MENU
MAIN_MENU = get_callback_btns(
    btns={
        "first": "first",
        "second": "second",
    },
    sizes=(2, ),
)
