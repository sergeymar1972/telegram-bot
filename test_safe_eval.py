import pytest
from bot import safe_eval  # импортируем функцию из bot.py

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
