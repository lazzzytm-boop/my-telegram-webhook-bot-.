import asyncio
import logging
import os
from aiohttp import web # Обязательно для web.Application

from aiogram import Dispatcher, Bot
from aiogram.types import ParseMode

from config import BOT_TOKEN, APP_URL  # <--- Добавили импорт APP_URL
from handlers.client import router as client_router
from handlers.admin import router as admin_router
from database.db import DB as Database # <--- ИМПОРТИРУЕМ DB, НО НАЗЫВАЕМ ЕГО Database
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

async def main(): # <--- НАЧАЛО ФУНКЦИИ (БЕЗ ОТСТУПА)
    
    # ... (логирование, которое у вас было)
    # logging.basicConfig(...) 
    # logger.info("Starting bot in Webhook mode...") 

    # 1. Инициализация (ДОЛЖНА ИМЕТЬ ОДИНАКОВЫЙ ОТСТУП)
    bot = Bot(BOT_TOKEN) # <--- УДАЛИЛИ 
    dp = Dispatcher(bot) # <--- Используем Dispatcher() для обхода TypeError
    app = web.Application()

    # 46 # 2. Регистрация роутеров и Webhook
    dp.include_routers(client_router, admin_router)
    dp.startup.register(Database.on_startup)
    dp.startup.register(on_startup) 

    # Настройка Webhook-хендлера и очистка
    app.router.add_post(f'/{BOT_TOKEN}', dp.web_handler)
    app.on_startup.append(on_startup)
    
    await bot.delete_webhook(drop_pending_updates=True) # <--- Очистка Webhook
    
    # 3. Запуск веб-сервера
    runner = web.AppRunner(app)
    await runner.setup()
    
    PORT = os.environ.get("PORT", 8080) # Используем 8080 как запасной, если что-то пойдет не так
    site = web.TCPSite(runner, host='0.0.0.0', port=PORT)
    await site.start()
    await asyncio.Future()

# СИНХРОННЫЙ БЛОК ЗАПУСКА (ОБЯЗАТЕЛЬНО БЕЗ ОТСТУПА)
if __name__ == '__main__':
    # Импортируем asyncio только здесь, если он не импортирован выше
    # import asyncio
    try:
        # УБЕДИТЕСЬ, ЧТО ИМПОРТИРУЕТСЯ ВЕРСИЯ БЕЗ АРГУМЕНТА (main)
        # async.run(main()) - ВАШ КОД ИЗ СТАРОГО ЛОГА
        
        # Лучше использовать asyncio.run(main())
        asyncio.run(main()) 
    except KeyboardInterrupt:
        # Ваш обработчик прерывания
        pass
    except Exception as e:
        # Добавьте логирование, чтобы увидеть другие ошибки
        # print(f"Критическая ошибка запуска: {e}") 
        pass





























