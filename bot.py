import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я простой бот.\n"
        "Попробуй /help или просто напиши что-нибудь."
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "/start — приветствие\n"
        "/help — эта справка\n"
        "Любой текст — я повторю его обратно (эхо)."
    )

@dp.message()
async def echo_handler(message: types.Message):
    # Эхо: повторяем текст пользователя
    await message.answer(f"Ты написал: {message.text}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
