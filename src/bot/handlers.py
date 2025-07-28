import bot.keybords as kb
from aiogram import Router ,Bot,Dispatcher ,types
from aiogram.types import BotCommand
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import time ,asyncio ,random
from psycopg2 import sql, errors
from for_api.setting import API_TOKEN,ADMIN_CHAT_ID
import psycopg2,json
import pandas as pd
from for_api.setting import  DATABASE_URL

from aiogram import Bot

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton ,ReplyKeyboardMarkup,KeyboardButton

from datetime import datetime ,timedelta

from aiogram.types import FSInputFile

check = 0 

router = Router()

bot = Bot(token=API_TOKEN)

class Form(StatesGroup):
    waiting_for_login = State()
    waiting_for_time = State()

def daily_report():


    try: 
        with open("info/daily_report.json", 'r') as file:
            df = json.load(file)
        today = "2025-07-28"

        if today in df:

            report_df = pd.DataFrame(df[today])

            report = f"📊 Дневной отчёт за {today}\n\n"
            report += f"🌡 Средняя температура: {report_df['temperature'].mean():.1f}°C\n"
            report += f"💧 Средняя влажность: {report_df['humidity'].mean():.1f}%\n"
            report += f"⚠️ Средний уровень воды: {report_df['water_level'].mean():.1f} литров\n"
            report += f"\n📈 Максимальная температура: {report_df['temperature'].max():.1f}°C\n"
            report += f"📉 Минимальная влажность: {report_df['humidity'].min():.1f}%\n"

        else:
            return "нет данных"
        return report
    
    except Exception as e:
        return f"Ошибка генерации отчёта: {e}"
    
def get_two_weeks_report():
    try:
        with open("info/weekly_report.json", 'r') as file:
            data = json.load(file)
        
        # Получаем данные за последние 2 недели
        weeks = list(data.keys())[-2:] 
        result = {}
        
        for week in weeks:
            week_data = data[week]
            result[week] = {
                'dates': [day['date'] for day in week_data],
                'avg_temps': [day['avg_temperature'] for day in week_data],
                'avg_humidity': [day['avg_humidity'] for day in week_data],
                'min_water': [day['min_water_level'] for day in week_data]
            }
        
        return result
    
    except Exception as e:
        return f"Ошибка: {str(e)}"
    
def get_two_weeks_text_report():
    data = get_two_weeks_report()
    if isinstance(data, str): 
        return data
        
    report = "📅 Отчет за 2 недели:\n\n"
    
    for week, values in data.items():
        week_num = week.split('_')[1]
        report += f"Неделя {week_num}:\n"
        report += f"📅 Даты: {', '.join(values['dates'])}\n"
        report += f"🌡 Температуры: {', '.join(map(str, values['avg_temps']))}°C\n"
        report += f"💧 Влажность: {', '.join(map(str, values['avg_humidity']))}%\n"
        report += f"⚠️ Уровень воды: {', '.join(map(str, values['min_water']))}%\n\n"
    
    return report

def get_db_connection():
    return psycopg2.connect(DATABASE_URL) 


async def register_user(telegram_id: int, username: str, first_name: str, last_name: str) -> bool:
    """Вставка данных"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            sql.SQL('''
                INSERT INTO users (telegram_id, username, first_name, last_name)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (telegram_id) DO NOTHING
            '''),
            (telegram_id, username, first_name, last_name)
        )
        conn.commit()
        return cursor.rowcount > 0  # True если была вставка, False если пользователь уже существует
    except errors.UniqueViolation:
        print(f"Ошибка при регистрации:")
        return False
    finally:
        conn.close()


@router.message(CommandStart())
async def cmd_start(message: types.Message):


    asyncio.create_task(check_critical_parameters(bot))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO notification_users (user_id, chat_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET receive_alerts = TRUE
        """, (message.from_user.id, message.chat.id))
        conn.commit()
    except Exception as e:
        await message.answer("❌ Не удалось оформить подписку")
    finally:
        conn.close()

    user = message.from_user
    is_registered = await register_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    if is_registered:
        msg1 = await message.answer("✅ Вы успешно зарегистрированы!")
        await message.answer("Что хотите сделать?",reply_markup = kb.get_api)
        await asyncio.sleep(2)
        await msg1.delete()

    else:
        msg1 = await message.answer("ℹ️ Вы уже зарегистрированы в системе.")
        await message.answer("Что хотите сделать?",reply_markup = kb.get_api)
        await asyncio.sleep(2)
        await msg1.delete()

@router.message(F.text == "/myid")
async def get_chat_id(message: types.Message):
    await message.answer(f"Ваш chat_id: {message.chat.id}")


async def get_move_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """Обновляем клавиатуру"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT water_on, fan_on FROM device_states WHERE user_id = %s", (user_id,))
    state = cursor.fetchone()
    conn.close()
    
    if not state:
        water_state = False
        fan_state = False
    else:
        water_state, fan_state = state
    
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Выключить полив" if water_state else "Включить полив🚿",
                callback_data="water_off" if water_state else "water_on"
            ),
            InlineKeyboardButton(
                text="Выключить обдув" if fan_state else "Включить обдув💨",
                callback_data="fan_off" if fan_state else "fan_on"
            )
        ],
        [InlineKeyboardButton(text="<< Назад", callback_data="get_back")]
    ])



@router.callback_query(F.data.startswith("fan_"))
async def handle_fan(callback: CallbackQuery):
    action = callback.data.split("_")[1]  # "on" или "off"
    user_id = callback.from_user.id
    
    new_state_fan = (action == "on") 

    update_fan(user_id,new_state_fan)
    
    # Обновляем клавиатуру
    await callback.message.edit_reply_markup(
        reply_markup=await get_move_keyboard(user_id)
    )
    await callback.answer(f"Обдув {'включен' if new_state_fan else 'выключен'}")

@router.message(F.text == "/fan_on")
async def handle_fan_on(message: Message):
    user_id = message.from_user.id
    update_fan(user_id, True)  
    
    await message.answer(
        "Обдув включен",
        reply_markup=await get_move_keyboard(user_id)
    )

def update_fan(user_id: int, fan: bool):

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO device_states (user_id, fan_on)
        VALUES (%s, %s)
        ON CONFLICT (user_id) 
        DO UPDATE SET 
            fan_on = EXCLUDED.fan_on
    """, (user_id, fan))
    
    conn.commit()
    conn.close()

@router.callback_query(F.data.startswith("water_"))
async def handle_water(callback: CallbackQuery):
    action = callback.data.split("_")[1]  # "on" или "off"
    user_id = callback.from_user.id
    
    new_state_water = (action == "on") 

    update_water(user_id,new_state_water)
    
    # Обновляем клавиатуру
    await callback.message.edit_reply_markup(
        reply_markup=await get_move_keyboard(user_id)
    )
    await callback.answer(f"Полив {'включен' if new_state_water else 'выключен'}")

@router.message(F.text == "/water_on")
async def handle_fan_on(message: Message):
    user_id = message.from_user.id
    update_water(user_id, True)  
    
    await message.answer(
        "Полив включен",
        reply_markup=await get_move_keyboard(user_id)
    )

def update_water(user_id: int, water: bool):

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO device_states (user_id, water_on)
        VALUES (%s, %s)
        ON CONFLICT (user_id) 
        DO UPDATE SET 
            water_on = EXCLUDED.water_on
    """, (user_id, water))
    
    conn.commit()
    conn.close()

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='🚀 Запустить бота'),
        BotCommand(command='/myid', description='🆔 Узнать свой ID'),
        BotCommand(command='/water_on', description='📅 Отчет за день'),
        BotCommand(command='/fan_on', description='📆 Отчет за неделю'),
        # BotCommand(command='/help', description='❓ Помощь по командам'),
        # BotCommand(command='/stats', description='❓ Помощь по командам')
    ]
    await bot.set_my_commands(main_menu_commands)

async def check_critical_parameters(bot: Bot):
    while True:
        try:
            data = read_json_currient("info/greenhouse_data.json")
            
            # Получаем всех пользователей, которые подписаны на уведомления
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT chat_id FROM notification_users WHERE receive_alerts = TRUE")
            users = cursor.fetchall()
            conn.close()
            
            for (chat_id,) in users:
                if data['water_level'] <= 2:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Хорошо", callback_data=f"delete_water_{data['water_level']}")]
                    ])
                    
                    await bot.send_message(
                        chat_id,
                        "⚠️ КРИТИЧЕСКИЙ УРОВЕНЬ ВОДЫ!\n"
                        f"Текущий уровень: {data['water_level']}%\n"
                        "Необходимо пополнить запас воды!",
                        parse_mode="Markdown",
                        reply_markup=keyboard
                    )

                if data['temperature'] > 35:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Хорошо", callback_data=f"delete_temp_{data['temperature']}")]
                    ])
                    
                    await bot.send_message(
                        chat_id,
                        "⚠️ ВЫСОКАЯ ТЕМПЕРАТУРА!\n"
                        f"Текущая температура: {data['temperature']}°C\n"
                        "Рекомендуется включить обдув!",
                        parse_mode="Markdown",
                        reply_markup=keyboard
                    )
            
        except Exception as e:
            print(f"Ошибка при проверке параметров: {e}")
        
        await asyncio.sleep(300)

@router.callback_query(F.data.startswith("delete_"))
async def handle_delete(callback: CallbackQuery, bot: Bot):  
    await callback.message.delete()
  

def read_json_currient(file_path):
    """Текущие показатели"""
    
    try:
        with open(file_path, 'r') as file:
                json_data = json.load(file)
            
        status_df = pd.DataFrame([json_data['greenhouse_status']])
            
        print(status_df)
        print(type(status_df))

        return {
            'status_df': status_df,
            'temperature': status_df['temperature'][0],
            'humidity': status_df['humidity'][0],
            'water_level': status_df['water_level'][0]
        }
    
    except FileNotFoundError as e:
        print(f"Ошибка: Файл {file_path} не найден")
        raise
    except json.JSONDecodeError as e:
        print(f"Ошибка: Некорректный JSON в файле {file_path}")
        raise
    except KeyError as e:
        print(f"Ошибка: Отсутствует ключ {e} в JSON-структуре")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла: {e}")
        raise


#Информация о теплице

@router.callback_query((F.data == "inf"))
async def inf(callback: CallbackQuery):
    """Меню информации"""
    
    await callback.message.edit_text("Что хотите узнать?", reply_markup=kb.get_inf)
    await callback.answer()

@router.callback_query((F.data == "tempirature"))
async def tempirature(callback: CallbackQuery):
    
    data = read_json_currient("info/greenhouse_data.json")
    currient_tempirature = data['temperature']

    if currient_tempirature > 35:
        await callback.message.edit_text(f"Температура слишком большая: {currient_tempirature}°C 🆘",reply_markup=kb.just_menue_fan)
        await callback.answer(f"Внимание❗❗❗")
    else:
        await callback.message.edit_text(f"Сейчас температура составляет: {currient_tempirature}°C", reply_markup=kb.just_menue)
    await callback.answer()

@router.callback_query((F.data == "level_water"))
async def level_water(callback: CallbackQuery):
    
    data = read_json_currient("info/greenhouse_data.json")
    currient_water_level = data['water_level']

    if currient_water_level <= 2:
        await callback.message.edit_text(f"Осталось мало воды: {currient_water_level} литров",reply_markup=kb.just_menue)
        await callback.answer(f"Внимание❗❗❗")
    else:
        await callback.message.edit_text(f"Осталось воды: {currient_water_level} литров", reply_markup=kb.just_menue)
    await callback.answer()


@router.callback_query((F.data == "humidity"))
async def humidity(callback: CallbackQuery):
    
    data = read_json_currient("info/greenhouse_data.json")
    currient_humidity = data['humidity']

    if currient_humidity > 64:
        await callback.message.edit_text(f"Влажность слишком большая: {currient_humidity}%🆘",reply_markup=kb.just_menue_water_off)
        await callback.answer(f"Внимание❗❗❗")
    elif currient_humidity < 30:
        await callback.message.edit_text(f"Влажность слишком маленькая: {currient_humidity}%🆘",reply_markup=kb.just_menue_water_on)
        await callback.answer(f"Внимание❗❗❗")
    else:
        await callback.message.edit_text(f"Сейчас влажность составляет: {currient_humidity}%", reply_markup=kb.just_menue)
    await callback.answer()

@router.callback_query((F.data == "report"))
async def humidity(callback: CallbackQuery):
    await callback.message.edit_text(f"Отчет за день/неделю", reply_markup=kb.day_week)

@router.callback_query(F.data == "rep_day")
async def rep_day(callback: CallbackQuery):
    
    
    await callback.message.edit_text(
        text = daily_report(),
        reply_markup= kb.just_menue
    )
    await callback.answer()

@router.callback_query(F.data == "rep_week")
async def rep_week(callback: CallbackQuery):
    
    
    await callback.message.edit_text(
        text = get_two_weeks_text_report(),
        reply_markup= kb.just_menue
    )
    await callback.answer()

# Действие
@router.callback_query(F.data == "move")
async def menu_bd(callback: CallbackQuery):
    """Управление устройствами"""
    
    await callback.message.edit_text(
        text="Что хотите сделать?",
        reply_markup=await get_move_keyboard(callback.from_user.id)
    )
    await callback.answer()



    

# Возврат
@router.callback_query(F.data == "get_back")
async def back(callback: CallbackQuery, state:FSMContext):

    # await callback.message.delete()
    await callback.message.edit_text(
        "Здравствуйте, что бы вы хотели сделать?",
        reply_markup=kb.get_api
    )
    await callback.answer()

@router.callback_query(F.data == "get_back2")
async def back(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    await callback.message.answer(
        "Здравствуйте, что бы вы хотели сделать?",
        reply_markup=kb.get_api
    )
    await callback.answer()
    check = 1

@router.callback_query(F.data == "get_back1")
async def back(callback: CallbackQuery, state:FSMContext):
    await callback.message.edit_text(f"Что хотите узнать?", reply_markup=kb.get_inf)



