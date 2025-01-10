from aiogram import F, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import orm_get_banner, orm_get_products_by_type_and_category
from handlers.handlers_user_methods import get_menu_content, get_product_content, get_user_service_info
from keyboards.inline import MenuCallBack, ProductCallBack, get_user_main_btns
from lexicon.lexicon import LEXICON_OTHER
from middlewares.db import DataBaseSession


user_router = Router()

user_router.message.middleware(DataBaseSession(session_pool=session_maker))
user_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


@user_router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    """Сообщение в случае команды /start"""
    media, reply_markup = await get_menu_content(session, menu_name="main")

    await message.answer_photo(
        media.media, caption=media.caption, reply_markup=reply_markup
    )


@user_router.callback_query(F.data == "main_menu", StateFilter("*"))
async def back_to_main_menu(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Сообщение в возврата в главное меню"""
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


@user_router.callback_query(MenuCallBack.filter())
async def user_menu(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    session: AsyncSession
):
    """Отображение основных категорий меню"""
    media, reply_markup = await get_menu_content(
        session,
        menu_name=callback_data.menu_name,
    )

    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


@user_router.callback_query(ProductCallBack.filter())
async def user_menu(
    callback: CallbackQuery,
    callback_data: ProductCallBack,
    session: AsyncSession
):

    """Отображение товаров в зависимости от типа и категории"""
    if not callback_data.product_id:
        # if callback_data.pr_type == "PRODUCT":
        #     media, reply_markup = await get_menu_content(
        #         session,
        #         menu_name=callback_data.menu_name,
        #     )

        #     await callback.message.edit_media(media=media, reply_markup=reply_markup)
        #     await callback.answer()

        if callback_data.pr_type == "SERVICE":
            await callback.answer()
            text, reply_markup = await get_product_content(
                session,
                category=callback_data.category,
                type=callback_data.pr_type,
            )

            await callback.message.edit_caption(
                caption=text,
                reply_markup=reply_markup
            )

    else:
        # if callback_data.pr_type == "PRODUCT":
        #     media, reply_markup = await get_menu_content(
        #         session,
        #         menu_name=callback_data.menu_name,
        #     )

        #     await callback.message.edit_media(media=media, reply_markup=reply_markup)
        if callback_data.pr_type == "SERVICE":
            await callback.answer()
            image, reply_markup = await get_user_service_info(
                session, callback_data.category, int(callback_data.product_id)
            )

            await callback.message.edit_media(
                media=image,
                caption=image.caption,
                reply_markup=reply_markup
            )
