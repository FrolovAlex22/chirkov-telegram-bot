from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.models import Author, Event, Product


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
    level: int = 0


class ProductCallBack(CallbackData, prefix="product"):
    category: str
    pr_type: str = "PRODUCT"
    product_id: int | None = None
    author_id: int | None = None
    page: int = 1
    application: bool = False


class EventCallBack(CallbackData, prefix="event"):
    category: str
    event_id: int | None = None
    level: int = 0
    year: int | None = None


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
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="предстоящие события в Чирковъ",
                callback_data=EventCallBack(
                    category="Мероприятия",
                    level=2
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="Выбор событий по годам",
                callback_data=EventCallBack(
                    category="Мероприятия",
                    level=1
                ).pack()))

    keyboard.add(InlineKeyboardButton(text="Назад",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


def choise_year_kb(
        years: list[int],
        sizes: tuple[int] = (2,)
    ):
    keyboard = InlineKeyboardBuilder()

    for year in years:
        keyboard.add(InlineKeyboardButton(text=str(year),
                callback_data=EventCallBack(
                    category="Мероприятия",
                    level=2,
                    year=year
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="Назад",
                callback_data=MenuCallBack(menu_name="events").pack()))
    keyboard.add(InlineKeyboardButton(text="В главное меню",
                callback_data=MenuCallBack(menu_name="main").pack()))

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

    keyboard.add(
        InlineKeyboardButton(
            text="Посмотреть работы наших художников",
            callback_data=MenuCallBack(
                menu_name="art_galery",
                level=1
            ).pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="Предстоящие мероприятия",
            callback_data=EventCallBack(
                category="Арт галерея",
            ).pack()
        )
    )
    keyboard.add(InlineKeyboardButton(text="В главное меню",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_art_galery_lvl1_btns(
        authors: list[Author], sizes: tuple[int] = (2,)
    ):
    keyboard = InlineKeyboardBuilder()

    for num, a in enumerate(authors, start=1):
        text = f"{num}. {a.name}"
        keyboard.add(InlineKeyboardButton(text=text,
                callback_data=ProductCallBack(
                    author_id=str(a.id),
                    category="Арт галерея",
                    pr_type="PRODUCT"
                ).pack()))

    keyboard.add(InlineKeyboardButton(text="В меню арт галереи",
                callback_data=MenuCallBack(menu_name="art_galery").pack()))

    keyboard.add(InlineKeyboardButton(text="В главное меню",
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


def get_user_product_list_back_btns(
        category: str, product_id: int, sizes: tuple[int] = (2,)
    ):

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Оставить заявку",
                callback_data=ProductCallBack(
                    pr_type="SERVICE",
                    category=category,
                    product_id=product_id,
                    application=True
                ).pack()))

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
    author_id: str | None,
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
                    author_id=author_id,
                    page=page + 1).pack()))

        elif menu_name == "previous":
            row.append(InlineKeyboardButton(
                text=text,
                callback_data=ProductCallBack(
                    category=category,
                    author_id=author_id,
                    page=page - 1).pack()))

    return keyboard.row(*row).as_markup()


######################## Работа с событиями ##################################
def get_user_event_list_btns(
        events: list[Event],
        category: str | None,
        level: int,
        sizes: tuple[int] = (2,)
    ):
    keyboard = InlineKeyboardBuilder()

    for num, e in enumerate(events, start=1):
        text = f"{num}. {e.title}"
        keyboard.add(InlineKeyboardButton(text=text,
                callback_data=EventCallBack(
                    event_id=str(e.id),
                    category=category,
                    level=level
                ).pack()))

    if category is not None:
        back_path = CATEGORY_MENU_NAME_DICT[category]
    else:
        back_path = "main"

    keyboard.add(
        InlineKeyboardButton(
            text="Верунться назад",
            callback_data=MenuCallBack(menu_name=back_path).pack()
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text="В главное меню",
            callback_data=MenuCallBack(menu_name="main").pack()
            )
        )

    return keyboard.adjust(*sizes).as_markup()


def user_event_id_back_btns(category: str, sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="Верунться назад",
                callback_data=MenuCallBack(
                    menu_name=CATEGORY_MENU_NAME_DICT[category]
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="В главное меню",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


def user_event_by_date_btns(
        events: list[Event],
        sizes: tuple[int] = (2,)
    ):

    keyboard = InlineKeyboardBuilder()
    for n, e in enumerate(events, start=1):
        text = f"{n}. {e.title} Дата проведения: {e.date.strftime('%d.%m.%Y')}"
        keyboard.add(InlineKeyboardButton(text=text,
                callback_data=EventCallBack(
                    event_id=str(e.id),
                    category="Мероприятия",
                    level=1
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="Верунться назад",
                callback_data=MenuCallBack(
                    menu_name=CATEGORY_MENU_NAME_DICT["Мероприятия"]
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="В главное меню",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()


def user_upcoming_events_btns(
        events: list[Event],
        sizes: tuple[int] = (2,)
    ):

    keyboard = InlineKeyboardBuilder()
    for n, e in enumerate(events, start=1):
        text = f"{n}. {e.title} Дата: {e.date.strftime('%d.%m.%Y')}"
        keyboard.add(InlineKeyboardButton(text=text,
                callback_data=EventCallBack(
                    event_id=str(e.id),
                    category="Мероприятия",
                    level=0
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="Верунться назад",
                callback_data=MenuCallBack(
                    menu_name=CATEGORY_MENU_NAME_DICT["Мероприятия"]
                ).pack()))
    keyboard.add(InlineKeyboardButton(text="В главное меню",
                callback_data=MenuCallBack(menu_name="main").pack()))

    return keyboard.adjust(*sizes).as_markup()
