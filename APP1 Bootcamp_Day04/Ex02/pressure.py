import random  # Для генерации случайных чисел
import time    # Для задержки между измерениями


def emit_gel(step):
    """
    Генератор, который генерирует давление жидкости.
    Давление изменяется случайным образом с шагом из диапазона [0, step].
    Если давление выходит за границы, генератор завершает работу.
    """
    pressure = 50  # Начальное давление
    direction = 1  # Направление изменения давления (1 - вверх, -1 - вниз)
    while True:
        delta = random.uniform(0, step)  # Случайное изменение в пределах шага
        pressure += direction * delta  # Изменяем давление

        # Если давление выходит за границы [0, 100], генератор завершает работу
        if pressure > 100 or pressure < 0:
            return

        new_direction = yield pressure  # Возвращаем текущее давление и ожидаем новое направление

        # Если новое направление передано, обновляем его
        if new_direction is not None:
            direction = new_direction


def valve(generator, step):
    """
    Управляет потоком давления.
    Инвертирует направление изменения давления, если оно выходит за пределы [20, 80].
    Завершает работу, если давление выходит за пределы [10, 90].
    """
    pressure = next(generator)  # Инициализируем генератор и получаем первое значение
    while True:
        if pressure is None:  # Защита от случаев, если генератор завершил работу
            print("Generator stopped unexpectedly.")
            break

        print(f"Measured pressure: {pressure:.2f}")  # Вывод текущего давления

        # Проверяем, находится ли давление в критическом диапазоне
        if pressure < 10 or pressure > 90:
            print("Critical pressure detected! Emergency shutdown.")
            break

        # Проверяем, находится ли давление вне рабочего диапазона
        if pressure < 20 or pressure > 80:
            print("Pressure out of bounds! Reversing direction.")
            pressure = generator.send(-1)  # Инвертируем направление изменения давления
        else:
            pressure = next(generator)  # Читаем следующее значение

        time.sleep(0.5)  # Задержка для снижения нагрузки на CPU


if __name__ == "__main__":
    # Устанавливаем максимальный шаг
    step = 10
    # Создаем генератор давления
    pressure_generator = emit_gel(step)
    # Запускаем управление давлением
    valve(pressure_generator, step)
