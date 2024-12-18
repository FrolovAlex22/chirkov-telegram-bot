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
        "Мероприятия в Чирковъ": "event_user",
        "Мастерская керамики 4 чтихии": "ceramics_user",
        "Парк виртуальной реальности": "vr_user",
        "Арт-галерея": "art_gallery_user",
    },
    sizes=(1, ),
)


# CERAMICS MENU
CERAMICS_MENU = get_callback_btns(
    btns={
        "Предстоящие мероприятия": "cearamics_event_user",
        "Наши работы в продажи": "ceramics_works_of_masters",
        "Записаться на урок": "ceramics_lesson_user",
        "Вернуться в главное меню Чирковъ": "main_menu",
    },
    sizes=(1, ),
)


CERAMICS_MASTERS_MENU = get_callback_btns(
    btns={
        "Мастер 1": "back_to_main_menu",
        "Мастер 2": "back_to_main_menu",
        "Вернуться в главное меню керамики": "ceramics_user",
    },
    sizes=(1, ),
)


CERAMICS_LESSON_MENU = get_callback_btns(
    btns={
        "Урок 1": "back_to_main_menu",
        "Урок 2": "back_to_main_menu",
        "Вернуться в главное меню керамики": "ceramics_user",
    },
    sizes=(1, ),
)


# VIRTUAL REALITY MENU
VR_MENU = get_callback_btns(
    btns={
        "Подробнее про услугу": "vr_info",
        "Оставить заявку на посещение": "vr_application",
        "Вернуться в главное меню Чирковъ": "main_menu",
    },
    sizes=(1, ),
)


VR_INFO = get_callback_btns(
    btns={
        "Кастомная клавиатура с ссылкой на вк": "vr_info_vk",
        "Вернуться в главное меню VR": "vr_user",
    },
    sizes=(1, ),
)


# ART GALLERY
ART_INFO = get_callback_btns(
    btns={
        "Картины с выставки Чирковъ": "art_today",
        "Работы Бирских мастеров": "atr_birsk_masters",
        "Вернуться в главное меню Чирковъ": "main_menu",
    },
    sizes=(1, ),
)


ART_TODAY = get_callback_btns(
    btns={
        "Пагинация картин": "art_gallery_user",
        "Вернуться в меню арт-галереи": "art_gallery_user",
    },
    sizes=(1, ),
)


ART_BIRSK_MASTERS = get_callback_btns(
    btns={
        "Выгрузка мастеров из БД": "art_gallery_user",
        "Вернуться в меню арт-галереи": "art_gallery_user",
    },
    sizes=(1, ),
)


# EVENT MENU
EVENT_KB = get_callback_btns(
    btns={
        "Список мероприятий": "main_menu",
        "Вернуться в главное меню": "main_menu",
    },
    sizes=(1, ),
)
