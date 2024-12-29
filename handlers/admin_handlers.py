from datetime import datetime
from aiogram import F, Router
from aiogram.filters import StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import (
    orm_change_banner_image, orm_create_author, orm_create_event, orm_delete_author, orm_delete_event, orm_get_authors, orm_get_authors_by_id, orm_get_authors_by_name, orm_get_banner, orm_get_categories, orm_get_category_by_name, orm_get_event_by_id, orm_get_events, orm_get_events_by_category, orm_get_info_pages
)
from keyboards.admin_kb import (
ADMIN_KB, ADMIN_MENU_SELECTION_AUTHOR, ADMIN_MENU_SELECTION_EVENT,
    BACK_TO_ADMIN_MENU, SELECTION_AFTER_ADDING_BANNER, get_authors_list, get_categoryes_list,

)
from keyboards.inline import get_callback_btns
from keyboards.my_calendar import CalendarMarkup
from keyboards.reply import ADMIN_CHOISE_CATEGORY
from lexicon.lexicon import LEXICON_ADMIN, LEXICON_CERAMICS, LEXICON_OTHER, LIST_CATEGORY
from middlewares.db import DataBaseSession


admin_router = Router()

admin_router.message.middleware(DataBaseSession(session_pool=session_maker))
admin_router.callback_query.middleware(
    DataBaseSession(session_pool=session_maker)
)


# Переход в основные разделы администратора
@admin_router.message(Command(commands=["admin"]))
async def start_admin(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    """Вызов меню администратора"""
    await state.clear()
    banner = await orm_get_banner(session, page="admin")
    if not banner.image:
        await message.answer(
            LEXICON_OTHER["need_banner"], reply_markup=ADMIN_KB
        )
    await message.answer_photo(
        banner.image, caption=banner.description, reply_markup=ADMIN_KB
    )


@admin_router.callback_query(F.data == "back_admin_menu")
async def start_admin_callback(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    await state.clear()
    await callback.answer()
    banner = await orm_get_banner(session, page="admin")
    if not banner.image:
        await callback.message.answer(
            LEXICON_OTHER["need_banner"], reply_markup=ADMIN_KB
        )
    await callback.message.answer_photo(
        banner.image, caption=banner.description, reply_markup=ADMIN_KB
    )


@admin_router.callback_query(F.data == "back_admin_menu")
async def start_admin_callback(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    await state.clear()
    await callback.answer()
    banner = await orm_get_banner(session, page="admin")
    if not banner.image:
        await callback.message.answer(
            LEXICON_OTHER["need_banner"], reply_markup=ADMIN_KB
        )
    await callback.message.answer_photo(
        banner.image, caption=banner.description, reply_markup=ADMIN_KB
    )

######################## Управление баннерами #################################
class AddBanner(StatesGroup):
    """FSM для загрузки/изменения баннеров"""
    image = State()


@admin_router.callback_query(
        StateFilter(None),
        or_f(F.data == 'add_banner')
    )
async def add_banner_image(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    """
    Отправляем перечень информационных страниц бота и становимся в состояние
    отправки photo
    """
    await callback.answer()
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await callback.message.answer(
        f"Отправьте фото баннера.\nВ описании укажите для"
        f" какой страницы:\n{', '.join(pages_names)}",
        reply_markup=get_callback_btns(
            btns={"Отмена, вернуться в меню администратора": "back_admin_menu"},
            sizes=(1, 1)
        )
    )
    await state.set_state(AddBanner.image)


@admin_router.message(AddBanner.image, F.photo)
async def add_banner(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    """
    Добавляем/изменяем изображение в таблице (данные баннера заполнены в БД)
    """
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    print(for_page)
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(f"Введите нормальное название страницы, например:\
                         \n{', '.join(pages_names)}")
        return

    await state.update_data(image_id=image_id, for_page=for_page)
    await orm_change_banner_image(session, for_page, image_id,)
    await message.answer(
        "Баннер добавлен/изменен.",
        reply_markup=SELECTION_AFTER_ADDING_BANNER
    )
    await state.clear()


@admin_router.message(AddBanner.image)
async def add_banner_wrong(message: Message) -> None:
    """Ловим некоррекный ввод"""
    await message.answer("Отправьте фото баннера или отмена")


########################## Управление авторами ################################
class AddAuthor(StatesGroup):
    """FSM Для заполнения модели 'author'"""
    name = State()
    telegram_id = State()
    category = State()


@admin_router.callback_query(F.data == "admin_author")
async def admin_author_menu(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Главное меню раздела Авторы"""
    await callback.answer()
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_ADMIN["admin_author_choise"],
            reply_markup=ADMIN_MENU_SELECTION_AUTHOR
        )
        return
    banner = await orm_get_banner(session, page="admin")
    await callback.message.answer_photo(

        caption=LEXICON_ADMIN["admin_author_choise"],
        reply_markup=ADMIN_MENU_SELECTION_AUTHOR
    )


@admin_router.callback_query(F.data == "admin_author_list")
async def admin_authors_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Отображение списка авторов. Возможность удаления"""
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


@admin_router.callback_query(F.data.startswith("delete_author_warning_"))
async def delete_author_warning_(
    callback: CallbackQuery,
    session: AsyncSession
) -> None:
    """Предупреждение перед удалением автора"""
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


@admin_router.callback_query(F.data.startswith("delete_author_"))
async def deleted_author(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем автора"""
    author_id = callback.data.split("_")[-1]
    await orm_delete_author(session, int(author_id))

    await callback.answer("Автор удален!")
    await callback.message.answer(
        LEXICON_ADMIN["author_deleted"],
        reply_markup=ADMIN_MENU_SELECTION_AUTHOR
        )


@admin_router.callback_query(F.data == "add_author")
async def admin_author_add_author(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.answer()
    await callback.message.answer(
        text=LEXICON_ADMIN["set_name"],
        reply_markup=BACK_TO_ADMIN_MENU
    )
    await state.set_state(AddAuthor.name)


@admin_router.message(
        StateFilter(AddAuthor.name, AddAuthor.telegram_id, AddAuthor.category),
        F.text
    )
async def admin_author_add_input_fields(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
):
    """
    Добавление автора в БД. Обработка всех состояний в процессе заполнения
    FSM AddAuthor.
    """
    actual_state = await state.get_state()

    if actual_state == AddAuthor.name:
        await state.update_data(name=message.text)
        await message.delete()
        await message.answer(
            text=LEXICON_ADMIN["set_telegram_id"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        await state.set_state(AddAuthor.telegram_id)

    elif actual_state == AddAuthor.telegram_id:
        if  not message.text.isdigit():
            await message.answer(text="Номер id должен состоять из цифр")
            return
        await state.update_data(telegram_id=message.text)
        await message.answer(
            text=LEXICON_ADMIN["set_category"],
            reply_markup=ADMIN_CHOISE_CATEGORY
        )
        await state.set_state(AddAuthor.category)

    elif actual_state == AddAuthor.category:
        await message.delete()
        if message.text not in LIST_CATEGORY:
            await message.answer(
                text="Такой категории нет",
                reply_markup=ADMIN_CHOISE_CATEGORY
            )
            return

        category = await orm_get_category_by_name(session, message.text)
        await state.update_data(category=str(category.id))
        data = await state.get_data()
        check_name_author = await orm_get_authors_by_name(session, data["name"])
        if check_name_author:
            await message.answer(
                text=LEXICON_ADMIN["admin_author_duplicate"],
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(AddAuthor.name)
            return

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
        await state.clear()


########################### Управление событиями ##############################
class AddEvent(StatesGroup):
    """FSM Для заполнения модели 'event'"""
    title = State()
    description = State()
    image = State()
    date = State()
    category = State()
    author = State()


@admin_router.callback_query(F.data == "admin_event")
async def admin_author_menu(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Главное меню раздела Мероприятия"""
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_ADMIN["admin_event_choise"],
            reply_markup=ADMIN_MENU_SELECTION_EVENT
        )
        return
    banner = await orm_get_banner(session, page="admin")
    await callback.message.answer_photo(
        banner.image,
        caption=LEXICON_ADMIN["admin_author_choise"],
        reply_markup=ADMIN_MENU_SELECTION_EVENT
    )


@admin_router.callback_query(F.data == "admin_event_list")
async def admin_events_list_choise_category(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Выбор категории перед отображением списка мероприятий"""
    await callback.answer()
    categoryes_list = await orm_get_categories(session)
    await callback.message.answer(
        text=LEXICON_ADMIN["set_category"],
        reply_markup=get_categoryes_list(categoryes_list)
    )


@admin_router.callback_query(F.data.startswith("choise_category_"))
async def admin_events_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Отображение списка мероприятий"""
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


@admin_router.callback_query(F.data.startswith("admin_event_info_"))
async def admin_event_info(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Отображение информации о мероприятии"""
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



@admin_router.callback_query(F.data.startswith("delete_event_warning_"))
async def delete_event_warning_(
    callback: CallbackQuery,
    session: AsyncSession
) -> None:
    """Предупреждение перед удалением мероприятия"""
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


@admin_router.callback_query(F.data.startswith("delete_event_"))
async def deleted_event(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем мероприятие"""
    event_id = callback.data.split("_")[-1]
    await orm_delete_event(session, int(event_id))

    await callback.answer("Собитие удалено!")
    await callback.message.answer(
        LEXICON_ADMIN["event_deleted"],
        reply_markup=ADMIN_MENU_SELECTION_EVENT
        )


@admin_router.callback_query(F.data == "add_event")
async def admin_events(callback: CallbackQuery, state: FSMContext):
    """Добавление события. Начало заполнения FSM AddEvent"""
    await callback.answer()
    await callback.message.answer(
        text=LEXICON_ADMIN["set_event_title"],
        reply_markup=BACK_TO_ADMIN_MENU
    )
    await state.set_state(AddEvent.title)


@admin_router.message(
        StateFilter(
            AddEvent.title,
            AddEvent.description,
            AddEvent.image,
        ),
        or_f(F.text, F.photo)
    )
async def admin_add_events_messages(message: Message, state: FSMContext):
    """Обработка всех состояний типа Messqge при заполнении FSM AddEvent"""
    actual_state = await state.get_state()

    if actual_state == AddEvent.title:
        if message.photo:
            await message.answer(
                text=LEXICON_ADMIN["photo_error_need_text"],
            )
            return
        await state.update_data(title=message.text)
        await message.delete()
        await message.answer(
            text=LEXICON_ADMIN["set_event_description"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        await state.set_state(AddEvent.description)

    elif actual_state == AddEvent.description:
        if message.photo:
            await message.answer(
                text=LEXICON_ADMIN["photo_error_need_text"],
            )
            return
        await state.update_data(description=message.text)
        await message.delete()
        await message.answer(
            text=LEXICON_ADMIN["set_event_image"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        await state.set_state(AddEvent.image)

    elif actual_state == AddEvent.image:
        if message.photo:
            await state.update_data(image=message.photo[-1].file_id)
        else:
            await message.answer(
                text=LEXICON_ADMIN["text_error_need_photo"],
                reply_markup=BACK_TO_ADMIN_MENU
            )
            return
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year
        await message.answer(
            text=LEXICON_ADMIN["set_event_date"],
            reply_markup=CalendarMarkup(current_month, current_year).build.kb
        )
        await state.set_state(AddEvent.date)


@admin_router.message(
        StateFilter(AddEvent.title, AddEvent.description, AddEvent.image,
        ),
    )
async def admin_add_events_messages_error(message: Message):
    """Обработка не правильных сообщений при заполнении FSM AddEvent"""
    await message.answer(
        text=LEXICON_ADMIN["error_need_photo_or_text"],
        reply_markup=BACK_TO_ADMIN_MENU
    )


@admin_router.callback_query(
        StateFilter(
            AddEvent.date,
            AddEvent.category,
            AddEvent.author
        ),
    )
async def admin_add_events_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """Обработка всех состояний типа Callback при заполнении FSM AddEvent"""
    await callback.answer()
    actual_state = await state.get_state()
    mes = callback.data

    if actual_state == AddEvent.date:
        if "date" in mes:
            str_date = callback.data.split()[1]
            await state.update_data(date=str_date)
            await callback.message.delete()
            categoryes = await orm_get_categories(session)
            await callback.message.answer(
                text=LEXICON_ADMIN["set_event_category"],
                reply_markup=get_categoryes_list(categoryes)
            )
            await state.set_state(AddEvent.category)

    if actual_state == AddEvent.category:
        await callback.message.delete()
        category = mes.split("_")[-1]
        await state.update_data(category=category)
        authors = await orm_get_authors(session)
        await callback.message.answer(
            text=LEXICON_ADMIN["set_event_author"],
            reply_markup=get_authors_list(authors)
        )
        await state.set_state(AddEvent.author)

    if actual_state == AddEvent.author:
        await callback.message.delete()
        author = mes.split("_")[-1]
        await state.update_data(author=author)
        data = await state.get_data()
        await orm_create_event(session, data)
        await callback.message.answer(
            text=LEXICON_ADMIN["event_added"],
            reply_markup=ADMIN_MENU_SELECTION_EVENT
        )

# # EVENTS
# @admin_router.callback_query(F.data == "admin_events")
# async def admin_events(callback: CallbackQuery):
#     await callback.message.edit_caption(
#         caption=LEXICON_ADMIN["event"],
#         reply_markup=ADMIN_EVENT
#     )


# # GALERY
# @admin_router.callback_query(F.data == "admin_galery")
# async def admin_galery(callback: CallbackQuery):
#     await callback.message.edit_caption(
#         caption=LEXICON_ADMIN["galery"],
#         reply_markup=ADMIN_GALERY
#     )


# # CERAMIC
# class CeramicMaster(StatesGroup):
#     name = State()


# @admin_router.callback_query(F.data == "admin_ceramic")
# async def admin_ceramic(
#     callback: CallbackQuery,
#     session: AsyncSession,
#     state: FSMContext
# ):
#     if state:
#         await state.clear()
#     await callback.answer()
#     if callback.message.photo:
#         await callback.message.edit_caption(
#             caption=LEXICON_ADMIN["ceramic"],
#             reply_markup=ADMIN_CERAMIC
#         )
#     else:
#         banner = await orm_get_banner(session, page="admin")
#         if not banner.image:
#             await callback.message.answer(
#                 LEXICON_OTHER["need_banner"], reply_markup=ADMIN_KB
#             )
#         await callback.message.answer_photo(
#             banner.image,
#             caption=LEXICON_ADMIN["ceramic"],
#             reply_markup=ADMIN_CERAMIC
#         )


# @admin_router.callback_query(F.data == "admin_ceramic_master_and_works")
# async def admin_ceramic_master_and_works(callback: CallbackQuery):
#     await callback.message.edit_caption(
#         caption=LEXICON_CERAMICS["admin_master_and_works"],
#         reply_markup=ADMIN_CERAMIC_MASTERS
#     )


# # ceramic: master
# @admin_router.callback_query(F.data == "admin_ceramic_master")
# async def admin_ceramic_master_menu(callback: CallbackQuery):
#     await callback.message.edit_caption(
#         caption=LEXICON_CERAMICS["admin_master"],
#         reply_markup=ADMIN_CERAMIC_MASTERS_CHOISE
#     )


# @admin_router.callback_query(F.data == "admin_ceramic_master_add")
# async def admin_ceramic_master_add(
#     callback: CallbackQuery,
#     state: FSMContext
# ):
#     await callback.answer()
#     await state.set_state(CeramicMaster.name)
#     if callback.message.photo:
#         await callback.message.edit_caption(
#             caption=LEXICON_CERAMICS["admin_master_add"],
#             reply_markup=BACK_TO_ADMIN_MENU
#         )
#     else:
#         await callback.message.answer(
#             text=LEXICON_CERAMICS["admin_master_add"],
#             reply_markup=BACK_TO_ADMIN_MENU
#         )


# @admin_router.message(CeramicMaster.name, F.text)
# async def admin_ceramic_master_add_get_name(
#     message: Message,
#     state: FSMContext,
#     session: AsyncSession
# ):
#     await orm_add_ceramic_master(session, message.text)
#     await message.delete()
#     await state.clear()
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_master_add_complete"],
#         reply_markup=ADMIN_CERAMIC_MASTERS_AFTER_ADD
#     )


# @admin_router.message(CeramicMaster.name, ~F.text)
# async def admin_ceramic_master_add_get_name(
#     message: Message,
# ):
#     await message.delete()
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_master_add_error"],
#         reply_markup=BACK_TO_ADMIN_MENU
#     )


# @admin_router.callback_query(F.data == "admin_ceramic_master_list")
# async def admin_ceramic_master_list(
#     callback: CallbackQuery,
#     session: AsyncSession
# ):
#     for master in await orm_get_ceramic_masters(session):
#         await callback.message.answer(
#             text=(f"{master.name}\n"
#             ),
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Удалить": f"delete_master_warning_{master.id}",
#                 }
#             ),
#         )
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_master_list"],
#         reply_markup=ADMIN_CERAMIC_MASTERS_LIST
#     )


# @admin_router.callback_query(F.data.startswith("delete_master_warning_"))
# async def ceramicmaster_delete_warning(
#     callback: CallbackQuery,
#     session: AsyncSession
# ) -> None:
#     """Предупреждение перед удалением мастера"""
#     master_id = callback.data.split("_")[-1]
#     master = await orm_get_ceramic_master(session, int(master_id))
#     await callback.message.answer(
#         text=f"<b>ВНИМАНИЕ!</b>\n\nМастер {master.name} будет удален без"
#              " возможности восстановления!!!",
#         reply_markup=get_callback_btns(
#             btns={
#                 "Удалить безвозвратно": f"delete_master_{master_id}",
#                 "Вернуться в раздел керамики": "admin_ceramic"
#             },
#             sizes=(1, 1)
#         )
#     )


# @admin_router.callback_query(F.data.startswith("delete_master_"))
# async def ceramic_master_delete(
#     callback: CallbackQuery, session: AsyncSession
# ) -> None:
#     """Удаляем мастера"""
#     master_id = callback.data.split("_")[-1]
#     await orm_delete_ceramic_master(session, int(master_id))

#     await callback.answer("Мастер удален")
#     await callback.message.answer(
#         LEXICON_CERAMICS["admin_master_after_delete"],
#         reply_markup=ADMIN_CERAMIC_MASTERS_LIST
#         )


# # ceramic: works
# class CeramicWorks(StatesGroup):
#     title = State()
#     description = State()
#     price = State()
#     master = State


# @admin_router.callback_query(F.data == "admin_ceramic_works")
# async def admin_ceramic_works(callback: CallbackQuery):
#     await callback.message.edit_caption(
#         caption=LEXICON_CERAMICS["admin_works"],
#         reply_markup=ADMIN_CERAMIC_WORKS
#     )


# @admin_router.callback_query(F.data == "admin_ceramic_works_add")
# async def admin_ceramic_works_add(
#     callback: CallbackQuery,
#     state: FSMContext
# ):
#     await callback.answer()
#     await state.set_state(CeramicWorks.title)
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_works_add"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )


# @admin_router.message(CeramicWorks.title, F.text)
# async def admin_ceramic_works_add_get_title(
#     message: Message,
#     state: FSMContext
# ):
#     await state.update_data(title=message.text)
#     await message.delete()
#     await state.set_state(CeramicWorks.description)
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_works_add_description"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )

# @admin_router.message(CeramicWorks.title, ~F.text)
# async def admin_ceramic_works_add_get_title_wrong(
#     message: Message,
# ):
#     await message.delete()
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_works_add_error"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )


# @admin_router.message(CeramicWorks.description, F.text)
# async def admin_ceramic_works_add_get_description(
#     message: Message,
#     state: FSMContext
# ):
#     await state.update_data(description=message.text)
#     await message.delete()
#     await state.set_state(CeramicWorks.price)
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_works_add_price"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )


# @admin_router.message(CeramicWorks.price, F.text)
# async def admin_ceramic_works_add_get_price(
#     message: Message,
#     state: FSMContext,
#     session: AsyncSession
# ):
#     if not message.text.isdigit():
#         await message.delete()
#         await message.answer(
#             text=LEXICON_CERAMICS["admin_works_add_error_price"],
#             reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#         )
#         return
#     await state.update_data(price=message.text)
#     await message.delete()
#     mastrer_list = await orm_get_ceramic_masters(session)
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_works_add_master"],
#         reply_markup=get_ceramic_works_btns(
#             masters_list=mastrer_list,
#             sizes=(1, )
#         )
#     )
#     await state.set_state(CeramicWorks.master)


# @admin_router.message(CeramicWorks.price, ~F.text)
# async def admin_ceramic_works_add_get_price_wrong(
#     message: Message,
# ):
#     await message.delete()
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_works_add_error"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )


# @admin_router.callback_query(F.data.startswith("choise_master_works_"))
# async def admin_ceramic_works_choise_master(
#     callback: CallbackQuery,
#     state: FSMContext,
#     session: AsyncSession
# ):
#     await callback.answer()
#     master_id = callback.data.split("_")[-1]
#     await callback.message.delete()
#     data = await state.get_data()
#     await orm_add_ceramic_work(
#         session = session,
#         title=data["title"],
#         description=data["description"],
#         price=int(data["price"]),
#         master_id=int(master_id)
#     )
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_works_add_complete"],
#         reply_markup=ADMIN_CERAMIC_WORKS
#     )
#     await state.clear()


# @admin_router.callback_query(F.data == "admin_ceramic_works_list")
# async def admin_ceramic_works_list_choise_master(
#     callback: CallbackQuery,
#     session: AsyncSession
# ):
#     await callback.answer()
#     masters = await orm_get_ceramic_masters(session)
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_works_list_choise"],
#         reply_markup=get_ceramic_masters_btns(
#             masters_list=masters
#         )
#     )


# @admin_router.callback_query(F.data.startswith("choise_master_work_list_"))
# async def admin_ceramic_works_list(
#     callback: CallbackQuery,
#     session: AsyncSession
# ):
#     await callback.message.delete()
#     for work in await orm_get_ceramic_works_by_master(
#         session, master_id=int(callback.data.split("_")[-1])
#     ):
#         await callback.message.answer(
#             text=f"{work.title}",
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Удалить": f"delete_work_warning_{work.id}",
#                 }
#             )
#         )
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_works_list"],
#         reply_markup=ADMIN_CERAMIC_MASTERS_LIST
#     )


# @admin_router.callback_query(F.data.startswith("delete_work_warning_"))
# async def admin_ceramic_works_delete_warning(
#     callback: CallbackQuery,
#     session: AsyncSession
# ):
#     await callback.answer()
#     work_id = callback.data.split("_")[-1]
#     work = await orm_get_ceramic_work(session, int(work_id))
#     text = f"{LEXICON_CERAMICS["admin_works_delete_warning"]} {work.title}"
#     await callback.message.answer(
#         text,
#         reply_markup=get_callback_btns(
#             btns={
#                 "Удалить": f"delete_work_{work_id}",
#                 "Отменить и вернуться в раздел керамики": "admin_ceramic"
#             }
#         )
#     )


# @admin_router.callback_query(F.data.startswith("delete_work_"))
# async def admin_ceramic_works_delete(
#     callback: CallbackQuery,
#     session: AsyncSession
# ):
#     await callback.answer()
#     work_id = callback.data.split("_")[-1]
#     await orm_delete_ceramic_work(session, int(work_id))
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_works_after_delete"],
#         reply_markup=ADMIN_CERAMIC_WORKS_AFTER_DELETE
#     )


# # ceramic: service
# class CeramicService(StatesGroup):
#     title = State()
#     price = State()


# @admin_router.callback_query(F.data == "admin_ceramic_services")
# async def admin_ceramic_services(callback: CallbackQuery):
#     await callback.message.edit_caption(
#         caption=LEXICON_CERAMICS["admin_service_choise"],
#         reply_markup=ADMIN_CERAMIC_SERVICES
#     )


# @admin_router.callback_query(F.data == "admin_ceramic_add_service")
# async def admin_ceramic_add_service(
#     callback: CallbackQuery,
#     state: FSMContext
# ):
#     await callback.answer()
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_service_add"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )
#     await state.set_state(CeramicService.title)


# @admin_router.message(CeramicService.title, F.text)
# async def admin_ceramic_add_service_get_title(
#     message: Message,
#     state: FSMContext
# ):
#     await state.update_data(title=message.text)
#     await message.delete()
#     text = (
#         f"Вы ввели: <b>{message.text}</b>\n\nТеперь введите цену целым "
#         "числом:"
#         )
#     await message.answer(
#         text,
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )

#     await state.set_state(CeramicService.price)


# @admin_router.message(CeramicService.title, ~F.text)
# async def admin_ceramic_add_service_get_title(
#     message: Message,
# ):
#     await message.delete()
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_service_add_error"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )


# @admin_router.message(CeramicService.price, F.text)
# async def admin_ceramic_add_service_get_price(
#     message: Message,
#     state: FSMContext,
#     session: AsyncSession
# ):
#     data = await state.get_data()
#     price = int(message.text)
#     await message.delete()
#     await orm_add_ceramic_service(session, data["title"], price)
#     text = (
#         f"{LEXICON_CERAMICS["admin_service_add_complete"]}Название: "
#         f"{data['title']}\nЦена: {price}"
#     )
#     await message.answer(
#         text=text,
#         reply_markup=ADMIN_CERAMIC_SERVICES_AFTER_ADD
#     )
#     await state.clear()


# @admin_router.message(CeramicService.price, ~F.text)
# async def admin_ceramic_add_service_get_price(
#     message: Message,
# ):
#     await message.delete()
#     await message.answer(
#         text=LEXICON_CERAMICS["admin_service_add_error_price"],
#         reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
#     )


# @admin_router.callback_query(F.data == "admin_ceramic_services_list")
# async def admin_ceramic_service_list(
#     callback: CallbackQuery,
#     session: AsyncSession
# ):
#     await callback.answer()
#     for service in await orm_get_ceramic_services(session):
#         await callback.message.answer(
#             text=(f"{service.title}: {service.price} руб."
#             ),
#             reply_markup=get_callback_btns(
#                 btns={
#                     "Удалить": f"delete_service_warning_{service.id}",
#                 }
#             ),
#         )
#     await callback.message.answer(
#         text=LEXICON_CERAMICS["admin_service_list"],
#         reply_markup=ADMIN_CERAMIC_MASTERS_LIST
#     )


# @admin_router.callback_query(F.data.startswith("delete_service_warning_"))
# async def ceramic_serice_delete_warning(
#     callback: CallbackQuery,
#     session: AsyncSession
# ) -> None:
#     """Предупреждение перед удалением сервиса"""
#     service_id = callback.data.split("_")[-1]
#     service = await orm_get_ceramic_service(session, int(service_id))
#     await callback.message.answer(
#         text=f"<b>ВНИМАНИЕ!</b>\nУслуга {service.title} будет удалена без"
#              " возможности восстановления!!!",
#         reply_markup=get_callback_btns(
#             btns={
#                 "Удалить безвозвратно": f"delete_service_{service_id}",
#                 "Вернуться в раздел керамики": "admin_ceramic"
#             },
#             sizes=(1, 1)
#         )
#     )


# @admin_router.callback_query(F.data.startswith("delete_service_"))
# async def ceramic_service_delete(
#     callback: CallbackQuery, session: AsyncSession
# ) -> None:
#     """Удаляем мастера"""
#     service_id = callback.data.split("_")[-1]
#     await orm_delete_ceramic_service(session, int(service_id))

#     await callback.answer("Сервис удален")
#     await callback.message.answer(
#         LEXICON_CERAMICS["admin_service_after_delete"],
#         reply_markup=ADMIN_CERAMIC_MASTERS_LIST
#         )


# # VR
# @admin_router.callback_query(F.data == "admin_vr")
# async def admin_vr(callback: CallbackQuery):
#     await callback.message.edit_caption(
#         caption=LEXICON_ADMIN["vr"],
#         reply_markup=ADMIN_VR
#     )
