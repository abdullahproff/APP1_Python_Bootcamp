from enum import Enum # Импортируем модуль Enum для создания перечислений (Enums).

PurseType = dict[str, int] # Определяем тип PurseType как словарь, где ключ — строка, а значение — целое число.

class PurseFields(str, Enum):# Создаем перечисление PurseFields, чтобы использовать предопределенные ключи.
    GI = "gold_ingots" # Поле GI представляет ключ для золотых слитков ("gold_ingots").

def empty() -> PurseType: # Определяем функцию empty(), которая возвращает пустой словарь типа PurseType.
    return {} # Возвращаем пустой словарь — это пустой кошелек.

def add_ingot(purse: PurseType) -> PurseType: # Определяем функцию add_ingot(), которая принимает и возвращает словарь PurseType.
    ingots = purse.get(PurseFields.GI, 0) # Получаем количество слитков, используя ключ PurseFields.GI; если его нет, возвращаем 0.
    return {PurseFields.GI.value: ingots + 1} # Возвращаем новый словарь с обновленным количеством слитков (на 1 больше).

def get_ingot(purse: PurseType) -> PurseType: # Определяем функцию get_ingot(), которая также принимает и возвращает словарь PurseType.
    ingots = purse.get(PurseFields.GI, 0) # Получаем текущее количество слитков; если их нет, возвращаем 0.
    if not ingots: # Проверяем, пуст ли кошелек (ingots == 0).
        raise ValueError("the purse is already empty") # Если пуст, вызываем ошибку ValueError с сообщением.
    return {PurseFields.GI.value: ingots - 1} # Возвращаем новый словарь, уменьшая количество слитков на 1.

if __name__ == "__main__":
    purse = empty()
    print("Начальный пустой кошелек:", purse)  # Ожидается {}

    purse = add_ingot(purse)
    print("Кошелек после добавления одного слитка:", purse)  # Ожидается {'gold_ingots': 1}

    purse = add_ingot(purse)
    print("Кошелек после добавления второго слитка:", purse)  # Ожидается {'gold_ingots': 2}

    purse = get_ingot(purse)
    print("Кошелек после забора одного слитка:", purse)  # Ожидается {'gold_ingots': 1}

    purse = get_ingot(purse)
    print("Кошелек после забора последнего слитка:", purse)  # Ожидается {}

    # Пробуем забрать слиток из пустого кошелька
    try:
        purse = get_ingot(purse)
    except ValueError as e:
        print("Ошибка при попытке забрать слиток из пустого кошелька:", e)