from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Product


CATEGORY_MENU_NAME_DICT = {
    "Мастерская керамики": "ceramic",
    "Виртуальная реальность": "vr",
    "Арт галерея": "art_galery",
    "Мероприятия": "events"
}


def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)
) -> InlineKeyboardBuilder:

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():

        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


class MenuCallBack(CallbackData, prefix="menu"):
    menu_name: str


class ProductCallBack(CallbackData, prefix="product"):
    category: str
    pr_type: str = "PRODUCT"
    product_id: int | None = None
    author_id: int | None = None
    page: int = 1


class EventCallBack(CallbackData, prefix="event"):
    category: str
    event_id: int | None = None


###################### Главное меню и основные разделы #########################
def get_user_main_btns(*, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Мероприятия в Чирковъ": "events",
        "Мастерская керамики 4 чтихии 🏺": "ceramic",
        "VR club 1663": "vr",
        "Художественная галерея": "art_galery",
    }
    for text, menu_name in btns.items():
        if menu_name == "events":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))
        elif menu_name == "ceramic":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))
        elif menu_name == "vr":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))
        elif menu_name == "art_galery":
            keyboard.add(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_ceramic_btns(*, sizes: tuple[int] = (1, )):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Запись",
            callback_data=ProductCallBack(
                category="Мастерская керамики",
                pr_type="SERVICE"
            ).pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Изделия керамики в продаже",
            callback_data=ProductCallBack(
                category="Мастерская керамики",
                pr_type="PRODUCT"
            ).pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Предстоящие мероприятия",
            callback_data=EventCallBack(
                category="Мастерская керамики",
            ).pack()
        )
    )
    keyboard.add(InlineKeyboardButton(text="Назад",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_events_btns(*, sizes: tuple[int] = (2,)):
    # Переделать на пагинацию, с продуктами категории события!!!!!!!!!!!!!!!!!!
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Назад",
                callback_data=MenuCallBack(menu_name="main").pack()))
    keyboard.add(InlineKeyboardButton(text="События 🛒",
                callback_data=MenuCallBack(menu_name="main").pack()))

    # for c in categories:
    #     keyboard.add(InlineKeyboardButton(text=c.name,
    #             callback_data=MenuCallBack(level=level+1, menu_name=c.name, category=c.id).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_vr_btns(*, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text="Запись на посещение",
            callback_data=ProductCallBack(
                category="Виртуальная реальность",
                pr_type="SERVICE"
            ).pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Назад",
            callback_data=MenuCallBack(menu_name="main").pack()
        )
    )

    return keyboard.adjust(*sizes).as_markup()


def get_user_art_galery_btns(*, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Назад",
                callback_data=MenuCallBack(menu_name="main").pack()))
    keyboard.add(InlineKeyboardButton(text="art_galery 🛒",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


######################## Работа с продуктами ##################################
def get_user_product_list_btns(
        products: list[Product],
        category: str,
        sizes: tuple[int] = (2,)
    ):

    keyboard = InlineKeyboardBuilder()

    for num, p in enumerate(products, start=1):
        text = f"{num}. {p.name}. Цена - {p.price} руб."
        keyboard.add(InlineKeyboardButton(text=text,
                callback_data=ProductCallBack(
                    product_id=str(p.id),
                    pr_type="SERVICE",
                    category=category
                ).pack()))

    keyboard.add(
        InlineKeyboardButton(
            text="Верунться назад",
            callback_data=MenuCallBack(
                menu_name=CATEGORY_MENU_NAME_DICT[category]
            ).pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="В главное меню",
            callback_data=MenuCallBack(menu_name="main").pack()
            )
        )

    return keyboard.adjust(*sizes).as_markup()


def get_user_product_list_back_btns(category: str, sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Верунться назад",
                callback_data=MenuCallBack(
                    menu_name=CATEGORY_MENU_NAME_DICT[category]
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="В главное меню",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_products_btns(
    *,
    page: int,
    category: str,
    pagination_btns: dict,
    sizes: tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text="В главное меню", callback_data="main_menu")
    )

    keyboard.adjust(*sizes)

    row = []
    for text, menu_name in pagination_btns.items():
        if menu_name == "next":
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=ProductCallBack(
                    category=category,
                    page=page + 1).pack()))

        elif menu_name == "previous":
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=ProductCallBack(
                    category=category,
                    page=page - 1).pack()))

    return keyboard.row(*row).as_markup()
