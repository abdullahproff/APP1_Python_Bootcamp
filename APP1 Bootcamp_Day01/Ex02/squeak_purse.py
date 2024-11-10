import argparse
from enum import Enum # Импортируем модуль Enum для создания перечислений.
from functools import wraps # Импортируем wraps из functools для сохранения метаданных декорируемых функций.
from typing import Callable # Импортируем Callable для указания типа функции.

PurseType = dict[str, int] # Определяем тип PurseType как словарь, где ключ — строка, а значение — целое число.

class PurseFields(str, Enum): # Создаем перечисление PurseFields, наследуя от str и Enum.
    GI = "gold_ingots" # Поле GI представляет ключ для золотых слитков с именем "gold_ingots".

def make_squeak(func: Callable) -> Callable: # Определяем декоратор make_squeak, принимающий функцию и возвращающий функцию.
    # Аргумент func в декораторе make_squeak имеет тип Callable, 
    # указывая, что этот аргумент — функция, которую можно вызвать.
    @wraps(func) # Используем wraps для сохранения информации о декорируемой функции.
    def _wrapper(*args): # Определяем внутреннюю функцию _wrapper, которая принимает произвольное количество аргументов.
        print("SQUEAK") # Печатаем "SQUEAK" перед вызовом декорируемой функции.
        return func(*args) # Вызываем и возвращаем результат работы декорируемой функции с переданными аргументами.

    return _wrapper # Возвращаем внутреннюю функцию _wrapper как результат работы декоратора.

@make_squeak # Применяем декоратор make_squeak к функции empty.
def empty() -> PurseType: # Определяем функцию empty, возвращающую пустой кошелек.
    return {} # Возвращаем пустой словарь, представляющий пустой кошелек.

@make_squeak # Применяем декоратор make_squeak к функции add_ingot.
def add_ingot(purse: PurseType) -> PurseType: # Определяем функцию add_ingot, принимающую и возвращающую PurseType.
   
    ingots = purse.get(PurseFields.GI, 0) # Получаем текущее количество слитков; если ключа нет, возвращаем 0.
    return {PurseFields.GI.value: ingots + 1} # Возвращаем новый словарь с увеличенным на 1 количеством слитков.

@make_squeak # Применяем декоратор make_squeak к функции get_ingot.
def get_ingot(purse: PurseType) -> PurseType: # Определяем функцию get_ingot, принимающую и возвращающую PurseType.

    ingots = purse.get(PurseFields.GI, 0) # Получаем текущее количество слитков; если ключа нет, возвращаем 0.
    if not ingots: # Проверяем, есть ли слитки в кошельке (если их 0).
        raise ValueError("the purse is already empty") # Если слитков нет, выбрасываем исключение ValueError.
    return {PurseFields.GI.value: ingots - 1} # Возвращаем новый словарь с уменьшенным на 1 количеством слитков.

    # make_squeak — это декоратор, который добавляет вывод "SQUEAK" каждый раз при вызове декорированной функции.
    # empty, add_ingot, и get_ingot — это функции для работы с кошельком, каждая из которых теперь выводит "SQUEAK" при вызове благодаря декоратору.
    # Декоратор применяется к функциям с помощью @make_squeak, что добавляет к ним поведение, определенное в декораторе, без изменения их исходного кода.


# Этот блок будет исполняться, если файл запускается напрямую
if __name__ == "__main__":
    # Создаем парсер для командной строки
    parser = argparse.ArgumentParser(description="Работа с золотыми слитками в кошельке.")
    
    # Ожидаем получение значения золотых слитков через аргументы командной строки
    parser.add_argument('gold_ingots', metavar='GI', type=int, help="Количество золотых слитков")
    
    # Разбираем аргументы командной строки
    args = parser.parse_args()

    # Преобразуем переданное количество слитков в кошелек
    purse = {PurseFields.GI.value: args.gold_ingots}
    
    # Вызовем функции с этим кошельком
    print("\nВызов empty():")
    print(empty())  # Ожидаемый вывод: "SQUEAK", затем {}

    print("\nВызов add_ingot():")
    new_purse = add_ingot(purse)
    print(new_purse)  # Ожидаемый вывод: "SQUEAK", затем {"gold_ingots": ingots + 1}

    print("\nВызов get_ingot():")
    updated_purse = get_ingot(new_purse)
    print(updated_purse)  # Ожидаемый вывод: "SQUEAK", затем {"gold_ingots": ingots - 1}