from collections import Counter # Импортируем класс Counter из модуля collections для подсчета рейтинга игроков.
from players import Player # Импортируем базовый класс Player из модуля players.
from states import Moves # Импортируем класс Moves, который представляет ходы игроков (cheat или cooperate).

class GameError(Exception): # Определяем собственное исключение для обработки ошибок в игре.
    pass

class Game:
    def __init__(self, *, matches: int = 10):
    # Конструктор класса Game принимает количество матчей (по умолчанию 10).
        self._matches = matches
        # Сохраняем количество матчей.
        self._rating = Counter()
        # Инициализируем счетчик для хранения рейтинга игроков.

    def play(self, player1: Player, player2: Player) -> None:
        # Метод для проведения игр между двумя игроками.
        p1_prev_move = None
        # Инициализируем переменную для хранения предыдущего хода игрока 1.
        p2_prev_move = None
        # Инициализируем переменную для хранения предыдущего хода игрока 2.

        for round_ in range(1, self._matches + 1):
            # Цикл для каждого раунда игры.
            p1_move = player1.move(p2_prev_move, round_)
            # Игрок 1 делает ход, основываясь на предыдущем ходе игрока 2.
            p2_move = player2.move(p1_prev_move, round_)
            # Игрок 2 делает ход, основываясь на предыдущем ходе игрока 1.
            
            match_ = (
                f"match #{round_}: "
                f"player1_move = {p1_move} vs player2_move = {p2_move}"
            )
            # Формируем строку с описанием текущего матча.
            print(f"Match #{round_}: {player1} = {p1_move} vs {player2} = {p2_move}")

            # Определяем результаты игры на основе комбинаций ходов.
            if (p1_move, p2_move) == (Moves.cheat, Moves.cheat):
                self._rating[str(player1)] += 0
                self._rating[str(player2)] += 0
            elif (p1_move, p2_move) == (Moves.cooperate, Moves.cooperate):
                self._rating[str(player1)] += 2
                self._rating[str(player2)] += 2
            elif (p1_move, p2_move) == (Moves.cheat, Moves.cooperate):
                self._rating[str(player1)] += 3
                self._rating[str(player2)] -= 1
            elif (p1_move, p2_move) == (Moves.cooperate, Moves.cheat):
                self._rating[str(player1)] -= 1
                self._rating[str(player2)] += 3

            player1.update(p2_move, round_)
            # Обновляем игрока 1 с ходом игрока 2.
            player2.update(p1_move, round_)
            # Обновляем игрока 2 с ходом игрока 1.

            p1_prev_move = p1_move
            # Сохраняем текущий ход игрока 1 для следующего раунда.
            p2_prev_move = p2_move
            # Сохраняем текущий ход игрока 2 для следующего раунда.

        player1.reset()
        # Сбрасываем состояние игрока 1 после завершения всех раундов.
        player2.reset()
        # Сбрасываем состояние игрока 2 после завершения всех раундов.

    def top3(self) -> None:
    # Метод для вывода трех лучших игроков по результатам игр.
        rating = ""
        for rank, (player, score) in enumerate(self._rating.most_common(3), start=1):
            # Перебираем три лучших игрока и их результаты.
            rating += f"{rank}: {player} ({score})\n"
        print(rating.rstrip())
        # Печатаем рейтинг лучших игроков.