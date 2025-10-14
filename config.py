import os

# Получаем значения из переменных окружения.
# В скобках должно быть только ИМЯ переменной, которое вы настроите на Leapcell.
BOT_TOKEN = os.environ.get("BOT_TOKEN") 
CHANNEL_URL = os.environ.get("CHANNEL_URL")  
CHANNEL_ID = os.environ.get("CHANNEL_ID")  
VERIF_CHANNEL_ID = os.environ.get("VERIF_CHANNEL_ID") 
SUPP = os.environ.get("SUPP") 
PROMO = os.environ.get("PROMO") 
APP_URL = os.environ.get("APP_URL") 

# Это значение (ID админа) можно оставить в коде
ADMIN_ID = 2051322188

# Проверка на наличие критически важных переменных
if BOT_TOKEN is None or APP_URL is None:
    raise EnvironmentError("BOT_TOKEN или APP_URL не найдены в переменных окружения.")