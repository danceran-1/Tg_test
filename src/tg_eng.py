from aiogram import Bot, Dispatcher
from bot.handlers import router
from for_api.setting import API_TOKEN
import logging
import bot.handlers as hand

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    print("Бот запускается...")
  
    await dp.start_polling(bot)  

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())