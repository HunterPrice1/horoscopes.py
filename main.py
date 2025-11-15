import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers.user_handlers import router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Используем ваш токен (ЗАМЕНИТЕ НА НОВЫЙ!)
    BOT_TOKEN = "8192982527:AAF0Qvl3utxIrH9VJVhytr1t6Qo7eRmlykY"
    
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set!")
        return
    
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()
    
    # Регистрируем роутеры
    dp.include_router(router)
    
    logger.info("Bot started successfully!")
    print("🔮 Zodiac Oracle Bot is running...")
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
