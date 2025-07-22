import bot.keybords as kb
from aiogram import Router ,Bot,Dispatcher
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import time ,asyncio ,random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton ,ReplyKeyboardMarkup,KeyboardButton

from datetime import datetime ,timedelta

from aiogram.types import FSInputFile

check = 0 

router = Router()

class Form(StatesGroup):
    waiting_for_login = State()
    waiting_for_time = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """При нажатии на Start"""
    
    await message.answer("Здравствуйте, что бы вы хотели узнать?", reply_markup=kb.get_api)


#МЕНЮ
@router.callback_query((F.data == "support") | (F.data == "inf_about_company") | (F.data == "service"))
async def menu_supp(callback: CallbackQuery):
    """техническая поддержка"""
    
    await callback.message.edit_text("Выберите подкатегорию", reply_markup=kb.back)
    await callback.answer()

@router.callback_query((F.data == "get_data"))
async def menu_bd(callback: CallbackQuery):
    """техническая поддержка"""
    
    await callback.message.edit_text("Выберите подкатегорию", reply_markup=kb.data_base)
    await callback.answer()

@router.callback_query((F.data == "complaint"))
async def menu_complaint(callback: CallbackQuery):
    """техническая поддержка"""
    
    await callback.message.edit_text("Выберите подкатегорию", reply_markup=kb.projects)
    await callback.answer()

@router.callback_query((F.data == "oneC"))
async def menu_complaint(callback: CallbackQuery):
    """техническая поддержка"""
  
    await callback.message.edit_text("Выберите подкатегорию", reply_markup=kb.oneC)
    await callback.answer()

@router.callback_query((F.data == "include_in"))
async def menu_complaint(callback: CallbackQuery):
    """техническая поддержка"""
   
    await callback.message.edit_text("Выберите подкатегорию", reply_markup=kb.count)
    await callback.answer()


#Подкатергории
@router.callback_query(F.data == "first")
async def ctgry_first(callback: CallbackQuery, state:FSMContext):


    await callback.message.edit_text(
        
        "Выберите подподкатегорию",
        reply_markup = kb.for_first 
    )

@router.callback_query(F.data == "PodPod")
async def ctgry_first_podPod(callback: CallbackQuery, state:FSMContext):

   
    await callback.message.edit_text(
        "Выберите подподкатегорию",
        reply_markup = kb.for_first_pod_pod 
    )

@router.callback_query((F.data == "one_more") | (F.data == "second"))
async def ctgry_first_podPod(callback: CallbackQuery, state:FSMContext):

    await callback.message.edit_text(
        "Просто проверка, ничего важного",
        reply_markup = kb.just_menue 
    )


#1c
@router.callback_query(F.data == "manage")
async def oneC_manage(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    document = FSInputFile("docs/Создание_Заказа_Покупателя_и_выставление_счёта.pdf",filename="Создание_Заказа_Покупателя_и_выставление_счёта.pdf")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Создание Заказа Покупателя и выставление счёта.",
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "nakldnay")
async def oneC_nakldnay(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    document = FSInputFile("docs/Создание отгрузочной накладной.pdf",filename="Создание отгрузочной накладной.pdf")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Создание отгрузочной накладной",
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "back_buyer")
async def oneC_back_buyer(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    document = FSInputFile("docs/Возврат от покупателя.pdf",filename="Возврат от покупателя.pdf")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Возврат от покупателя",
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "kontragen")
async def oneC_kontragen(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    document = FSInputFile("docs/Создание контрагента.pdf",filename="Создание контрагента.pdf")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Создание контрагента",
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "numencklatura")
async def oneC_numencklatura(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    document = FSInputFile("docs/Создание номенклатуры.pdf",filename="Создание номенклатуры.pdf")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Создание номенклатуры",
        reply_markup = kb.just_menue 
    )



#ЖАЛОБЫ
@router.callback_query(F.data == "klen")
async def rec_klen(callback: CallbackQuery, state:FSMContext):

    
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    with open("docs/klen.txt",'r',encoding='utf-8') as file:
        S = file.read()

    await callback.message.edit_text(
        S,
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "restint")
async def rec_hard_word(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    document = FSInputFile("docs/Рестинтернешнл.docx",filename="Рестинтернешнл.docx")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Рестинтернешнл",
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "mg")
async def rec_mg(callback: CallbackQuery, state:FSMContext):

   
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    with open("docs/мастерглас.txt",'r',encoding='utf-8') as file:
        S = file.read()

    await callback.message.edit_text(
        S,
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "project_2015")
async def rec_project_2015(callback: CallbackQuery, state:FSMContext):

    
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    with open("docs/проект_2015.txt",'r',encoding='utf-8') as file:
        S = file.read()

    await callback.message.edit_text(
        S,
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "project_russia")
async def rec_russian_prj(callback: CallbackQuery, state:FSMContext):

    
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.1)
    await msg1.delete()

    with open("docs/метраном.txt",'r',encoding='utf-8') as file:
        S = file.read()

    await callback.message.edit_text(
        S,
        reply_markup = kb.just_menue 
    )

# БАЗА ЗНАНИЙ
@router.callback_query(F.data == "barnyi_inventar")
async def bz_inventary(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.4)
    await msg1.delete()

    document = FSInputFile("docs/Барный инвентарь (3).pdf",filename="Барный инвентарь (3).pdf")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Барный инвентарь",
        reply_markup = kb.just_menue 
    )

@router.callback_query(F.data == "food")
async def bz_food(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    await asyncio.sleep(0.4)
    await msg1.delete()

    document = FSInputFile("docs/Сиропы, топинги, пюре.pdf",filename="Сиропы, топинги, пюре.pdf")

    await callback.message.answer_document(
        document=document,
        caption="Вот документ для изучения Сиропы, топинги, пюре",
        reply_markup = kb.just_menue 
    )

@router.callback_query((F.data == "tools") | (F.data == "third"))
async def bz_tools(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    msg1 = await callback.message.answer("Ожидайте... 😊")
    

# Возврат
@router.callback_query(F.data == "get_back")
async def back(callback: CallbackQuery, state:FSMContext):

    # await callback.message.delete()
    await callback.message.edit_text(
        "Здравствуйте, что бы вы хотели узнать?",
        reply_markup=kb.get_api
    )
    await callback.answer()

@router.callback_query(F.data == "get_back2")
async def back(callback: CallbackQuery, state:FSMContext):

    await callback.message.delete()
    await callback.message.answer(
        "Здравствуйте, что бы вы хотели узнать?",
        reply_markup=kb.get_api
    )
    await callback.answer()
    check = 1

@router.callback_query(F.data == "get_back1")
async def back(callback: CallbackQuery, state:FSMContext):


    await callback.message.edit_text(
        "Выберите подкатегорию",
        reply_markup=kb.count
    )



