from aiogram import F, Router
from aiogram.filters import StateFilter, Command, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_maker
from database.methods import (
    orm_add_ceramic_master, orm_add_ceramic_service, orm_add_ceramic_work,
    orm_change_banner_image, orm_delete_ceramic_master,
    orm_delete_ceramic_service, orm_delete_ceramic_work, orm_get_banner,
    orm_get_ceramic_master, orm_get_ceramic_masters, orm_get_ceramic_service,
    orm_get_ceramic_services, orm_get_ceramic_work,
    orm_get_ceramic_works_by_master, orm_get_info_pages
)
from keyboards.admin_kb import (
    ADMIN_CERAMIC, ADMIN_CERAMIC_MASTERS, ADMIN_CERAMIC_MASTERS_AFTER_ADD,
    ADMIN_CERAMIC_MASTERS_CHOISE, ADMIN_CERAMIC_MASTERS_LIST,
    ADMIN_CERAMIC_SERVICES, ADMIN_CERAMIC_SERVICES_AFTER_ADD,
    ADMIN_CERAMIC_SERVICES_CANCEL, ADMIN_CERAMIC_WORKS,
    ADMIN_CERAMIC_WORKS_AFTER_DELETE, ADMIN_EVENT, ADMIN_GALERY, ADMIN_KB,
    ADMIN_VR, BACK_TO_ADMIN_MENU, SELECTION_AFTER_ADDING_BANNER,
    get_ceramic_masters_btns, get_ceramic_works_btns
)
from keyboards.inline import get_callback_btns
from lexicon.lexicon import LEXICON_ADMIN, LEXICON_CERAMICS, LEXICON_OTHER
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


# Управление баннерами
# Микро FSM для загрузки/изменения баннеров
class AddBanner(StatesGroup):
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
        f" какой страницы:\n{', '.join(pages_names)}"
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


# EVENTS
@admin_router.callback_query(F.data == "admin_events")
async def admin_events(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=LEXICON_ADMIN["event"],
        reply_markup=ADMIN_EVENT
    )


# GALERY
@admin_router.callback_query(F.data == "admin_galery")
async def admin_galery(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=LEXICON_ADMIN["galery"],
        reply_markup=ADMIN_GALERY
    )


# CERAMIC
class CeramicMaster(StatesGroup):
    name = State()


@admin_router.callback_query(F.data == "admin_ceramic")
async def admin_ceramic(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    if state:
        await state.clear()
    await callback.answer()
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_ADMIN["ceramic"],
            reply_markup=ADMIN_CERAMIC
        )
    else:
        banner = await orm_get_banner(session, page="admin")
        if not banner.image:
            await callback.message.answer(
                LEXICON_OTHER["need_banner"], reply_markup=ADMIN_KB
            )
        await callback.message.answer_photo(
            banner.image,
            caption=LEXICON_ADMIN["ceramic"],
            reply_markup=ADMIN_CERAMIC
        )


@admin_router.callback_query(F.data == "admin_ceramic_master_and_works")
async def admin_ceramic_master_and_works(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=LEXICON_CERAMICS["admin_master_and_works"],
        reply_markup=ADMIN_CERAMIC_MASTERS
    )


# ceramic: master
@admin_router.callback_query(F.data == "admin_ceramic_master")
async def admin_ceramic_master_menu(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=LEXICON_CERAMICS["admin_master"],
        reply_markup=ADMIN_CERAMIC_MASTERS_CHOISE
    )


@admin_router.callback_query(F.data == "admin_ceramic_master_add")
async def admin_ceramic_master_add(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()
    await state.set_state(CeramicMaster.name)
    if callback.message.photo:
        await callback.message.edit_caption(
            caption=LEXICON_CERAMICS["admin_master_add"],
            reply_markup=BACK_TO_ADMIN_MENU
        )
    else:
        await callback.message.answer(
            text=LEXICON_CERAMICS["admin_master_add"],
            reply_markup=BACK_TO_ADMIN_MENU
        )


@admin_router.message(CeramicMaster.name, F.text)
async def admin_ceramic_master_add_get_name(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    await orm_add_ceramic_master(session, message.text)
    await message.delete()
    await state.clear()
    await message.answer(
        text=LEXICON_CERAMICS["admin_master_add_complete"],
        reply_markup=ADMIN_CERAMIC_MASTERS_AFTER_ADD
    )


@admin_router.message(CeramicMaster.name, ~F.text)
async def admin_ceramic_master_add_get_name(
    message: Message,
):
    await message.delete()
    await message.answer(
        text=LEXICON_CERAMICS["admin_master_add_error"],
        reply_markup=BACK_TO_ADMIN_MENU
    )


@admin_router.callback_query(F.data == "admin_ceramic_master_list")
async def admin_ceramic_master_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    for master in await orm_get_ceramic_masters(session):
        await callback.message.answer(
            text=(f"{master.name}\n"
            ),
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_master_warning_{master.id}",
                }
            ),
        )
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_master_list"],
        reply_markup=ADMIN_CERAMIC_MASTERS_LIST
    )


@admin_router.callback_query(F.data.startswith("delete_master_warning_"))
async def ceramicmaster_delete_warning(
    callback: CallbackQuery,
    session: AsyncSession
) -> None:
    """Предупреждение перед удалением мастера"""
    master_id = callback.data.split("_")[-1]
    master = await orm_get_ceramic_master(session, int(master_id))
    await callback.message.answer(
        text=f"<b>ВНИМАНИЕ!</b>\n\nМастер {master.name} будет удален без"
             " возможности восстановления!!!",
        reply_markup=get_callback_btns(
            btns={
                "Удалить безвозвратно": f"delete_master_{master_id}",
                "Вернуться в раздел керамики": "admin_ceramic"
            },
            sizes=(1, 1)
        )
    )


@admin_router.callback_query(F.data.startswith("delete_master_"))
async def ceramic_master_delete(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем мастера"""
    master_id = callback.data.split("_")[-1]
    await orm_delete_ceramic_master(session, int(master_id))

    await callback.answer("Мастер удален")
    await callback.message.answer(
        LEXICON_CERAMICS["admin_master_after_delete"],
        reply_markup=ADMIN_CERAMIC_MASTERS_LIST
        )


# ceramic: works
class CeramicWorks(StatesGroup):
    title = State()
    description = State()
    price = State()
    master = State


@admin_router.callback_query(F.data == "admin_ceramic_works")
async def admin_ceramic_works(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=LEXICON_CERAMICS["admin_works"],
        reply_markup=ADMIN_CERAMIC_WORKS
    )


@admin_router.callback_query(F.data == "admin_ceramic_works_add")
async def admin_ceramic_works_add(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()
    await state.set_state(CeramicWorks.title)
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_works_add"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )


@admin_router.message(CeramicWorks.title, F.text)
async def admin_ceramic_works_add_get_title(
    message: Message,
    state: FSMContext
):
    await state.update_data(title=message.text)
    await message.delete()
    await state.set_state(CeramicWorks.description)
    await message.answer(
        text=LEXICON_CERAMICS["admin_works_add_description"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )

@admin_router.message(CeramicWorks.title, ~F.text)
async def admin_ceramic_works_add_get_title_wrong(
    message: Message,
):
    await message.delete()
    await message.answer(
        text=LEXICON_CERAMICS["admin_works_add_error"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )


@admin_router.message(CeramicWorks.description, F.text)
async def admin_ceramic_works_add_get_description(
    message: Message,
    state: FSMContext
):
    await state.update_data(description=message.text)
    await message.delete()
    await state.set_state(CeramicWorks.price)
    await message.answer(
        text=LEXICON_CERAMICS["admin_works_add_price"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )


@admin_router.message(CeramicWorks.price, F.text)
async def admin_ceramic_works_add_get_price(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    if not message.text.isdigit():
        await message.delete()
        await message.answer(
            text=LEXICON_CERAMICS["admin_works_add_error_price"],
            reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
        )
        return
    await state.update_data(price=message.text)
    await message.delete()
    mastrer_list = await orm_get_ceramic_masters(session)
    await message.answer(
        text=LEXICON_CERAMICS["admin_works_add_master"],
        reply_markup=get_ceramic_works_btns(
            masters_list=mastrer_list,
            sizes=(1, )
        )
    )
    await state.set_state(CeramicWorks.master)


@admin_router.message(CeramicWorks.price, ~F.text)
async def admin_ceramic_works_add_get_price_wrong(
    message: Message,
):
    await message.delete()
    await message.answer(
        text=LEXICON_CERAMICS["admin_works_add_error"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )


@admin_router.callback_query(F.data.startswith("choise_master_works_"))
async def admin_ceramic_works_choise_master(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    await callback.answer()
    master_id = callback.data.split("_")[-1]
    await callback.message.delete()
    data = await state.get_data()
    await orm_add_ceramic_work(
        session = session,
        title=data["title"],
        description=data["description"],
        price=int(data["price"]),
        master_id=int(master_id)
    )
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_works_add_complete"],
        reply_markup=ADMIN_CERAMIC_WORKS
    )
    await state.clear()


@admin_router.callback_query(F.data == "admin_ceramic_works_list")
async def admin_ceramic_works_list_choise_master(
    callback: CallbackQuery,
    session: AsyncSession
):
    await callback.answer()
    masters = await orm_get_ceramic_masters(session)
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_works_list_choise"],
        reply_markup=get_ceramic_masters_btns(
            masters_list=masters
        )
    )


@admin_router.callback_query(F.data.startswith("choise_master_work_list_"))
async def admin_ceramic_works_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    await callback.message.delete()
    for work in await orm_get_ceramic_works_by_master(
        session, master_id=int(callback.data.split("_")[-1])
    ):
        await callback.message.answer(
            text=f"{work.title}",
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_work_warning_{work.id}",
                }
            )
        )
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_works_list"],
        reply_markup=ADMIN_CERAMIC_MASTERS_LIST
    )


@admin_router.callback_query(F.data.startswith("delete_work_warning_"))
async def admin_ceramic_works_delete_warning(
    callback: CallbackQuery,
    session: AsyncSession
):
    await callback.answer()
    work_id = callback.data.split("_")[-1]
    work = await orm_get_ceramic_work(session, int(work_id))
    text = f"{LEXICON_CERAMICS["admin_works_delete_warning"]} {work.title}"
    await callback.message.answer(
        text,
        reply_markup=get_callback_btns(
            btns={
                "Удалить": f"delete_work_{work_id}",
                "Отменить и вернуться в раздел керамики": "admin_ceramic"
            }
        )
    )


@admin_router.callback_query(F.data.startswith("delete_work_"))
async def admin_ceramic_works_delete(
    callback: CallbackQuery,
    session: AsyncSession
):
    await callback.answer()
    work_id = callback.data.split("_")[-1]
    await orm_delete_ceramic_work(session, int(work_id))
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_works_after_delete"],
        reply_markup=ADMIN_CERAMIC_WORKS_AFTER_DELETE
    )


# ceramic: service
class CeramicService(StatesGroup):
    title = State()
    price = State()


@admin_router.callback_query(F.data == "admin_ceramic_services")
async def admin_ceramic_services(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=LEXICON_CERAMICS["admin_service_choise"],
        reply_markup=ADMIN_CERAMIC_SERVICES
    )


@admin_router.callback_query(F.data == "admin_ceramic_add_service")
async def admin_ceramic_add_service(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer()
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_service_add"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )
    await state.set_state(CeramicService.title)


@admin_router.message(CeramicService.title, F.text)
async def admin_ceramic_add_service_get_title(
    message: Message,
    state: FSMContext
):
    await state.update_data(title=message.text)
    await message.delete()
    text = (
        f"Вы ввели: <b>{message.text}</b>\n\nТеперь введите цену целым "
        "числом:"
        )
    await message.answer(
        text,
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )

    await state.set_state(CeramicService.price)


@admin_router.message(CeramicService.title, ~F.text)
async def admin_ceramic_add_service_get_title(
    message: Message,
):
    await message.delete()
    await message.answer(
        text=LEXICON_CERAMICS["admin_service_add_error"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )


@admin_router.message(CeramicService.price, F.text)
async def admin_ceramic_add_service_get_price(
    message: Message,
    state: FSMContext,
    session: AsyncSession
):
    data = await state.get_data()
    price = int(message.text)
    await message.delete()
    await orm_add_ceramic_service(session, data["title"], price)
    text = (
        f"{LEXICON_CERAMICS["admin_service_add_complete"]}Название: "
        f"{data['title']}\nЦена: {price}"
    )
    await message.answer(
        text=text,
        reply_markup=ADMIN_CERAMIC_SERVICES_AFTER_ADD
    )
    await state.clear()


@admin_router.message(CeramicService.price, ~F.text)
async def admin_ceramic_add_service_get_price(
    message: Message,
):
    await message.delete()
    await message.answer(
        text=LEXICON_CERAMICS["admin_service_add_error_price"],
        reply_markup=ADMIN_CERAMIC_SERVICES_CANCEL
    )


@admin_router.callback_query(F.data == "admin_ceramic_services_list")
async def admin_ceramic_service_list(
    callback: CallbackQuery,
    session: AsyncSession
):
    await callback.answer()
    for service in await orm_get_ceramic_services(session):
        await callback.message.answer(
            text=(f"{service.title}: {service.price} руб."
            ),
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_service_warning_{service.id}",
                }
            ),
        )
    await callback.message.answer(
        text=LEXICON_CERAMICS["admin_service_list"],
        reply_markup=ADMIN_CERAMIC_MASTERS_LIST
    )


@admin_router.callback_query(F.data.startswith("delete_service_warning_"))
async def ceramic_serice_delete_warning(
    callback: CallbackQuery,
    session: AsyncSession
) -> None:
    """Предупреждение перед удалением сервиса"""
    service_id = callback.data.split("_")[-1]
    service = await orm_get_ceramic_service(session, int(service_id))
    await callback.message.answer(
        text=f"<b>ВНИМАНИЕ!</b>\nУслуга {service.title} будет удалена без"
             " возможности восстановления!!!",
        reply_markup=get_callback_btns(
            btns={
                "Удалить безвозвратно": f"delete_service_{service_id}",
                "Вернуться в раздел керамики": "admin_ceramic"
            },
            sizes=(1, 1)
        )
    )


@admin_router.callback_query(F.data.startswith("delete_service_"))
async def ceramic_service_delete(
    callback: CallbackQuery, session: AsyncSession
) -> None:
    """Удаляем мастера"""
    service_id = callback.data.split("_")[-1]
    await orm_delete_ceramic_service(session, int(service_id))

    await callback.answer("Сервис удален")
    await callback.message.answer(
        LEXICON_CERAMICS["admin_service_after_delete"],
        reply_markup=ADMIN_CERAMIC_MASTERS_LIST
        )


# VR
@admin_router.callback_query(F.data == "admin_vr")
async def admin_vr(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=LEXICON_ADMIN["vr"],
        reply_markup=ADMIN_VR
    )
