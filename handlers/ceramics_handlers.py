from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from handlers.nadlers_methods import products
from middlewares.db import DataBaseSession
from database.methods import orm_get_banner, orm_get_ceramic_work
from keyboards.inline import CERAMICS_MASTERS_MENU, CERAMICS_MENU, MAIN_MENU, ProductCallBack
from lexicon.lexicon import LEXICON_CERAMICS, LEXICON_OTHER


ceramics_router = Router()

ceramics_router.message.middleware(DataBaseSession(session_pool=session_maker))
ceramics_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


@ceramics_router.callback_query(F.data == "ceramics_user")
async def start_ceramics(callback: CallbackQuery, session: AsyncSession):
    """Главное меню разделов керамики"""
    await callback.answer()
    banner = await orm_get_banner(session, page="ceramic")
    if not banner.image:
        await callback.message.answer(
           LEXICON_OTHER["need_banner"],
        )
    await callback.message.answer_photo(
        banner.image, caption=banner.description, reply_markup=CERAMICS_MENU
    )
    # await callback.answer()
    # await callback.message.answer(
    #     LEXICON_CERAMICS["ceramics_menu"],
    #     reply_markup=CERAMICS_MENU
    # )


# Подраздел: предстояще мероприятия
# Должно отображаться новый ответ, с фоторографией и пагинацией предстоящих мероприятий возможность оставить заявку на посещение
@ceramics_router.callback_query(F.data == "cearamics_event_user")
async def cearamics_event(callback: CallbackQuery):
    """Раздел предстоящих мероприятий керамики"""
    await callback.message.answer(
        LEXICON_CERAMICS["ceramics_event"],
        reply_markup=MAIN_MENU
    )


# Подраздел: работы мастеров
# @ceramics_router.callback_query(F.data == "ceramics_works_of_masters") # ТУТА
@ceramics_router.callback_query(ProductCallBack.filter()) # ТУТА
async def ceramics_works_of_masters(
    callback: CallbackQuery, callback_data: ProductCallBack, session: AsyncSession
):
    """Раздел просмотра работ мастеров"""
    # await callback.message.answer(
    #     LEXICON_CERAMICS["ceramics_works_of_masters"],
    #     reply_markup=CERAMICS_MASTERS_MENU
    # )
    text, reply_markup = await products(
        session,
        page=callback_data.page,
    )
    if callback.message.text:
        await callback.message.edit_text(text=text, reply_markup=reply_markup)
    else:
        await callback.message.answer(text=text, reply_markup=reply_markup)
    await callback.answer()


# Подраздел: запись на мастер-класс
@ceramics_router.callback_query(F.data == "ceramics_lesson_user")
async def cearamics_lessons(callback: CallbackQuery):
    """Раздел укроков в мастерской керамики"""
    await callback.message.answer(
        LEXICON_CERAMICS["ceramics_lesson"],
        reply_markup=CERAMICS_MASTERS_MENU
    )
