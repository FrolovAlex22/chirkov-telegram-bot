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

# ----------------------ОТСЕЧКА-------------------------------------
class MenuCallBack(CallbackData, prefix="menu"):
    # level: int
    menu_name: str
    # category: int | None = None
    # page: int = 1
    # product_id: int | None = None



def get_user_main_btns(*, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Мероприятия в Чирковъ": "events",
        "Мастерская керамики 4 чтихии 🏺": "ceramic",
        "VR club 1663": "vr",
        "Художественная галерея": "art_galery",
    }
    for text, menu_name in btns.items():
        if menu_name == 'events':
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))
        elif menu_name == 'ceramic':
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))
        elif menu_name == 'vr':
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))
        elif menu_name == 'art_galery':
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_events_btns(*, sizes: tuple[int] = (2,)):
    # Переделать на пагинацию, с продуктами категории события!!!!!!!!!!!!!!!!!!
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallBack(menu_name='main').pack()))
    keyboard.add(InlineKeyboardButton(text='События 🛒',
                callback_data=MenuCallBack(menu_name='main').pack()))

    # for c in categories:
    #     keyboard.add(InlineKeyboardButton(text=c.name,
    #             callback_data=MenuCallBack(level=level+1, menu_name=c.name, category=c.id).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_ceramic_btns(*, sizes: tuple[int] = (2,)):
    # Переделать на пагинацию, с продуктами категории события!!!!!!!!!!!!!!!!!!
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallBack(menu_name='main').pack()))
    keyboard.add(InlineKeyboardButton(text='Керамика 🛒',
                callback_data=MenuCallBack(menu_name='main').pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_vr_btns(*, sizes: tuple[int] = (2,)):
    # Переделать на пагинацию, с продуктами категории события!!!!!!!!!!!!!!!!!!
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallBack(menu_name='main').pack()))
    keyboard.add(InlineKeyboardButton(text='1663 🛒',
                callback_data=MenuCallBack(menu_name='main').pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_art_galery_btns(*, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallBack(menu_name='main').pack()))
    keyboard.add(InlineKeyboardButton(text='art_galery 🛒',
                callback_data=MenuCallBack(menu_name='main').pack()))

    return keyboard.adjust(*sizes).as_markup()

# _____________________________________________________________________________

class ProductCallBack(CallbackData, prefix="ceramic_works"):
    page: int = 1
    product_id: int | None = None


def get_products_btns(
    *,
    page: int,
    pagination_btns: dict,
    sizes: tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text='В главное меню', callback_data='main_menu')
    )

    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=ProductCallBack(
                    page=page + 1).pack()))

        elif menu_name == "previous":
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=ProductCallBack(

                        page=page - 1).pack()))

    return keyboard.row(*row).as_markup()


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
        "Наши работы в продаже": ProductCallBack().pack(),
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
