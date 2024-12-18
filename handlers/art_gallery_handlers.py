from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import ART_BIRSK_MASTERS, ART_INFO, ART_TODAY, VR_MENU
from lexicon.lexicon import LEXICON_ART_GALLERY


art_router = Router()


@art_router.callback_query(F.data == "art_gallery_user")
async def start_art_gallery(callback: CallbackQuery):
    """Главное меню разделов арт-галереи"""
    await callback.answer()
    await callback.message.answer(
        LEXICON_ART_GALLERY["art_menu"],
        reply_markup=ART_INFO
    )


# Подраздел: галерея сегодня
@art_router.callback_query(F.data == "art_today")
async def art_today_info(callback: CallbackQuery):
    """Текущая коллекция в кафе"""
    await callback.message.answer(
        LEXICON_ART_GALLERY["art_today"],
        reply_markup=ART_TODAY
    )


# Подраздел: Бирские мастера
@art_router.callback_query(F.data == "atr_birsk_masters")
async def art_city_masters(callback: CallbackQuery):
    """Список мастеров города"""
    await callback.message.answer(
        LEXICON_ART_GALLERY["art_birsk_masters"],
        reply_markup=ART_BIRSK_MASTERS
    )
