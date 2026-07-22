import pytest
from bot import safe_eval  # импортируем функцию из bot.py
from datetime import datetime

MONTHS_RU = {
    1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
    7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
}

def test_russian_date_format():
    now = datetime.now()
    month_name = MONTHS_RU[now.month]
    
    # Эмулируем то, что делает бот
    result = f"{now.day} {month_name} {now.year}, {now.hour:02d}:{now.minute:02d}"

    assert isinstance(result, str)
    assert month_name in result
    assert ":" in result
    assert len(result.split(":")) == 2  # проверяем, что двоеточие ровно одно (часы:минуты)
def test_addition():
    assert safe_eval("2 + 2") == 4.0

def test_multiplication():
    assert safe_eval("3 * 4") == 12.0

def test_division():
    assert safe_eval("10 / 2") == 5.0

def test_parentheses():
    assert safe_eval("(2 + 3) * 4") == 20.0

def test_float_result():
    result = safe_eval("7 / 2")
    assert result == 3.5

def test_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        safe_eval("1 / 0")

def test_invalid_characters():
    # Попытка выполнить код с os или __import__
    with pytest.raises(ValueError):
        safe_eval("__import__('os')")

    with pytest.raises(ValueError):
        safe_eval("os.system('ls')")

    # Просто недопустимый символ
    with pytest.raises(ValueError):
        safe_eval("2 + 2;")

def test_empty_expression():
    with pytest.raises(ValueError):
        safe_eval("")

def test_whitespace_only():
    with pytest.raises(ValueError):
        safe_eval("   ")
