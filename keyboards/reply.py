from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_keyboard(
    *btns: str | tuple[str | KeyboardButton] | KeyboardButton,
    placeholder: str = None,
    request_contact: int = None,
    # request_location: int = None,
    sizes: tuple[int] = (2,),
):
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):

        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        # elif request_location and request_location == index:
        #     keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)


def get_contact_btns():
    kb_builder = ReplyKeyboardBuilder()
    contact_btn = KeyboardButton(
        text='Отправить телефон',
        request_contact=True
    )
    kb_builder.row(contact_btn, width=1)

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

ADMIN_CHOISE_CATEGORY = get_keyboard(
    "Арт галерея",
    "Мастерская керамики",
    "Виртуальная реальность",
    "Мероприятия",
    sizes=(1,)
)