import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота (ЗАМЕНИТЕ на новый после создания бота!)
BOT_TOKEN = "8192982527:AAF0Qvl3utxIrH9VJVhytr1t6Qo7eRmlykY"

# Создаем бота с правильными настройками
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
)
dp = Dispatcher()

# База предсказаний
HOROSCOPES = {
    "oven": ["🔥 Овен! Сегодня звезды советуют проявить инициативу!", "🔥 Овен! Удача на вашей стороне!"],
    "telec": ["💰 Телец! Идеальный день для финансовых операций!", "💰 Телец! Деньги идут к вам!"],
    "bliznecy": ["💫 Близнецы! Ждут интересные встречи!", "💫 Близнецы! Новые знакомства!"],
    "rak": ["🌙 Рак! День для семьи и домашних дел!", "🌙 Рак! Прислушайтесь к интуиции!"],
    "lev": ["🦁 Лев! Сегодня вы в центре внимания!", "🦁 Лев! Проявите творческие способности!"],
    "deva": ["📊 Дева! Идеальный день для планирования!", "📊 Дева! Детали имеют значение!"],
    "vesy": ["⚖️ Весы! Баланс и гармония!", "⚖️ Весы! Ищите компромиссы!"],
    "skorpion": ["🦂 Скорпион! Тайны раскроются!", "🦂 Скорпион! Будьте проницательны!"],
    "strelec": ["🏹 Стрелец! Новые горизонты ждут!", "🏹 Стрелец! Будьте смелее!"],
    "kozerog": ["🐐 Козерог! Карьера на первом месте!", "🐐 Козерог! Упорство приведет к успеху!"],
    "vodoley": ["💧 Водолей! Вы удивите всех!", "💧 Водолей! Инновационные решения!"],
    "ryby": ["🐠 Рыбы! День для творчества!", "🐠 Рыбы! Доверьтесь интуиции!"]
}

ZODIAC_SIGNS = {
    "oven": "♈ Овен", "telec": "♉ Телец", "bliznecy": "♊ Близнецы",
    "rak": "♋ Рак", "lev": "♌ Лев", "deva": "♍ Дева",
    "vesy": "♎ Весы", "skorpion": "♏ Скорпион", "strelec": "♐ Стрелец",
    "kozerog": "♑ Козерог", "vodoley": "♒ Водолей", "ryby": "♓ Рыбы"
}

@dp.message(Command("start"))
async def cmd_start(message: Message):
    builder = InlineKeyboardBuilder()
    for sign, name in ZODIAC_SIGNS.items():
        builder.button(text=name, callback_data=f"sign_{sign}")
    builder.adjust(3)
    
    await message.answer(
        "🔮 *Добро пожаловать в Zodiac Oracle!*\n\nВыберите ваш знак зодиака:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data.startswith("sign_"))
async def process_sign(callback: CallbackQuery):
    sign = callback.data.split("_")[1]
    prediction = random.choice(HOROSCOPES.get(sign, ["🌟 Звезды пока молчат..."]))
    sign_name = ZODIAC_SIGNS.get(sign, sign)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Выбрать другой знак", callback_data="back_to_start")
    
    await callback.message.edit_text(
        f"🔮 *{sign_name}*\n\n{prediction}\n\n✨ Пусть звезды благоволят вам!",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    builder = InlineKeyboardBuilder()
    for sign, name in ZODIAC_SIGNS.items():
        builder.button(text=name, callback_data=f"sign_{sign}")
    builder.adjust(3)
    
    await callback.message.edit_text(
        "🔮 Выберите ваш знак зодиака:",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🌟 *Помощь по боту:*\n\n"
        "/start - начать работу\n"
        "/help - показать справку\n\n"
        "Выбирайте знак зодиака для получения предсказания!"
    )

@dp.message()
async def echo(message: Message):
    await message.answer("🔮 Используйте /start для начала работы с ботом!")

async def main():
    logger.info("🚀 Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
