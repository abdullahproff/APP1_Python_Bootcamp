import abc  # Импортируем модуль для создания абстрактных классов
from random import choice  # Импортируем функцию для случайного выбора
from states import Moves  # Импортируем возможные ходы игроков

class Player(abc.ABC):  # Абстрактный базовый класс для всех игроков
    def __init__(self, *, matches: None | int = None) -> None:  # Конструктор класса игрока
        self._matches = matches  # Сохраняем количество матчей

    def __str__(self) -> str:  # Метод для строкового представления игрока
        return self.__class__.__name__  # Возвращаем имя класса игрока (например, Cheater)

    @abc.abstractmethod  # Абстрактный метод для хода игрока
    def move(self, other: None | Moves = None, round: None | int = None) -> str:
        raise NotImplementedError

    @abc.abstractmethod  # Абстрактный метод для сброса состояния игрока
    def reset(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod  # Абстрактный метод для обновления состояния игрока
    def update(self, other_move: Moves, round: None | int = None) -> None:
        raise NotImplementedError

class Cheater(Player):  # Класс игрока, который всегда жульничает
    def move(self, other: None | Moves = None, round: None | int = None) -> str:
        return Moves.cheat  # Возвращаем ход "жульничать"

    def reset(self) -> None:  # Метод для сброса состояния игрока
        return None

    def update(self, other_move: Moves, round: None | int = None) -> None:  # Метод для обновления состояния игрока
        return None

class Cooperator(Player):  # Класс игрока, который всегда сотрудничает
    def move(self, other: None | Moves = None, round: None | int = None) -> str:
        return Moves.cooperate  # Возвращаем ход "сотрудничать"

    def reset(self) -> None:  # Метод для сброса состояния игрока
        return None

    def update(self, other_move: Moves, round: None | int = None) -> None:  # Метод для обновления состояния игрока
        return None

class Copycat(Player):  # Класс игрока, который копирует ход противника
    def move(self, other: None | Moves = None, round: None | int = None) -> str:
        if round == 1:
            return Moves.cooperate  # В первом раунде всегда сотрудничает
        if not other:
            return choice([Moves.cheat, Moves.cooperate])  # Случайный ход, если нет предыдущего хода
        if other == Moves.cooperate:
            return Moves.cooperate  # Если противник сотрудничает, то тоже сотрудничаем
        return Moves.cheat  # Если противник жульничает, то жульничаем

    def reset(self) -> None:  # Метод для сброса состояния игрока
        return None

    def update(self, other_move: Moves, round: None | int = None) -> None:  # Метод для обновления состояния игрока
        return None

class Detective(Player):  # Класс игрока-детектива, который расследует
    def __init__(self) -> None:
        self._is_cheated = False  # Состояние, которое показывает, был ли игрок обманут
        self._moves = [Moves.cooperate, Moves.cheat, Moves.cooperate, Moves.cooperate]  # Начальные ходы детектива

    def move(self, other: None | Moves = None, round: None | int = None) -> str:
        if round < 1:
            raise ValueError(f"round value {round} is less than 1")  # Проверка на корректность раунда
        if round < 5:
            return self._moves[round - 1]  # В первых четырёх раундах предсказуемые ходы
        if self._is_cheated:
            return Copycat().move(other=other, round=round)  # Если был обман, копируем ход противника
        return Cheater().move(other=other, round=round)  # Если не было обмана, жульничаем

    def reset(self) -> None:
        self._is_cheated = False  # Сбрасываем состояние детектива

    def update(self, other_move: Moves, round: None | int = None) -> None:
        if other_move == Moves.cheat:
            self._is_cheated = True  # Если противник жульничает, фиксируем это

class Grudger(Player):  # Класс игрока, который мстит за обман
    def __init__(self, *, matches: None | int = None) -> None:
        super().__init__(matches=matches)
        self._strategy = Cooperator()  # Изначально игрок сотрудничает

    def move(self, other: None | Moves = None, round: None | int = None) -> str:
        return self._strategy.move(other=other, round=round)  # Делает ход в зависимости от стратегии

    def reset(self) -> None:
        self._strategy = Cooperator()  # Сброс состояния стратегии в сотрудничество

    def update(self, other_move: Moves, round: None | int = None) -> None:
        if other_move == Moves.cheat:
            self._strategy = Cheater()  # Если противник жульничает, изменяем стратегию на жульничество

class MyPlayer(Player):  # Ваш пользовательский игрок
    def __init__(self, *, matches: None | int = None) -> None:
        super().__init__(matches=matches)
        self._strategies = [Cooperator(), Cheater()]  # Стратегии игрока: сотрудничество и жульничество
        self._strategy = choice(self._strategies)  # Изначально выбираем случайную стратегию

    def move(self, other: None | Moves = None, round: None | int = None) -> str:
        return self._strategy.move(other=other, round=round)  # Выполняем ход в зависимости от выбранной стратегии

    def reset(self) -> None:
        self._strategy = choice(self._strategies)  # Сброс состояния и выбор новой стратегии

    def update(self, other_move: Moves, round: None | int = None) -> None:
        if other_move == Moves.cheat:
            self._strategy = Cheater()  # Если противник жульничает, меняем стратегию на жульничество
        else:
            strategy = choice(self._strategies)
            self._strategy = strategy  # В противном случае выбираем случайную стратегию
        if self._matches and (round + 1) == self._matches:
            self._strategy = Cheater()  # На последнем раунде всегда жульничает