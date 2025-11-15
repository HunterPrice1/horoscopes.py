import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Используем переменную окружения или дефолтный токен
    BOT_TOKEN = "8192982527:AAF0Qvl3utxIrH9VJVhytr1t6Qo7eRmlykY"
    
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()
    
    # Простой обработчик для теста
    @dp.message()
    async def echo(message):
        await message.answer("🔮 Бот работает! Используйте /start")
    
    logger.info("Bot started successfully!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
