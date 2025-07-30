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

get_inf = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Температура🌡", callback_data="tempirature"),
        InlineKeyboardButton(text="Влажность🌀", callback_data="humidity")
    ],
    [
        InlineKeyboardButton(text="Запас воды💧", callback_data="level_water"),
        InlineKeyboardButton(text="Отчет📗", callback_data="report")
    ],
    [
        InlineKeyboardButton(text="<< Назад", callback_data="get_back")
    ]
])

get_move_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Включить полив🚿", callback_data="water_on")],
    [InlineKeyboardButton(text="Включить обдув💨", callback_data="fan_on")],
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back")]
])

day_week = InlineKeyboardMarkup(inline_keyboard=[
    
    [
        InlineKeyboardButton(text="За день", callback_data="rep_day"),
        InlineKeyboardButton(text="За неделю", callback_data="rep_week")
    ],

    [
        InlineKeyboardButton(text="<< Назад", callback_data="get_back1"),
        InlineKeyboardButton(text="В меню ↩", callback_data="get_back")
    ]
])


get_api = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Выполнить действие", callback_data="move"),
        InlineKeyboardButton(text="Узнать информацию", callback_data="inf")
    ]
])

get_api_eng = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Perform action", callback_data="move"),
        InlineKeyboardButton(text="Find out information", callback_data="inf")
    ]
])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="<< Назад", callback_data="get_back")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back")]
])

just_menue = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back2")]
])

just_menue_fan = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Включить обдув💨", callback_data="fan_on")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back2")]
])

just_menue_water_off = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Выключить полив🚿", callback_data="water_off")],
    [InlineKeyboardButton(text="В меню ↩", callback_data="get_back2")]
])

just_menue_water_on = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Включить полив🚿", callback_data="water_on")],
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



