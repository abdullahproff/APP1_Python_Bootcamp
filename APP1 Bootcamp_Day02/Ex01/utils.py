from typing import Any, NewType  # Импортируем типы для проверки типов

NonNegativeInt = NewType("NonNegativeInt", int)  # Создаем новый тип для ненегативных целых чисел

def validate_int(value: Any) -> int:  # Проверка, является ли значение целым числом
    if not isinstance(value, int):
        raise TypeError(f"{value} is not int")  # Если это не число, выбрасываем исключение
    return value

def validate_non_negative_int(value: Any) -> NonNegativeInt:  # Проверка на ненегативное целое число
    value = validate_int(value)  # Проверяем, что это целое число
    if value < 0:
        raise ValueError(f"{value} is negative")  # Если число отрицательное, выбрасываем исключение
    return value
