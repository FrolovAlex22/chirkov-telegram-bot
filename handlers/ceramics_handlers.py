from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import CERAMICS_MASTERS_MENU, CERAMICS_MENU, MAIN_MENU
from lexicon.lexicon import LEXICON_CERAMICS, LEXICON_OTHER


ceramics_router = Router()


@ceramics_router.callback_query(F.data == "ceramics_user")
async def start_ceramics(callback: CallbackQuery):
    """Главное меню разделов керамики"""
    await callback.answer()
    await callback.message.answer(
        LEXICON_CERAMICS["ceramics_menu"],
        reply_markup=CERAMICS_MENU
    )


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
@ceramics_router.callback_query(F.data == "ceramics_works_of_masters")
async def ceramics_works_of_masters(callback: CallbackQuery):
    """Раздел просмотра работ мастеров"""
    await callback.message.answer(
        LEXICON_CERAMICS["ceramics_works_of_masters"],
        reply_markup=CERAMICS_MASTERS_MENU
    )


# Подраздел: запись на мастер-класс
@ceramics_router.callback_query(F.data == "ceramics_lesson_user")
async def cearamics_lessons(callback: CallbackQuery):
    """Раздел укроков в мастерской керамики"""
    await callback.message.answer(
        LEXICON_CERAMICS["ceramics_lesson"],
        reply_markup=CERAMICS_MASTERS_MENU
    )
