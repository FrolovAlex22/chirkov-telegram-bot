from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import orm_get_banner, orm_get_ceramic_work, orm_get_ceramic_works
from keyboards.inline import get_products_btns, get_user_art_galery_btns, get_user_ceramic_btns, get_user_events_btns, get_user_main_btns, get_user_vr_btns
from utils.paginator import Paginator


def pages(paginator: Paginator):
    """Кнопки для пагинации"""
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns


async def products(session, page):
    """Получение списка работ из керамики"""
    works = await orm_get_ceramic_works(session=session)

    paginator = Paginator(works, page=page)
    work = paginator.get_page()[0]

    # image = InputMediaPhoto(
    #     media=product.photo,
    #     caption=f"<strong>{product.title}"
    #             f"</strong>\n{product.description}\n"
    #             f"Стоимость: {round(product.price, 2)}\n"
    #             f"<strong>Товар {paginator.page}"
    #             f" из {paginator.pages}</strong>",
    # )
    text = f"{work.title}"


    pagination_btns = pages(paginator)

    kbds = get_products_btns(
        # level=level,
        # category=category,
        page=page,
        pagination_btns=pagination_btns,
        # product_id=work.id,
    )

    return text, kbds

# ------------------------------------------------------------------------------
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


# async def catalog(session, level, menu_name):  !!!!!!!!!!!!!!!ШПАРГАЛКА
#     banner = await orm_get_banner(session, menu_name)
#     image = InputMediaPhoto(media=banner.image, caption=banner.description)

#     categories = await orm_get_categories(session)
#     kbds = get_user_catalog_btns(level=level, categories=categories)

#     return image, kbds


async def get_menu_content(
    session: AsyncSession,
    # level: int,
    menu_name: str,
    # category: int | None = None,
    # page: int | None = None,
    # product_id: int | None = None,
    # user_id: int | None = None,
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