from enum import Enum  # Импортируем Enum для создания перечислений

class Moves(str, Enum):  # Перечисление для возможных ходов
    cheat = "cheat"  # Ход "жульничать"
    cooperate = "cooperate"  # Ход "сотрудничать"
