import asyncio
import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from openai import AsyncOpenAI
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
dp = Dispatcher()
# ...


# ================= НАСТРОЙКИ =================
TOKEN = "8226931143:AAFoQMiVJImChTzZ3Kkkhh3WAZQHZeQQDSE"
CHANNEL_ID = -1002968176550

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("✅ Бот работает!")

CITY = "Пердулянско"

# Groq API
client = AsyncOpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1"
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

# ================= AI =================
async def generate_news():
    prompt = f"""
Ты автор сатирического городского Telegram-канала новостей города {CITY}.

Напиши ОДНУ новость (2–4 предложения).

Стиль:
- максимально реалистичный
- как городские новости
- лёгкая ирония
-валюта щщщ

Темы:
- дороги, ЖКХ, цены, транспорт
- ремонты и городские проблемы
- конфликты жителей и администрации
-дтп цены на бензин в валюте ЩЩЩ 


ВАЖНО:
- не утверждай реальные факты
- это сатирический контент
-районы наваровский,Тайо, Герберта, Залужного, Людей Великого труда
- улицы имени залужного,Ромы,Наваро,людей великого труда,Сани Белого,Артема
-Пиши не так много про дороги конечно ты можеш писать но не так часто
-и не упоминай в каждом сообщении улицы делай разнобразней

Добавь 1–2 эмодзи.
"""

    response = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()

# ================= ОТПРАВКА В КАНАЛ =================
async def send_to_channel():
    try:
        news = await generate_news()

        text = f"📰 {CITY}\n\n{news}"


        await bot.send_message(chat_id=CHANNEL_ID, text=text)

        print("✔ Новость отправлена")

    except Exception as e:
        print("Ошибка:", e)

# ================= АВТО =================
async def main():
    print("Бот запущен...")

    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
    scheduler.add_job(
        lambda: asyncio.create_task(send_to_channel()),
        "interval",
        minutes=120  # можно менять
    )
    scheduler.start()

    await send_to_channel()  # первая новость сразу

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())