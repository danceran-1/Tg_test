from aiogram.types import ReplyKeyboardMarkup , KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



button1 = KeyboardButton(text='Выбор')
button2 = KeyboardButton(text='Еще что-то')
button_text = "Поулчить инофрмацию"



def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Повторить слова"),KeyboardButton(text="Настроить время проверки")],
            [KeyboardButton(text="Статистика")]
        ],
        resize_keyboard=True,  
        one_time_keyboard=True 
    )
    return keyboard

get_api = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1C", callback_data="oneC")],
    [InlineKeyboardButton(text="Рекламации", callback_data="complaint")],
    [InlineKeyboardButton(text="База знаний", callback_data="get_data")],
    [InlineKeyboardButton(text="Сервисное обслуживание оборудования", callback_data="service")],
    [InlineKeyboardButton(text="О компании", callback_data="inf_about_company")],
    [InlineKeyboardButton(text="Проверка вложенности", callback_data="include_in")],
    [InlineKeyboardButton(text="Техническая поддержка", callback_data="support")]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])

just_menue = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back2")]
])

projects = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Клён", callback_data="klen")],
    [InlineKeyboardButton(text="Рестинтернешнл", callback_data="restint")],
    [InlineKeyboardButton(text="Мастергласс", callback_data="mg")],
    [InlineKeyboardButton(text="Регион 50 (Проект 2015)", callback_data="project_2015")],
    [InlineKeyboardButton(text="Русский проект (Метроном)", callback_data="project_russia")],
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])

oneC = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создание Заказа Покупателя и выставление счёта.", callback_data="manage")],
    [InlineKeyboardButton(text="Создание отгрузочной накладной", callback_data="nakldnay")],
    [InlineKeyboardButton(text="Возврат от покупателя", callback_data="back_buyer")],
    [InlineKeyboardButton(text="Создание контрагента", callback_data="kontragen")],
    [InlineKeyboardButton(text="Создание номенклатуры", callback_data="numencklatura")],
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])

data_base = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Барный инвентарь", callback_data="barnyi_inventar")],
    [InlineKeyboardButton(text="Сиропы, топинги, пюре", callback_data="food")],
    [InlineKeyboardButton(text="Оборудование", callback_data="tools")],
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])

for_first = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ПодПодКатегория", callback_data="PodPod")],
    [InlineKeyboardButton(text="2 ПодПодКатегория", callback_data="second")],
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back1")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])
for_first_pod_pod = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Еще вложение", callback_data="one_more")],
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back1")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])

count = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Первый", callback_data="first")],
    [InlineKeyboardButton(text="Второй", callback_data="second")],
    [InlineKeyboardButton(text="третий", callback_data="third")],
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])



