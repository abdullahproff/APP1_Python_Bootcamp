from itertools import combinations  # Импортируем функцию для создания всех возможных пар
from random import shuffle  # Импортируем функцию для случайного перемешивания списка

from game import Game  # Импортируем класс Game для проведения игр
from players import (
    Cheater,  # Игрок, который всегда жульничает
    Cooperator,  # Игрок, который всегда сотрудничает
    Copycat,  # Игрок, который копирует ход противника
    Detective,  # Игрок, который расследует и мстит
    Grudger,  # Игрок, который мстит за обман
    MyPlayer,  # Ваш пользовательский игрок
)

if __name__ == "__main__":  # Если это главный исполняемый модуль
    num_of_matches = 10  # Устанавливаем количество матчей
    game = Game(matches=num_of_matches)  # Создаем объект игры

    players = [
        Cheater(),  # Добавляем различные типы игроков
        Cooperator(),
        Copycat(),
        Detective(),
        Grudger(),
    ]
    shuffle(players)  # Перемешиваем список игроков случайным образом

    pairs = combinations(players, 2)  # Создаем все возможные пары игроков
    for player1, player2 in pairs:  # Перебираем каждую пару
        print(f"pair = {(player1, player2)}")  # Выводим информацию о паре игроков
        game.play(player1, player2)  # Играем матч между двумя игроками
        game.top3()  # Выводим топ-3 игроков после игры
