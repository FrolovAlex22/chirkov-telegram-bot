from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import orm_get_banner, orm_get_category_by_name, orm_get_product_by_id, orm_get_products_by_type_and_category
from keyboards.inline import (
    get_user_art_galery_btns,
    get_user_ceramic_btns,
    get_user_events_btns,
    get_user_main_btns,
    get_user_product_list_back_btns,
    get_user_product_list_btns,
    get_user_vr_btns
)
from lexicon.lexicon import LEXICON_PRODUCT_SERVICE


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
