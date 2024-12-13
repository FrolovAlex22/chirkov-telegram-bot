from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline import MAIN_MENU
from lexicon.lexicon import LEXICON_OTHER


other_router = Router()


@other_router.message(CommandStart())
async def start_cmd(message: Message):
    """Сообщение в случае команды /start"""
    text = f"{message.from_user.first_name} {LEXICON_OTHER["main_menu"]}"
    await message.answer(text, reply_markup=MAIN_MENU)


@other_router.message()
async def echo(message: Message):
    """Сообщение в случае попытки переписки со стороны пользователя"""
    await message.answer(LEXICON_OTHER["other_answer"], reply_markup=MAIN_MENU)
