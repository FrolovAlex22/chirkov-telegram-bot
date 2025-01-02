from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import orm_get_banner
from handlers.handlers_user_methods import get_menu_content
from keyboards.inline import MAIN_MENU, MenuCallBack, get_user_main_btns
from lexicon.lexicon import LEXICON_OTHER
from middlewares.db import DataBaseSession


user_router = Router()

user_router.message.middleware(DataBaseSession(session_pool=session_maker))
user_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


@user_router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, menu_name="main")

    await message.answer_photo(
        media.media, caption=media.caption, reply_markup=reply_markup
    )


@user_router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    session: AsyncSession
):


    media, reply_markup = await get_menu_content(
        session,
        menu_name=callback_data.menu_name,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()

@user_router.callback_query(F.data == "main_menu", StateFilter("*"))
async def back_to_main_menu(
    callback: CallbackQuery,
    state: FSMContext | None,
    session: AsyncSession
):
    """Сообщение в возврата в главное меню"""
    if state:
        await state.clear()
    await callback.answer()
    banner = await orm_get_banner(session, page="main")
    if not banner.image:
        await callback.message.answer(
           LEXICON_OTHER["need_banner"],
        )
    await callback.message.answer_photo(
        banner.image, caption=banner.description,
        reply_markup=get_user_main_btns()
    )
