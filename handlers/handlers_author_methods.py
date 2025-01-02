from datetime import datetime
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.methods import (
    orm_create_author, orm_create_event, orm_delete_author, orm_delete_event,
    orm_get_authors, orm_get_authors_by_id, orm_get_authors_by_name,
    orm_get_banner, orm_get_categories, orm_get_event_by_id,
    orm_get_events_by_category
)
from keyboards.admin_kb import (
    ADMIN_MENU_SELECTION_AUTHOR, ADMIN_MENU_SELECTION_EVENT,
    BACK_TO_ADMIN_MENU, get_authors_list, get_categoryes_list
)
from keyboards.inline import get_callback_btns
from keyboards.my_calendar import CalendarMarkup
from keyboards.reply import ADMIN_CHOISE_CATEGORY
from lexicon.lexicon import LEXICON_ADMIN, LIST_CATEGORY


########################## Управление авторами ################################
class AddAuthor(StatesGroup):
    """FSM Для заполнения модели 'author'"""
    name = State()
    telegram_id = State()
    category = State()


async def admin_author_menu_method(
        session: AsyncSession,
        callback: CallbackQuery
    ):
    await callback.answer()
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_ADMIN["admin_author_choise"],
            reply_markup=ADMIN_MENU_SELECTION_AUTHOR
        )
        return
    banner = await orm_get_banner(session, page="admin")
    await callback.message.answer_photo(
        photo=banner.image,
        caption=LEXICON_ADMIN["admin_author_choise"],
        reply_markup=ADMIN_MENU_SELECTION_AUTHOR
    )
    return


async def admin_authors_list_method(
        session: AsyncSession, callback: CallbackQuery
    ):
    await callback.answer()
    for a in await orm_get_authors(session):
        await callback.message.answer(
            text=f"Имя: <b>{a.name}</b>\nКатегория: <b>{a.category}</b>",
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_author_warning_{a.id}",
                }
            ),
        )

    await callback.message.answer(
        text=LEXICON_ADMIN["authors_list"],
        reply_markup=ADMIN_MENU_SELECTION_AUTHOR
    )
    return


async def delete_author_warning_method(
        session: AsyncSession, callback: CallbackQuery
    ):
    await callback.answer()
    author_id = callback.data.split("_")[-1]
    author = await orm_get_authors_by_id(session, int(author_id))
    await callback.message.answer(
        text=f"<b>ВНИМАНИЕ!</b>\n\nАвтор {author.name} будет удален без"
             " возможности восстановления!!!",
        reply_markup=get_callback_btns(
            btns={
                "Удалить безвозвратно": f"delete_author_{author_id}",
                "Вернуться в раздел авторов": "admin_author"
            },
            sizes=(1, 1)
        )
    )
    return


async def deleted_author_method(
        session: AsyncSession, callback: CallbackQuery
    ):
    author_id = callback.data.split("_")[-1]
    await orm_delete_author(session, int(author_id))

    await callback.answer("Автор удален!")
    await callback.message.answer(
        LEXICON_ADMIN["author_deleted"],
        reply_markup=ADMIN_MENU_SELECTION_AUTHOR
        )
    return


async def admin_author_add_author_method(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text=LEXICON_ADMIN["set_name"],
        reply_markup=BACK_TO_ADMIN_MENU
    )
    return


async def admin_author_add_input_name_method(
        message: Message,
    ):
    await message.delete()
    await message.answer(
        text=LEXICON_ADMIN["set_telegram_id"],
        reply_markup=BACK_TO_ADMIN_MENU
    )
    return


async def admin_author_add_input_telegram_id_method(message: Message):
    if  not message.text.isdigit():
        await message.answer(text="Номер id должен состоять из цифр")
        return
    await message.answer(
        text=LEXICON_ADMIN["set_category"],
        reply_markup=ADMIN_CHOISE_CATEGORY
    )
    return


async def admin_author_add_input_category_method(
          message: Message, data: dict, session: AsyncSession,
    ):
    await message.delete()
    if message.text not in LIST_CATEGORY:
        await message.answer(
            text="Такой категории нет",
            reply_markup=ADMIN_CHOISE_CATEGORY
        )
        return False

    check_name_author = await orm_get_authors_by_name(session, data["name"])
    if check_name_author:
        await message.answer(
            text=LEXICON_ADMIN["admin_author_duplicate"],
            reply_markup=ReplyKeyboardRemove()
        )
        return False

    await orm_create_author(session, data)
    text = f"Автор <b>{data['name']}</b> добавлен"
    await message.answer(
        text=text,
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer(
        text=LEXICON_ADMIN["admin_author_choise_after_add"],
        reply_markup=ADMIN_MENU_SELECTION_AUTHOR
    )
    return True



########################### Управление событиями ##############################
class AddEvent(StatesGroup):
    """FSM Для заполнения модели 'event'"""
    title = State()
    description = State()
    image = State()
    date = State()
    category = State()
    author = State()


async def admin_event_menu_method(
        callback: CallbackQuery, session: AsyncSession
    ):
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_ADMIN["admin_event_choise"],
            reply_markup=ADMIN_MENU_SELECTION_EVENT
        )
        return False
    banner = await orm_get_banner(session, page="admin")
    await callback.message.answer_photo(
        banner.image,
        caption=LEXICON_ADMIN["admin_author_choise"],
        reply_markup=ADMIN_MENU_SELECTION_EVENT
    )
    return


async def admin_events_method(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        text=LEXICON_ADMIN["set_event_title"],
        reply_markup=BACK_TO_ADMIN_MENU
    )
    return


async def admin_add_events_messages_title_method(message: Message):
    if message.photo:
        await message.answer(
            text="Название события не должно быть фотографией",
        )
        return False
    await message.delete()
    await message.answer(
        text=LEXICON_ADMIN["set_event_description"],
        reply_markup=BACK_TO_ADMIN_MENU
    )
    return True


async def admin_add_events_mess_description_method(message: Message):
        if message.photo:
            await message.answer(
                text=LEXICON_ADMIN["photo_error_need_text"],
            )
            return False
        await message.delete()
        await message.answer(
            text=LEXICON_ADMIN["set_event_image"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        return True


async def admin_add_events_messages_image_method(message: Message):
    if not message.photo:
        await message.answer(
            text=LEXICON_ADMIN["text_error_need_photo"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        return False
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    await message.answer(
        text=LEXICON_ADMIN["set_event_date"],
        reply_markup=CalendarMarkup(current_month, current_year).build.kb
    )
    return True


async def admin_add_events_callback_date_method(
        callback: CallbackQuery, session: AsyncSession
    ):
        if "date" in callback.data:
            str_date = callback.data.split()[1]
            await callback.message.delete()
            categoryes = await orm_get_categories(session)
            await callback.message.answer(
                text=LEXICON_ADMIN["set_event_category"],
                reply_markup=get_categoryes_list(categoryes)
            )
            return str_date
        return False


async def admin_add_events_cb_category_method(
        callback: CallbackQuery, session: AsyncSession
    ):
        await callback.message.delete()
        category = callback.data.split("_")[-1]
        authors = await orm_get_authors(session)
        await callback.message.answer(
            text=LEXICON_ADMIN["set_event_author"],
            reply_markup=get_authors_list(authors)
        )
        return category


async def admin_add_events_cb_author_method(
        callback: CallbackQuery, data: dict, session: AsyncSession
    ):
        await callback.message.delete()
        author = callback.data.split("_")[-1]
        data["author"] = author
        await orm_create_event(session, data)
        await callback.message.answer(
            text=LEXICON_ADMIN["event_added"],
            reply_markup=ADMIN_MENU_SELECTION_EVENT
        )
        return


async def admin_events_list_choise_category_method(
        callback: CallbackQuery, session: AsyncSession
    ):
        await callback.answer()
        categoryes_list = await orm_get_categories(session)
        await callback.message.answer(
            text=LEXICON_ADMIN["set_category"],
            reply_markup=get_categoryes_list(categoryes_list)
        )
        return


async def admin_events_list_method(
        callback: CallbackQuery, session: AsyncSession
    ):
        await callback.answer()
        category = callback.data.split("_")[-1]
        for event in await orm_get_events_by_category(session, int(category)):
            text_date = event.date.strftime("%d.%m.%Y")
            await callback.message.answer(
                text=f"<b>{event.title}</b> Дата: {text_date}",
                reply_markup=get_callback_btns(
                    btns={
                        "Удалить": f"delete_event_warning_{event.id}",
                        "Подробнее": f"admin_event_info_{event.id}",
                    }
                ),
            )

        await callback.message.answer(
            text=LEXICON_ADMIN["events_list"],
            reply_markup=ADMIN_MENU_SELECTION_EVENT
        )
        return



async def admin_event_info_method(
        callback: CallbackQuery, session: AsyncSession
    ):
        await callback.answer()
        event_id = callback.data.split("_")[-1]
        event = await orm_get_event_by_id(session, int(event_id))

        text_date = event.date.strftime("%d.%m.%Y")
        text = (
            f"<b>{event.title}</b>\n\n<b>Описание:</b>\n{event.description}\n\n<b>"
            f"Дата проведения:</b> {text_date}\nКатегория: {event.categorys.name}"
            f"\nАвтор: {event.authors.name}"
        )

        await callback.message.answer_photo(
            photo=event.image,
            caption=text,
            reply_markup=ADMIN_MENU_SELECTION_EVENT
        )
        return


async def delete_event_warning_method(
        callback: CallbackQuery, session: AsyncSession
    ):
        event_id = callback.data.split("_")[-1]
        event = await orm_get_event_by_id(session, int(event_id))
        await callback.message.answer(
            text=f"<b>ВНИМАНИЕ!</b>\nМероприятие <b>{event.title}</b> будет "
                "удалено без возможности восстановления!!!",
            reply_markup=get_callback_btns(
                btns={
                    "Удалить безвозвратно": f"delete_event_{event_id}",
                    "Вернуться в раздел мероприятий": "admin_event"
                },
                sizes=(1, 1)
            )
        )
        return


async def deleted_event_method(callback: CallbackQuery, session: AsyncSession):
    event_id = callback.data.split("_")[-1]
    await orm_delete_event(session, int(event_id))

    await callback.answer("Собитие удалено!")
    await callback.message.answer(
        LEXICON_ADMIN["event_deleted"],
        reply_markup=ADMIN_MENU_SELECTION_EVENT
        )
    return
