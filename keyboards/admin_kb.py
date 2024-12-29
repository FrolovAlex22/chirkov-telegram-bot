from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import Author, Category, CeramicMaster
from keyboards.inline import get_callback_btns


BACK_TO_ADMIN_MENU = get_callback_btns(
    btns={
        "Вернуться в меню администратора": "back_admin_menu",
    },
    sizes=(1, ),
)


ADMIN_KB = get_callback_btns(
    btns={
        "Добавить/Изменить баннер": "add_banner",
        "Управление авторами": "admin_author",
        "Мероприятия Чирковъ": "admin_event",
    },
    sizes=(1, ),
)


# ADMIN_KB = get_callback_btns(
#     btns={
#         "Добавить/Изменить баннер": "add_banner",
#         "Мероприятия Чирковъ": "admin_events",
#         "Администрирование худоожественной галереи": "admin_galery",
#         "Раздел 'Керамика'": "admin_ceramic",
#         "Раздел 'VR'": "admin_vr",
#     },
#     sizes=(1, ),
# )


###################################### БАНЕРЫ ##################################
# Выбор после добавления банера
SELECTION_AFTER_ADDING_BANNER = get_callback_btns(
    btns={
        "Добавить баннер": "add_banner",
        "Меню администратора": "back_admin_menu",
    },
    sizes=(2,),
)


###################################### АВТОРЫ ##################################


ADMIN_MENU_SELECTION_AUTHOR = get_callback_btns(
    btns={
        "Добавить автора": "add_author",
        "Список авторов": "admin_author_list",
        "Вернуться в меню  администратора": "back_admin_menu",
    },
    sizes=(2,),
)


################################### МЕРОПРИЯТИЯ ###############################


ADMIN_MENU_SELECTION_EVENT = get_callback_btns(
    btns={
        "Добавить мероприятие": "add_event",
        "Список мероприятий": "admin_event_list",
        "Вернуться в меню  администратора": "back_admin_menu",
    },
    sizes=(2,),
)


def get_categoryes_list(
    categoryes_list: list[Category],
    sizes: tuple[int] = (1, ),
) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for category in categoryes_list:
        keyboard.add(InlineKeyboardButton(
            text=category.name,
            callback_data=f"choise_category_{category.id}"
        )
    )
    keyboard.add(InlineKeyboardButton(
        text='В меню раздела мероприятия', callback_data='admin_event')
    )
    return keyboard.adjust(*sizes).as_markup()


def get_authors_list(
    authors_list: list[Author],
    sizes: tuple[int] = (1, ),
) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for author in authors_list:
        keyboard.add(InlineKeyboardButton(
            text=author.name,
            callback_data=f"choise_author_{author.id}"
        )
    )
    keyboard.add(InlineKeyboardButton(
        text='В меню раздела мероприятия', callback_data='admin_event')
    )
    return keyboard.adjust(*sizes).as_markup()


# # EVENT
# ADMIN_EVENT = get_callback_btns(
#     btns={
#         "Добавить новое мероприятие": "admin_new_enent",
#         "Список мероприятий": "admin_list_event",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )


# # GALERY
# ADMIN_GALERY = get_callback_btns(
#     btns={
#         "Добавить новую работу": "admin_new_art_work",
#         "Зарегестировать новго художника": "admin_new_artist",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )


# # CERAMIC
# ADMIN_CERAMIC = get_callback_btns(
#     btns={
#         "Управление услугами": "admin_ceramic_services",
#         "Мастера и работы": "admin_ceramic_master_and_works",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_SERVICES = get_callback_btns(
#     btns={
#         "Добавить новую услугу": "admin_ceramic_add_service",
#         "Список услуг. Изменить/удалить": "admin_ceramic_services_list",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_SERVICES_AFTER_ADD = get_callback_btns(
#     btns={
#         "Добавить новую услугу": "admin_ceramic_add_service",
#         "Список услуг. Изменить/удалить": "admin_ceramic_services_list",
#         "Вернуться в раздел кераимки": "admin_ceramic",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_SERVICES_CANCEL = get_callback_btns(
#     btns={
#         "Отменить и вернуться в меню кераимки": "admin_ceramic",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_MASTERS = get_callback_btns(
#     btns={
#         "Управление мастерами": "admin_ceramic_master",
#         "Добавить/удалить работу": "admin_ceramic_works",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_MASTERS_CHOISE = get_callback_btns(
#     btns={
#         "Добавить нового мастера": "admin_ceramic_master_add",
#         "Список мастеров": "admin_ceramic_master_list",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_MASTERS_AFTER_ADD = get_callback_btns(
#     btns={
#         "Добавить мастера": "admin_ceramic_master_add",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_MASTERS_LIST = get_callback_btns(
#     btns={
#         "В раздел керамики": "admin_ceramic",
#         "В меню администратора": "back_admin_menu",
#     },
#     sizes=(2, ),
# )


# ADMIN_CERAMIC_WORKS = get_callback_btns(
#     btns={
#         "Добавить работу": "admin_ceramic_works_add",
#         "Список работ": "admin_ceramic_works_list",
#         "Вернуться в меню раздела керамики": "admin_ceramic",
#     },
#     sizes=(1, ),
# )


# ADMIN_CERAMIC_WORKS_AFTER_DELETE = get_callback_btns(
#     btns={
#         "Список работ": "admin_ceramic_works_list",
#         "Вернуться в меню раздела керамики": "admin_ceramic",
#     },
#     sizes=(1, ),
# )


# def get_ceramic_works_btns(
#     *,
#     masters_list: list[CeramicMaster],
#     sizes: tuple[int] = (1, ),
# ) -> InlineKeyboardBuilder:
#     keyboard = InlineKeyboardBuilder()

#     for master in masters_list:
#         keyboard.add(InlineKeyboardButton(
#             text=master.name,
#             callback_data=f"choise_master_works_{master.id}"
#         )
#     )
#     keyboard.add(InlineKeyboardButton(
#         text='В меню раздела керамики', callback_data='admin_ceramic')
#     )
#     return keyboard.adjust(*sizes).as_markup()


# def get_ceramic_masters_btns(
#     *,
#     masters_list: list[CeramicMaster],
#     sizes: tuple[int] = (1, ),
# ) -> InlineKeyboardBuilder:
#     keyboard = InlineKeyboardBuilder()

#     for master in masters_list:
#         keyboard.add(InlineKeyboardButton(
#             text=master.name,
#             callback_data=f"choise_master_work_list_{master.id}"
#         )
#     )
#     keyboard.add(InlineKeyboardButton(
#         text='В меню раздела керамики', callback_data='admin_ceramic')
#     )
#     return keyboard.adjust(*sizes).as_markup()


# # VR
# ADMIN_VR = get_callback_btns(
#     btns={
#         "Управление ссылками": "admin_vr_links",
#         "Тарифы": "admin_vr_tariffs",
#         "Вернуться в меню администратора": "back_admin_menu",
#     },
#     sizes=(1, ),
# )
