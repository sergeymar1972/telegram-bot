import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Не найден BOT_TOKEN в .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Простая клавиатура с кнопкой «Калькулятор»
def get_calc_keyboard():
    kb = [
        [KeyboardButton(text="🧮 Калькулятор")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот-калькулятор.\n"
        "Нажми кнопку «🧮 Калькулятор» или используй команду /calc <выражение>.\n"
        "Пример: /calc 2 + 2",
        reply_markup=get_calc_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/help — эта справка\n"
        "/calc <выражение> — посчитать выражение\n"
        "Например: /calc 10 * 5"
    )

# Разрешённые символы для калькулятора: цифры, пробелы, + - * / . () и знаки унарного минуса
ALLOWED_CHARS = set("0123456789+-*/(). ")

def safe_eval(expr: str) -> float:
    expr = expr.strip()
    if not expr:
        raise ValueError("Пустое выражение")
    # Проверка на разрешённые символы
    for ch in expr:
        if ch not in ALLOWED_CHARS:
            raise ValueError("Недопустимые символы в выражении")
    # eval в Python всё равно опасен, но с такой проверкой риск сильно снижен
    result = eval(expr, {"__builtins__": {}}, {})
    if isinstance(result, (int, float)):
        return float(result)
    raise ValueError("Результат не является числом")

@dp.message(Command("calc"))
async def cmd_calc(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Используй так: /calc 2 + 2\nПример: /calc (10 + 5) * 2")
        return

    expr = args[1]
    try:
        result = safe_eval(expr)
        # Убираем лишние нули после запятой для красоты
        if result.is_integer():
            result_str = str(int(result))
        else:
            result_str = f"{result:.10f}".rstrip("0").rstrip(".")
        await message.answer(f"Результат: {result_str}")
    except ZeroDivisionError:
        await message.answer("Ошибка: деление на ноль!")
    except Exception as e:
        await message.answer(f"Ошибка в выражении: {e}")

# Обработка нажатия кнопки «Калькулятор» — просим ввести выражение
@dp.message(F.text)
async def echo_calc(message: types.Message):
    expr = message.text.strip()
    # Игнорируем кнопку и команды, чтобы не дублировать логику
    if expr.startswith("/") or expr == "🧮 Калькулятор":
        return

    try:
        result = safe_eval(expr)
        if result.is_integer():
            result_str = str(int(result))
        else:
            result_str = f"{result:.10f}".rstrip("0").rstrip(".")
        await message.answer(f"Результат: {result_str}")
    except ZeroDivisionError:
        await message.answer("Ошибка: деление на ноль!")
    except Exception as e:
        # Теперь бот честно скажет, что не понял
        await message.answer(f"Не могу посчитать: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
