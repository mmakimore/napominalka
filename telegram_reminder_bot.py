import asyncio
from datetime import datetime, time
import pytz
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
TIMEZONE = pytz.timezone("Europe/Moscow")

# Время напоминаний
REMIND_TIMES = [
    time(10, 0),  # 10:00
    time(19, 0),  # 19:00
    time(23, 0),  # 23:00
]

REMIND_TEXT = "📬 Напоминание: пора сделать рассылку!"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start для теста
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("🤖 Бот напоминаний запущен! Ты получишь напоминания по расписанию.")
    # Отправляем сразу тестовое сообщение
    await message.answer(REMIND_TEXT)

# Фоновый цикл напоминаний
async def reminder_loop():
    sent_today = set()
    while True:
        now = datetime.now(TIMEZONE)
        current_time = now.time().replace(second=0, microsecond=0)
        for remind_time in REMIND_TIMES:
            key = (now.date(), remind_time)
            if current_time == remind_time and key not in sent_today:
                await bot.send_message(CHAT_ID, REMIND_TEXT)
                sent_today.add(key)
        # очищаем старые даты
        sent_today = {k for k in sent_today if k[0] == now.date()}
        await asyncio.sleep(30)  # проверка каждые 30 секунд

async def main():
    asyncio.create_task(reminder_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
