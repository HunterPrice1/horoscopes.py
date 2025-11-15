import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

# База данных предсказаний
HOROSCOPES = {
    "oven": {
        "today": [
            "🔥 Овен! Сегодня звезды советуют проявить инициативу. Удача на вашей стороне!",
            "🔥 Неожиданная встреча изменит ваш день. Будьте открыты новому!",
            "🔥 Энергия Марса дает силы для свершений. Не бойтесь действовать!"
        ],
        "week": [
            "📅 На неделе: финансовые вопросы решатся благоприятно. В среду - важный разговор.",
            "📅 Любовь и деньги будут в центре внимания. Пятница принесет приятный сюрприз."
        ],
        "month": [
            "🌙 Месяц начнется с профессиональных успехов. Во второй половине - время для отношений."
        ]
    },
    "telec": {
        "today": [
            "💰 Телец! Сегодня идеальный день для финансовых операций. Деньги идут к вам!",
            "💰 Проявите терпение в общении. Вечером ждет приятный отдых."
        ],
        "week": [
            "📅 Неделя принесет стабильность. Четверг - лучший день для важных решений."
        ],
        "month": [
            "🌙 Месяц обещает карьерный рост и укрепление материального положения."
        ]
    },
    "bliznecy": {
        "today": [
            "💫 Близнецы! Сегодня ждут интересные встречи и новые знакомства.",
            "💫 Общение принесет пользу. Не упустите шанс узнать что-то новое."
        ]
    },
    "rak": {
        "today": [
            "🌙 Рак! День для семьи и домашних дел. Прислушайтесь к интуиции."
        ]
    },
    "lev": {
        "today": [
            "🦁 Лев! Сегодня вы в центре внимания. Проявите творческие способности!"
        ]
    },
    "deva": {
        "today": [
            "📊 Дева! Идеальный день для планирования и организации. Детали имеют значение."
        ]
    },
    "vesy": {
        "today": [
            "⚖️ Весы! Баланс и гармония - ваши ключевые слова сегодня."
        ]
    },
    "skorpion": {
        "today": [
            "🦂 Скорпион! Тайны раскроются. Ваша проницательность на высоте."
        ]
    },
    "strelec": {
        "today": [
            "🏹 Стрелец! Путешествия и новые горизонты ждут вас. Будьте смелее!"
        ]
    },
    "kozerog": {
        "today": [
            "🐐 Козерог! Карьера и амбиции - ваш приоритет. Упорство приведет к успеху."
        ]
    },
    "vodoley": {
        "today": [
            "💧 Водолей! Инновации и нестандартные решения. Вы удивите всех!"
        ]
    },
    "ryby": {
        "today": [
            "🐠 Рыбы! День для творчества и мечтаний. Доверьтесь своей интуиции."
        ]
    }
}

# Знаки зодиака с эмодзи
ZODIAC_SIGNS = {
    "oven": "♈ Овен",
    "telec": "♉ Телец", 
    "bliznecy": "♊ Близнецы",
    "rak": "♋ Рак",
    "lev": "♌ Лев",
    "deva": "♍ Дева",
    "vesy": "♎ Весы", 
    "skorpion": "♏ Скорпион",
    "strelec": "♐ Стрелец",
    "kozerog": "♑ Козерог",
    "vodoley": "♒ Водолей",
    "ryby": "♓ Рыбы"
}

# Клавиатура для выбора знака зодиака
def get_zodiac_keyboard():
    builder = InlineKeyboardBuilder()
    for sign, name in ZODIAC_SIGNS.items():
        builder.button(text=name, callback_data=f"sign_{sign}")
    builder.adjust(3)  # 3 кнопки в ряд
    return builder.as_markup()

# Клавиатура для выбора периода
def get_period_keyboard(sign):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔮 Сегодня", callback_data=f"period_{sign}_today")
    builder.button(text="📅 Неделя", callback_data=f"period_{sign}_week") 
    builder.button(text="🌙 Месяц", callback_data=f"period_{sign}_month")
    builder.button(text="⬅️ Назад", callback_data="back_to_signs")
    builder.adjust(2)
    return builder.as_markup()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🔮 *Добро пожаловать в Zodiac Oracle!*\n\n"
        "Я помогу вам узнать, что готовят звезды. Выберите ваш знак зодиака:",
        reply_markup=get_zodiac_keyboard(),
        parse_mode="Markdown"
    )

# Обработка выбора знака зодиака
@router.callback_query(F.data.startswith("sign_"))
async def process_sign_selection(callback: CallbackQuery):
    sign = callback.data.split("_")[1]
    sign_name = ZODIAC_SIGNS.get(sign, sign)
    
    await callback.message.edit_text(
        f"✨ {sign_name}\n\nЧто вы хотите узнать?",
        reply_markup=get_period_keyboard(sign)
    )
    await callback.answer()

# Обработка выбора периода
@router.callback_query(F.data.startswith("period_"))
async def process_period_selection(callback: CallbackQuery):
    data_parts = callback.data.split("_")
    sign = data_parts[1]
    period = data_parts[2]
    
    sign_name = ZODIAC_SIGNS.get(sign, sign)
    
    # Получаем предсказание
    prediction = get_horoscope(sign, period)
    
    period_text = {
        "today": "сегодня",
        "week": "на неделе", 
        "month": "в этом месяце"
    }.get(period, period)
    
    await callback.message.edit_text(
        f"🔮 *{sign_name}* \n*{period_text.capitalize()}:*\n\n{prediction}\n\n"
        f"✨ Пусть звезды благоволят вам!",
        reply_markup=get_period_keyboard(sign),
        parse_mode="Markdown"
    )
    await callback.answer()

# Кнопка "Назад"
@router.callback_query(F.data == "back_to_signs")
async def back_to_signs(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔮 Выберите ваш знак зодиака:",
        reply_markup=get_zodiac_keyboard()
    )
    await callback.answer()

# Функция получения предсказания
def get_horoscope(sign: str, period: str) -> str:
    predictions = HOROSCOPES.get(sign, {}).get(period, [])
    if predictions:
        return random.choice(predictions)
    else:
        return "🌟 Звезды пока хранят молчание... Загляните позже!"

# Команда /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🌟 *Помощь по боту:*\n\n"
        "/start - начать работу с ботом\n"
        "/help - показать эту справку\n\n"
        "Выбирайте знак зодиака и период для получения предсказания!",
        parse_mode="Markdown"
    )

# Обработка обычных сообщений
@router.message()
async def echo_message(message: Message):
    await message.answer(
        "🔮 Используйте /start для начала работы с ботом!"
    )
