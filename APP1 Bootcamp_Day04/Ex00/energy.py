import ast  # Импортируем модуль ast для безопасного преобразования строк в Python-объекты.
from itertools import zip_longest  # Импортируем zip_longest для объединения списков разной длины.

# Определяем функцию fix_wiring, которая принимает списки cables, sockets и plugs.
def fix_wiring(cables, sockets, plugs):
    return (
        f"plug {c} into {s} using {p}" if p else f"weld {c} to {s} without plug" 
        # Для каждого элемента из объединенных списков:
        # Если штекер (plug) существует, формируем строку с подключением.
        # Если штекера нет, формируем строку с привариванием кабеля.
        for c, s, p in zip_longest(cables, sockets, plugs, fillvalue=None)  
        # Объединяем списки в кортежи (cable, socket, plug), заполняя недостающие элементы значением None.
        if isinstance(c, str) and isinstance(s, str) and (p is None or isinstance(p, str))
        # Фильтруем только те элементы, где кабель (c) и розетка (s) являются строками, а штекер (p) либо None, либо строка.
    )

if __name__ == "__main__":  # Условие для запуска кода только при непосредственном выполнении скрипта.
    print("Введите данные в формате Python-списков:")
    # Инструкция для пользователя о формате ввода.
    print("Пример:\nplugs = ['plugZ', None, 'plugY', 'plugX']\nsockets = [1, 'socket1', 'socket2', 'socket3', 'socket4']\ncables = ['cable2', 'cable1', False]\n")

    try:
        # Считываем ввод пользователя для списка штекеров.
        plugs_input = input("plugs = ")
        # Считываем ввод пользователя для списка розеток.
        sockets_input = input("sockets = ")
        # Считываем ввод пользователя для списка кабелей.
        cables_input = input("cables = ")

        # Преобразуем вводимые строки в списки с помощью ast.literal_eval().
        plugs = ast.literal_eval(plugs_input)  # Преобразуем plugs.
        sockets = ast.literal_eval(sockets_input)  # Преобразуем sockets.
        cables = ast.literal_eval(cables_input)  # Преобразуем cables.

        # Проверяем, что все преобразованные объекты являются списками.
        if not all(isinstance(lst, list) for lst in [plugs, sockets, cables]):
            raise ValueError("Все входные данные должны быть списками.")  # Если нет, выбрасываем ошибку.

        # Используем функцию fix_wiring для генерации команд и выводим каждую строку.
        for command in fix_wiring(cables, sockets, plugs):  # Перебираем команды из итератора.
            print(command)  # Печатаем команду.

    except Exception as e:  # Обрабатываем любые исключения, возникшие в процессе выполнения.
        print(f"Ошибка: {e}")  # Выводим сообщение об ошибке.

