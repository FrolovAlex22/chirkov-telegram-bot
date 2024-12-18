from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import CERAMICS_MASTERS_MENU, CERAMICS_MENU, MAIN_MENU, VR_INFO, VR_MENU
from lexicon.lexicon import LEXICON_CERAMICS, LEXICON_OTHER, LEXICON_VR


vr_router = Router()


@vr_router.callback_query(F.data == "vr_user")
async def start_vr(callback: CallbackQuery):
    """Главное меню разделов виртуальной реальности"""
    await callback.answer()
    await callback.message.answer(
        LEXICON_VR["vr_menu"],
        reply_markup=VR_MENU
    )


# Подраздел: информация
@vr_router.callback_query(F.data == "vr_info")
async def vr_info(callback: CallbackQuery):
    """Раздел информации о виртуальной реальности"""
    await callback.message.answer(
        LEXICON_VR["vr_info"],
        reply_markup=VR_INFO
    )


# Подраздел: заявка
@vr_router.callback_query(F.data == "vr_application")
async def vr_application(callback: CallbackQuery):
    """Раздел заявки на посещение виртуальной реальности"""
    await callback.message.answer(
        LEXICON_VR["vr_application"],
        reply_markup=VR_MENU
    )
