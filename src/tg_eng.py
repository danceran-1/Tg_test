from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import router
from for_api.setting import API_TOKEN
import logging
import asyncio
from aiohttp import web


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
dp.include_router(router)


async def web_handler(request):
    return web.Response(text="Bot is running")

async def start_bot():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Starting polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")

async def start_web_app():
    app = web.Application()
    app.add_routes([web.get('/', web_handler)])
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", 10000).start()

async def main():
    await asyncio.gather(
        start_web_app(),
        start_bot()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")