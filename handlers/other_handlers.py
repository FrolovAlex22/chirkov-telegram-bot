from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import orm_get_banner
from handlers.nadlers_methods import get_menu_content
from keyboards.inline import MAIN_MENU, MenuCallBack
from lexicon.lexicon import LEXICON_OTHER
from middlewares.db import DataBaseSession


other_router = Router()

other_router.message.middleware(DataBaseSession(session_pool=session_maker))
other_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


# @other_router.message(CommandStart())
# async def start_cmd(message: Message, session: AsyncSession, state: FSMContext):
#     """Сообщение в случае команды /start"""
#     if state:
#         await state.clear()
#     banner = await orm_get_banner(session, page="main")
#     if not banner.image:
#         await message.answer(
#            LEXICON_OTHER["need_banner"],
#         )
#     await message.answer_photo(
#         banner.image, caption=banner.description, reply_markup=MAIN_MENU
#     )


@other_router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, menu_name="main")

    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@other_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):


    media, reply_markup = await get_menu_content(
        session,
        # level=callback_data.level,
        menu_name=callback_data.menu_name,
        # category=callback_data.category,
        # page=callback_data.page,
        # product_id=callback_data.product_id,
        # user_id=callback.from_user.id,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()

@other_router.callback_query(F.data == "main_menu", StateFilter("*"))
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
        banner.image, caption=banner.description, reply_markup=MAIN_MENU
    )


@other_router.message()
async def reply_to_correspondence(message: Message):
    """Сообщение в случае попытки переписки со стороны пользователя"""
    await message.answer(LEXICON_OTHER["other_answer"], reply_markup=MAIN_MENU)
