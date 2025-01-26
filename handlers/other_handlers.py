import logging

from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from handlers.handlers_user_methods import get_menu_content
from lexicon.lexicon import LEXICON_OTHER
from middlewares.db import DataBaseSession


other_router = Router()

other_router.message.middleware(DataBaseSession(session_pool=session_maker))
other_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


logger = logging.getLogger(__name__)


@other_router.message()
async def reply_to_correspondence(message: Message, session: AsyncSession):
    """Сообщение в случае попытки переписки со стороны пользователя"""
    logger.info(
        f"Попытка переписки со стороны пользователя {message.from_user.id}"
    )
    media, reply_markup = await get_menu_content(session, menu_name="main")

    await message.answer_photo(
        media.media,
        caption=LEXICON_OTHER["other_answer"],
        reply_markup=reply_markup
    )
