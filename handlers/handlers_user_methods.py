from datetime import datetime
from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import (
    orm_get_authors_by_category, orm_get_banner, orm_get_category_by_name,
    orm_get_event_by_id, orm_get_event_by_year,
    orm_get_events_by_category_and_date, orm_get_product_by_id,
    orm_get_products_by_author_and_category, orm_get_products_by_category,
    orm_get_products_by_type_and_category, orm_get_upcoming_events
)
from keyboards.inline import (
    CATEGORY_MENU_NAME_DICT,
    EventCallBack,
    ProductCallBack,
    choise_year_kb,
    get_products_btns,
    get_user_art_galery_btns,
    get_user_art_galery_lvl1_btns,
    get_user_ceramic_btns,
    get_user_event_list_btns,
    get_user_events_btns,
    get_user_main_btns,
    get_user_product_list_back_btns,
    get_user_product_list_btns,
    get_user_vr_btns,
    user_event_by_date_btns,
    user_event_id_back_btns,
    user_upcoming_events_btns
)
from keyboards.my_calendar import CalendarMarkup
from keyboards.reply import get_contact_btns, get_keyboard
from lexicon.lexicon import CATEGORY_MENU_NAME_REVERSE_DICT, LEXICON_ART_GALLERY, LEXICON_EVENT, LEXICON_PRODUCT_SERVICE
from utils.paginator import Paginator


############################ MAIN MENU METHODS ##########################
async def main_menu(session, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_main_btns()

    return image, kbds


async def events(session, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_events_btns(sizes=(1, ))

    return image, kbds


async def ceramic(session, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_ceramic_btns()

    return image, kbds


async def vr(session, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_vr_btns()

    return image, kbds


async def art_galery(session, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_art_galery_btns()

    return image, kbds


async def art_galery_handlers(session, callback_text, category):
    text = LEXICON_ART_GALLERY["art_birsk_masters"]
    category_id = await orm_get_category_by_name(session, category)
    authors = await orm_get_authors_by_category(session, category_id.id)
    kbds = get_user_art_galery_lvl1_btns(authors, (1, ))

    return text, kbds


async def get_menu_content(
    session: AsyncSession,
    menu_name: str,
):
    if menu_name == "main":
        return await main_menu(session, menu_name)
    elif menu_name == "events":
        return await events(session, menu_name)
    elif menu_name == "ceramic":
        return await ceramic(session, menu_name)
    elif menu_name == "vr":
        return await vr(session, menu_name)
    elif menu_name == "art_galery":
        return await art_galery(session, menu_name)


############################ PRODUCT METHODS ##########################
async def get_product_content(
    session: AsyncSession,
    category: str,
    type: str,
):
    category_id = await orm_get_category_by_name(session, category)
    products = await orm_get_products_by_type_and_category(
        session, category_id.id, type
    )

    text = LEXICON_PRODUCT_SERVICE[category]
    kbds = get_user_product_list_btns(products, category, (1, ))

    return text, kbds


async def get_user_service_info(
    session: AsyncSession,
    category: str,
    product_id: int
):
    product = await orm_get_product_by_id(session, product_id)

    text = (
        f"<b>{product.name}</b>\n\n<b>Описание:</b>\n{product.description}"
        f"\n\n<b>Цена:</b> {product.price}"
    )

    image = InputMediaPhoto(media=product.image, caption=text)

    kb = get_user_product_list_back_btns(
        category,
        product_id,
        (2, )
    )

    return image, kb


async def get_user_service_application_calendar():

    text = "<b>Выберите дату посещения:</b>"

    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year

    kb = CalendarMarkup(current_month, current_year).build.kb

    return text, kb


async def set_user_phone_number_application():

    text = "Чтобы мы получили ваши контакты, пожалуйста, отправте номер телефона"

    kb = get_contact_btns()

    return text, kb


def pages(paginator: Paginator):
    """Кнопки для пагинации"""
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns


async def products(
        session: AsyncSession, page: int, category: str, author_id: str | None
    ):
    """Получение списка продуктов категории домашний уход"""
    category_id = await orm_get_category_by_name(session, category)
    if author_id:
        products = await orm_get_products_by_author_and_category(
            session, category_id.id, int(author_id)
        )

    else:
        products = await orm_get_products_by_category(
            session, category=category_id.id
        )
    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=product.image,
        caption=f"<strong>{product.name}"
                f"</strong>\n{product.description}\n"
                f"Стоимость: {round(product.price, 2)}\n"
                f"<strong>Товар {paginator.page}"
                f" из {paginator.pages}</strong>",
    )

    pagination_btns = pages(paginator)

    kbds = get_products_btns(
        category=category,
        page=page,
        author_id=author_id,
        product_id=str(product.id),
        name=product.name,
        price=str(product.price),
        pagination_btns=pagination_btns,
    )

    return image, kbds


############################ EVENT METHODS ##########################

async def get_event_content_with_category(
    session: AsyncSession,
    callback_data: EventCallBack,
):
    if callback_data.category:
        banner = await orm_get_banner(
            session,
            page=CATEGORY_MENU_NAME_DICT[callback_data.category]
        )
    else:
        banner = await orm_get_banner(session, "main")
    category = await orm_get_category_by_name(
        session, callback_data.category
    )
    events = await orm_get_events_by_category_and_date(
        session, category.id
    )
    if not events:
        text = LEXICON_EVENT["пустой список"]
    else:
        text = LEXICON_EVENT[callback_data.category]
    for num, event in enumerate(events, start=1):
        text += (
            f"\n\n<b>{num} - {event.title}. Дата проведения: "
            f"{event.date.strftime('%d.%m.%Y')}</b>\n\n"
        )
    kbds = get_user_event_list_btns(
        events, callback_data.category, callback_data.level, (1, )
    )
    image = InputMediaPhoto(media=banner.image, caption=text)

    return image, kbds


async def get_event_by_id(
    session: AsyncSession,
    callback_data: EventCallBack,
):
    event = await orm_get_event_by_id(session, callback_data.event_id)

    text = (
        f"<b>{event.title}</b>\n\n<b>Описание:</b>\n{event.description}"
        f"\n\n<b>Дата проведения:</b> {event.date.strftime('%d.%m.%Y')}"
        f"\nКатегория: {event.categorys.name}"
        f"\nАвтор: {event.authors.name}"
    )

    image = InputMediaPhoto(media=event.image, caption=text)

    kb = user_event_id_back_btns(callback_data.category, (2, ))

    return image, kb


async def get_event_by_year(
    session: AsyncSession,
    callback_data: EventCallBack,
):
    str_date = f"01.01.{callback_data.year}"
    date = datetime.strptime(str_date, '%d.%m.%Y')
    events = await orm_get_event_by_year(session, date)
    text = f"{LEXICON_EVENT["выбор года"]}{date.year} году:"
    for num, event in enumerate(events, start=1):
        text += (
            f"\n<b>{num} - {event.title}. Дата : "
            f"{event.date.strftime('%d.%m.%Y')}</b>"
        )
    banner = await orm_get_banner(session, "events")
    image = InputMediaPhoto(media=banner.image, caption=text)

    kb = user_event_by_date_btns(events, (1, ))

    return image, kb


async def choise_year(
    session: AsyncSession,
):
    start_year = datetime.strptime("01.01.2022", '%d.%m.%Y').year
    year = datetime.today().year

    years = [i for i in range(int(start_year), int(year) + 1)]
    text = "Выберите год:"
    banner = await orm_get_banner(session, "events")
    image = InputMediaPhoto(media=banner.image, caption=text)

    kb = choise_year_kb(years, (1, ))

    return image, kb




async def get_upcoming_events(
    session: AsyncSession,
):
    events = await orm_get_upcoming_events(session)
    text = LEXICON_EVENT["предстоящие мероприятия"]
    for num, event in enumerate(events, start=1):
        text += (
            f"\n<b>{num} - {event.title}. Дата : "
            f"{event.date.strftime('%d.%m.%Y')}</b>"
        )
    banner = await orm_get_banner(session, "events")
    image = InputMediaPhoto(media=banner.image, caption=text)

    kb = user_upcoming_events_btns(events, (1, ))

    return image, kb


async def get_event_content(
    session: AsyncSession,
    callback_data: EventCallBack,
):
    if not callback_data.event_id:
        if callback_data.level == 0:
            result = await get_event_content_with_category(session, callback_data)
            return result
        if callback_data.level == 1:
            result = await choise_year(session,)
            return result

        if callback_data.level == 2:
            if callback_data.year:
                result = await get_event_by_year(session, callback_data)
                return result
            else:
                result = await get_upcoming_events(session)
                return result


    else:
        result = await get_event_by_id(session, callback_data)
        return result
