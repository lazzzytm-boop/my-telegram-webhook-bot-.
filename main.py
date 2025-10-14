import asyncio
import logging
import os
from aiohttp import web

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from config import BOT_TOKEN, APP_URL  # <--- Добавили импорт APP_URL
from handlers.client import router as client_router
from handlers.admin import router as admin_router
from database.db import DataBase


logger = logging.getLogger(__name__)

# Получаем порт от хостинга (Leapcell передает его через переменную окружения PORT)
WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = int(os.environ.get("PORT", 8080))

async def on_startup(bot: Bot):
    # Установка Webhook при запуске сервера
    await bot.set_webhook(
        f"{APP_URL}/webhook", # Ваш домен + /webhook
        drop_pending_updates=True
    )
    logger.info(f"Webhook set to: {APP_URL}/webhook")

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=f'[BOT] {u"%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"}')
    
    logger.info("Starting bot in Webhook mode...")

    # Инициализация
    dp = Dispatcher()
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    
    # Регистрация роутеров и базы данных (как было)
    dp.include_routers(client_router, admin_router)
    dp.startup.register(DataBase.on_startup)
    
    # 1. Регистрация функции установки Webhook
    dp.startup.register(on_startup) 

    # 2. Создание веб-приложения для приема POST-запросов от Telegram
    app = web.Application()
    
    # 3. Маршрут, который будет принимать все обновления от Telegram
    app.router.add_post("/webhook", dp.web_handler) 
    
    # 4. Запуск веб-сервера
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    
    await bot.delete_webhook(drop_pending_updates=True) # Очистка старых ве
    await site.start() 

    # Бот будет работать, пока сервер работает.
    await asyncio.Future() 


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopped by KeyboardInterrupt")