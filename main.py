import asyncio
import logging
import os
from aiohttp import web # Обязательно для web.Application

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode

from config import BOT_TOKEN, APP_URL  # <--- Добавили импорт APP_URL
from handlers.client import router as client_router
from handlers.admin import router as admin_router
from database.db import DataBase
# # 2. Создание веб-приложения для приёма POST-запросов от Telegram
app = web.Application()  # ⬅️ Теперь Gunicorn его видит!

def main(async_loop: asyncio.AbstractEventLoop):
    # ... (здесь остальной код, который был в main)
    pass

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
 # # Инициализация (ДОБАВИТЬ ЭТО)
dp = Dispatcher(bot)
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
app = web.Application() # <- Создание веб-приложения AIOHTTP                                                                                                                                                          
# Инициализация
dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

# Регистрация роутеров и базы данных (как было)
dp.include_routers(client_router, admin_router)
dp.startup.register(DataBase.on_startup)
    
# 1. Регистрация функции установки Webhook
dp.startup.register(on_startup) 
# Хэндлер, который будет принимать обновления (ЭТО НУЖНО ДОБАВИТЬ)
app.router.add_post(f'/{BOT_TOKEN}', dp.web_handler)   

runner = web.AppRunner(app)
await runner.setup()
# *** ОБЯЗАТЕЛЬНО: указываем порт 8080 ***
site = web.TCPSite(runner, host='0.0.0.0', port=8080) 
await site.start() 
await asyncio.Future()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass













