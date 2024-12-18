from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart, Command
from aiogram.fsm.context import FSMContext

from aiogram.types import Message, CallbackQuery

from keyboards.admin_kb import ADMIN_CERAMIC, ADMIN_EVENT, ADMIN_GALERY, ADMIN_KB, ADMIN_VR, BACK_TO_ADMIN_MENU
from keyboards.inline import EVENT_KB, VR_INFO, VR_MENU
from lexicon.lexicon import LEXICON_ADMIN, LEXICON_CERAMICS, LEXICON_EVENT, LEXICON_OTHER


admin_router = Router()


@admin_router.message(Command(commands=["admin"]))
async def start_admin(message: Message):
    """Главное меню разделов виртуальной реальности"""
    await message.answer(
        LEXICON_ADMIN["admin"],
        reply_markup=ADMIN_KB
    )


@admin_router.callback_query(F.data == "back_admin_menu")
async def start_admin_callback(callback: CallbackQuery):
    await callback.message.answer(
        LEXICON_ADMIN["admin"],
        reply_markup=ADMIN_KB
    )


@admin_router.callback_query(F.data == "add_banner")
async def admin_banner(callback: CallbackQuery):
    await callback.message.answer(
        LEXICON_ADMIN["banner"],
        reply_markup=BACK_TO_ADMIN_MENU
    )


@admin_router.callback_query(F.data == "admin_events")
async def admin_events(callback: CallbackQuery):
    await callback.message.answer(
        LEXICON_ADMIN["event"],
        reply_markup=ADMIN_EVENT
    )


@admin_router.callback_query(F.data == "admin_galery")
async def admin_banner(callback: CallbackQuery):
    await callback.message.answer(
        LEXICON_ADMIN["galery"],
        reply_markup=ADMIN_GALERY
    )


@admin_router.callback_query(F.data == "admin_ceramic")
async def admin_banner(callback: CallbackQuery):
    await callback.message.answer(
        LEXICON_ADMIN["ceramic"],
        reply_markup=ADMIN_CERAMIC
    )


@admin_router.callback_query(F.data == "admin_vr")
async def admin_banner(callback: CallbackQuery):
    await callback.message.answer(
        LEXICON_ADMIN["vr"],
        reply_markup=ADMIN_VR
    )
