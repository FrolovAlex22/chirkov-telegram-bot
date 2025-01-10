from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import orm_get_banner, orm_get_category_by_name, orm_get_product_by_id, orm_get_products_by_category, orm_get_products_by_type_and_category
from keyboards.inline import (
    get_products_btns,
    get_user_art_galery_btns,
    get_user_ceramic_btns,
    get_user_events_btns,
    get_user_main_btns,
    get_user_product_list_back_btns,
    get_user_product_list_btns,
    get_user_vr_btns
)
from lexicon.lexicon import LEXICON_PRODUCT_SERVICE
from utils.paginator import Paginator


############################ USER METHODS ##########################
async def main_menu(session, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_main_btns()

    return image, kbds


async def events(session, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    kbds = get_user_events_btns()

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
    print(category_id.id, type)
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

    kb = get_user_product_list_back_btns(category, (2, ))

    return image, kb


def pages(paginator: Paginator):
    """Кнопки для пагинации"""
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns


async def products(session: AsyncSession, page: int, category: str):
    """Получение списка продуктов категории домашний уход"""
    category_id = await orm_get_category_by_name(session, category)
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
        pagination_btns=pagination_btns,
        # product_id=product.id,
    )

    return image, kbds
