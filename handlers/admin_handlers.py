from aiogram import F, Router
from aiogram.filters import StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import (
    orm_change_banner_image, orm_create_product, orm_delete_product,
    orm_get_authors, orm_get_banner, orm_get_categories, orm_get_info_pages,
    orm_get_product_by_id, orm_get_products_by_category
)
from handlers.handlers_author_methods import (
    AddAuthor, AddEvent, admin_add_events_callback_date_method,
    admin_add_events_cb_author_method, admin_add_events_cb_category_method,
    admin_add_events_mess_description_method,
    admin_add_events_messages_image_method,
    admin_add_events_messages_title_method, admin_author_add_author_method,
    admin_author_add_input_category_method, admin_author_add_input_name_method,
    admin_author_add_input_telegram_id_method, admin_author_menu_method,
    admin_authors_list_method, admin_event_info_method, admin_event_menu_method,
    admin_events_list_choise_category_method,
    admin_events_list_method, admin_events_method,
    delete_author_warning_method, delete_event_warning_method,
    deleted_author_method, deleted_event_method
)
from keyboards.admin_kb import (
    ADMIN_KB, ADMIN_MENU_SELECTION_PRODUCT, ADMIN_MENU_SELECTION_STATUS,
    BACK_TO_ADMIN_MENU, SELECTION_AFTER_ADDING_BANNER,
    get_authors_list_by_product, get_categoryes_list_by_product,

)
from keyboards.inline import get_callback_btns
from lexicon.lexicon import LEXICON_ADMIN, LEXICON_OTHER
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
@admin_router.callback_query(F.data == "admin_author")
async def admin_author_menu(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    """Главное меню раздела Авторы"""
    await state.clear()
    await admin_author_menu_method(session, callback)


@admin_router.callback_query(F.data == "admin_author_list")
async def admin_authors_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Отображение списка авторов. Возможность удаления"""
    await admin_authors_list_method(session, callback)


@admin_router.callback_query(F.data.startswith("delete_author_warning_"))
async def delete_author_warning_(
    callback: CallbackQuery,
    session: AsyncSession
) -> None:
    """Предупреждение перед удалением автора"""
    await delete_author_warning_method(session, callback)


@admin_router.callback_query(F.data.startswith("delete_author_"))
async def deleted_author(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем автора"""
    await deleted_author_method(session, callback)


@admin_router.callback_query(F.data == "add_author")
async def admin_author_add_author(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Начало добавления автора"""
    await admin_author_add_author_method(callback)
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
        await admin_author_add_input_name_method(message, state)
        await state.update_data(name=message.text)
        await state.set_state(AddAuthor.telegram_id)

    elif actual_state == AddAuthor.telegram_id:
        await admin_author_add_input_telegram_id_method(message, state)
        await state.update_data(telegram_id=message.text)
        await state.set_state(AddAuthor.category)

    elif actual_state == AddAuthor.category:
        data = await state.get_data()
        answer = await admin_author_add_input_category_method(
            message, data, session
        )
        if answer:
            await state.clear()
        else:
            await state.set_state(AddAuthor.name)
            await message.answer(
                text="Введите имя автора",
            )


########################### Управление событиями ##############################
@admin_router.callback_query(F.data == "admin_event")
async def admin_event_menu(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    """Главное меню раздела Мероприятия"""
    await state.clear()
    await admin_event_menu_method(callback, session)


@admin_router.callback_query(F.data == "add_event")
async def admin_events(callback: CallbackQuery, state: FSMContext):
    """Добавление события. Начало заполнения FSM AddEvent"""
    await state.clear()
    await admin_events_method(callback)
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
        answer = await admin_add_events_messages_title_method(message)
        if answer:
            await state.update_data(title=message.text)
            await state.set_state(AddEvent.description)


    elif actual_state == AddEvent.description:
        answer = await admin_add_events_mess_description_method(message)
        if answer:
            await state.update_data(description=message.text)
            await state.set_state(AddEvent.image)

    elif actual_state == AddEvent.image:
        anwer = await admin_add_events_messages_image_method(message)
        if anwer:
            await state.update_data(image=message.photo[-1].file_id)
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

    if actual_state == AddEvent.date:
        answer = await admin_add_events_callback_date_method(callback, session)
        if answer:
            await state.update_data(date=answer)
            await state.set_state(AddEvent.category)

    if actual_state == AddEvent.category:
        category = await admin_add_events_cb_category_method(callback, session)
        await state.update_data(category=category)
        await state.set_state(AddEvent.author)

    if actual_state == AddEvent.author:
        data = await state.get_data()
        await admin_add_events_cb_author_method(callback, data, session)
        await state.clear()


@admin_router.callback_query(F.data == "admin_event_list")
async def admin_events_list_choise_category(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Выбор категории перед отображением списка мероприятий"""
    await admin_events_list_choise_category_method(callback, session)


@admin_router.callback_query(F.data.startswith("choise_category_"))
async def admin_events_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Отображение списка мероприятий"""
    await admin_events_list_method(callback, session)


@admin_router.callback_query(F.data.startswith("admin_event_info_"))
async def admin_event_info(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Отображение информации о мероприятии"""
    await admin_event_info_method(callback, session)



@admin_router.callback_query(F.data.startswith("delete_event_warning_"))
async def delete_event_warning_(
    callback: CallbackQuery,
    session: AsyncSession
) -> None:
    """Предупреждение перед удалением мероприятия"""
    await delete_event_warning_method(callback, session)


@admin_router.callback_query(F.data.startswith("delete_event_"))
async def deleted_event(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем мероприятие"""
    await deleted_event_method(callback, session)


########################### Управление продуктами ##############################
class AddProduct(StatesGroup):
    """FSM Для заполнения модели 'product'"""
    name = State()
    description = State()
    price = State()
    image = State()
    category = State()
    author = State()
    status = State()


@admin_router.callback_query(F.data == "admin_product")
async def admin_product_menu(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    """Главное меню раздела Продукты"""
    if await state.get_state():
        await state.clear()
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_ADMIN["admin_product_choise"],
            reply_markup=ADMIN_MENU_SELECTION_PRODUCT
        )
        return
    banner = await orm_get_banner(session, page="admin")
    await callback.message.answer_photo(
        banner.image,
        caption=LEXICON_ADMIN["admin_product_choise"],
        reply_markup=ADMIN_MENU_SELECTION_PRODUCT
    )


@admin_router.callback_query(F.data == "add_product")
async def admin_add_product(callback: CallbackQuery, state: FSMContext):
    """Добавление товара. Начало заполнения FSM AddEvent"""
    await callback.answer()
    await callback.message.answer(
        text=LEXICON_ADMIN["set_product_name"],
        reply_markup=BACK_TO_ADMIN_MENU
    )
    await state.set_state(AddProduct.name)


@admin_router.message(
        StateFilter(
            AddProduct.name,
            AddProduct.description,
            AddProduct.price,
            AddProduct.image,
        ),
        or_f(F.text, F.photo)
    )
async def admin_add_product_messages(
    message: Message, state: FSMContext, session: AsyncSession
):
    """Обработка всех состояний типа Messqge при заполнении FSM AddProduct"""
    actual_state = await state.get_state()

    if actual_state == AddProduct.name:
        if message.photo:
            await message.answer(
                text=LEXICON_ADMIN["photo_error_need_text"],
            )
            return
        await state.update_data(name=message.text)
        await message.delete()
        await message.answer(
            text=LEXICON_ADMIN["set_product_description"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        await state.set_state(AddProduct.description)

    elif actual_state == AddProduct.description:
        if message.photo:
            await message.answer(
                text=LEXICON_ADMIN["photo_error_need_text"],
            )
            return
        await state.update_data(description=message.text)
        await message.delete()
        await message.answer(
            text=LEXICON_ADMIN["set_product_price"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        await state.set_state(AddProduct.price)

    elif actual_state == AddProduct.price:
        if message.photo:
            await message.answer(
                text=LEXICON_ADMIN["photo_error_need_text"],
            )
            return
        if not message.text.isdigit():
            await message.delete()
            await message.answer(
                text=LEXICON_ADMIN["admin_works_add_error_price"],
                reply_markup=BACK_TO_ADMIN_MENU
            )
            return
        await state.update_data(price=message.text)
        await message.delete()
        await message.answer(
            text=LEXICON_ADMIN["set_product_image"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
        await state.set_state(AddProduct.image)

    elif actual_state == AddProduct.image:
        if message.photo:
            await state.update_data(image=message.photo[-1].file_id)
        else:
            await message.answer(
                text=LEXICON_ADMIN["text_error_need_photo"],
                reply_markup=BACK_TO_ADMIN_MENU
            )
            return

        categoryes = await orm_get_categories(session)
        await message.answer(
            text=LEXICON_ADMIN["set_product_category"],
            reply_markup=get_categoryes_list_by_product(categoryes)
        )
        await state.set_state(AddProduct.category)




@admin_router.message(
        StateFilter(
            AddProduct.name,
            AddProduct.description,
            AddProduct.price,
            AddProduct.image,
        ),
    )
async def admin_add_products_messages_error(message: Message):
    """Обработка не правильных сообщений при заполнении FSM AddProduct"""
    await message.answer(
        text=LEXICON_ADMIN["error_need_photo_or_text"],
        reply_markup=BACK_TO_ADMIN_MENU
    )


@admin_router.callback_query(
        StateFilter(
            AddProduct.category,
            AddProduct.author,
            AddProduct.status,
        ),
    )
async def admin_add_products_callback(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    """Обработка всех состояний типа Callback при заполнении FSM AddProduct"""
    await callback.answer()
    actual_state = await state.get_state()
    mes = callback.data

    if actual_state == AddProduct.category:
        await callback.message.delete()
        category = mes.split("_")[-1]
        await state.update_data(category=category)
        authors = await orm_get_authors(session)
        await callback.message.answer(
            text=LEXICON_ADMIN["set_product_author"],
            reply_markup=get_authors_list_by_product(authors)
        )
        await state.set_state(AddProduct.author)

    if actual_state == AddProduct.author:
        await callback.message.delete()
        author = mes.split("_")[-1]
        await state.update_data(author=author)
        await callback.message.answer(
            text=LEXICON_ADMIN["set_product_status"],
            reply_markup=ADMIN_MENU_SELECTION_STATUS
        )
        await state.set_state(AddProduct.status)

    if actual_state == AddProduct.status:
        if not (
            mes.startswith("status_product") or mes.startswith("status_service")
        ):
            await callback.message.answer(
                text='что то не так с состоянием',
            )
            return

        await callback.message.delete()
        status = mes.split("_")[-1]
        await state.update_data(status=status)
        data = await state.get_data()
        await state.clear()
        await orm_create_product(session, data)
        await callback.message.answer(
            text=LEXICON_ADMIN["product_added"],
            reply_markup=ADMIN_MENU_SELECTION_PRODUCT
        )


@admin_router.callback_query(F.data == "admin_product_list")
async def admin_product_list_choise_category(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Выбор категории перед отображением списка продуктов"""
    await callback.answer()
    categoryes_list = await orm_get_categories(session)
    await callback.message.answer(
        text=LEXICON_ADMIN["set_category_product"],
        reply_markup=get_categoryes_list_by_product(categoryes_list)
    )


@admin_router.callback_query(F.data.startswith("product_choise_category_"))
async def admin_product_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Отображение списка продуктов в выбранной категории"""
    await callback.answer()
    category = callback.data.split("_")[-1]
    for product in await orm_get_products_by_category(session, int(category)):
        await callback.message.answer(
            text=f"<b>{product.name}\n</b>Автор: {product.author_product.name}",
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_product_warning_{product.id}",
                    "Подробнее": f"admin_product_info_{product.id}",
                }
            ),
        )
    await callback.message.answer(
        text=LEXICON_ADMIN["products_list"],
        reply_markup=ADMIN_MENU_SELECTION_PRODUCT
    )


@admin_router.callback_query(F.data.startswith("admin_product_info_"))
async def admin_product_info(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Отображение информации о товаре"""
    await callback.answer()
    product_id = callback.data.split("_")[-1]
    product = await orm_get_product_by_id(session, int(product_id))

    text = (
        f"<b>{product.name}</b>\n\n<b>Описание:</b>\n{product.description}\n\n<b>"
        f"Цена:</b> {product.price}\nАвтор: {product.author_product.name}"
    )

    await callback.message.answer_photo(
        photo=product.image,
        caption=text,
        reply_markup=ADMIN_MENU_SELECTION_PRODUCT
    )



@admin_router.callback_query(F.data.startswith("delete_product_warning_"))
async def delete_product_warning_(
    callback: CallbackQuery,
    session: AsyncSession
) -> None:
    """Предупреждение перед удалением товара"""
    await callback.answer()
    product_id = callback.data.split("_")[-1]
    product = await orm_get_product_by_id(session, int(product_id))
    await callback.message.answer(
        text=f"<b>ВНИМАНИЕ!</b>\Продукт <b>{product.name}</b> будет "
             "удалено без возможности восстановления!!!",
        reply_markup=get_callback_btns(
            btns={
                "Удалить безвозвратно": f"delete_product_{product_id}",
                "Вернуться в раздел товаров": "admin_product"
            },
            sizes=(1, 1)
        )
    )


@admin_router.callback_query(F.data.startswith("delete_product_"))
async def deleted_event(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем продукт"""
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар удалён!")
    await callback.message.answer(
        LEXICON_ADMIN["product_deleted"],
        reply_markup=ADMIN_MENU_SELECTION_PRODUCT
        )
