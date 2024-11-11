import sys

class Key:
    # Определяем класс Key, который будет использоваться для создания объектов ключей.
    
    def __init__(self, key_instance: str) -> None:
        # Проверка, что переданный аргумент является строкой
        if not isinstance(key_instance, str):
            raise ValueError("Первый аргумент должен быть строкой.")
        # Инициализируем приватный атрибут _passphrase строковым представлением объекта
        self._passphrase = repr(self)
        # Инициализируем атрибут _input_str значением, переданным в качестве аргумента
        self._input_str = key_instance

    def __getitem__(self, key: int):
        # Метод, который позволяет использовать объект класса Key как индексируемую коллекцию.
        return len(str(abs(key)))
        # Возвращает длину строки, представляющей абсолютное значение переданного индекса.
        # Например, для key = -123 вернется len("123") = 3.

    def __gt__(self, other: int) -> bool:
        # Метод, который определяет операцию сравнения "больше" (>) для объектов класса Key.
        return other > 9000
        # Возвращает True, если переданное значение (other) больше 9000, иначе False.

    def __len__(self) -> int:
        # Метод, который позволяет использовать встроенную функцию len() для объектов класса Key.
        return len(self._input_str)
        # Возвращает длину строки, переданной при создании объекта.

    def __str__(self) -> str:
        # Метод, который возвращает строку, переданную при создании объекта
        return self._input_str
        # Возвращает строку, которая была передана при создании объекта (первый аргумент).

    @property
    def passphrase(self) -> str:
        # Декоратор @property позволяет доступ к методу как к атрибуту (без использования скобок).
        return self._passphrase
        # Возвращает строковое представление объекта.

# Обработка ошибок при чтении аргументов командной строки
try:
    # Проверка количества переданных аргументов
    if len(sys.argv) < 4:
        raise ValueError("Необходимо передать три аргумента: строку, целое число и целое число.")

    # Чтение аргументов из командной строки
    key_instance_input = sys.argv[1]
    arg_getitem = int(sys.argv[2])  # Аргумент для метода __getitem__
    arg_gt = int(sys.argv[3])       # Аргумент для метода __gt__

    # Создание экземпляра класса Key
    key_instance = Key(key_instance_input)

    # Проверка работы метода __getitem__
    print(f"Результат key_instance[{arg_getitem}]:", key_instance[arg_getitem])

    # Проверка работы метода __gt__
    print(f"Результат key_instance > {arg_gt}:", key_instance > arg_gt)

    # Проверка работы метода __len__
    print("Результат len(key_instance):", len(key_instance))

    # Проверка работы метода __str__
    print("Результат str(key_instance):", str(key_instance))

    # Проверка работы свойства passphrase
    print("Значение passphrase:", key_instance.passphrase)

except ValueError as e:
    print("Ошибка:", e)
except Exception as e:
    print("Произошла непредвиденная ошибка:", e)
