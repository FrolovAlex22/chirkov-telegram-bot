from aiogram.types import InputMediaPhoto, CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import orm_get_banner
from keyboards.admin_kb import ADMIN_MENU_SELECTION_AUTHOR
from keyboards.inline import get_products_btns, get_user_art_galery_btns, get_user_ceramic_btns, get_user_events_btns, get_user_main_btns, get_user_vr_btns
from lexicon.lexicon import LEXICON_ADMIN
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


############################ ADMIN METHODS ##########################

async def test_method(
        state: FSMContext, session: AsyncSession, callback: CallbackQuery):
    await state.clear()
    await callback.answer()
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_ADMIN["admin_author_choise"],
            reply_markup=ADMIN_MENU_SELECTION_AUTHOR
        )
        return
    banner = await orm_get_banner(session, page="admin")
    await callback.message.answer_photo(
        photo=banner.image,
        caption=LEXICON_ADMIN["admin_author_choise"],
        reply_markup=ADMIN_MENU_SELECTION_AUTHOR
    )
    return
