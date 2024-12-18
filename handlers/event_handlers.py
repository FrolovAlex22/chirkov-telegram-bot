from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import EVENT_KB, VR_INFO, VR_MENU
from lexicon.lexicon import LEXICON_CERAMICS, LEXICON_EVENT, LEXICON_OTHER


event_router = Router()


@event_router.callback_query(F.data == "event_user")
async def start_vr(callback: CallbackQuery):
    """Главное меню разделов виртуальной реальности"""
    await callback.answer()
    await callback.message.answer(
        LEXICON_EVENT["event_menu"],
        reply_markup=EVENT_KB
    )
