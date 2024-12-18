from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
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
        "Мероприятия Чирковъ": "admin_events",
        "Администрирование худоожественной галереи": "admin_galery",
        "Раздел 'Керамика'": "admin_ceramic",
        "Раздел 'VR'": "admin_vr",
    },
    sizes=(1, ),
)


ADMIN_EVENT = get_callback_btns(
    btns={
        "Добавить новое мероприятие": "admin_new_enent",
        "Список мероприятий": "admin_list_event",
        "Вернуться в меню администратора": "back_admin_menu",
    },
    sizes=(1, ),
)


ADMIN_GALERY = get_callback_btns(
    btns={
        "Добавить новую работу": "admin_new_art_work",
        "Зарегестировать новго художника": "admin_new_artist",
        "Вернуться в меню администратора": "back_admin_menu",
    },
    sizes=(1, ),
)


ADMIN_CERAMIC = get_callback_btns(
    btns={
        "Управление услугами": "admin_ceramic_services",
        "Мастера и работы": "admin_ceramic_master_and_works",
        "Вернуться в меню администратора": "back_admin_menu",
    },
    sizes=(1, ),
)


ADMIN_VR = get_callback_btns(
    btns={
        "Управление ссылками": "admin_vr_links",
        "Тарифы": "admin_vr_tariffs",
        "Вернуться в меню администратора": "back_admin_menu",
    },
    sizes=(1, ),
)
