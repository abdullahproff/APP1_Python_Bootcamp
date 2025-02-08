import threading
import time
import random

# Класс, представляющий отвертку
class Screwdriver:
    def __init__(self, id):
        self.id = id
        self.lock = threading.Lock()  # Lock для синхронизации доступа к отвертке

# Класс, представляющий Доктора
class Doctor(threading.Thread):
    def __init__(self, id, left_screwdriver, right_screwdriver, blasts_count=5):
        threading.Thread.__init__(self)
        self.id = id
        self.left_screwdriver = left_screwdriver
        self.right_screwdriver = right_screwdriver
        self.blasts_count = blasts_count  # Количество "BLAST!", которые должен выполнить Доктор

    def run(self):
        for _ in range(self.blasts_count):  # Ограничиваем количество итераций
            # Пытаемся взять обе отвертки
            with self.left_screwdriver.lock:
                with self.right_screwdriver.lock:
                    # Если удалось взять обе отвертки, выполняем взрыв
                    print(f"Doctor {self.id}: BLAST!")
                    time.sleep(random.random())  # Имитируем время выполнения взрыва
            # Отпускаем отвертки и ждем перед следующим действием
            time.sleep(random.random())
    
    #Раскомментировать код ниже для примера с бесконечным циклом
    """def run(self):
        while True:
            # Пытаемся взять обе отвертки
            with self.left_screwdriver.lock:
                with self.right_screwdriver.lock:
                    # Если удалось взять обе отвертки, выполняем взрыв
                    print(f"Doctor {self.id}: BLAST!")
                    time.sleep(random.random())  # Имитируем время выполнения взрыва
            # Отпускаем отвертки и ждем перед следующим действием
            time.sleep(random.random())"""

# Создаем отвертки
screwdrivers = [Screwdriver(i) for i in range(5)]

# Создаем Докторов и назначаем им отвертки
doctors = [
    Doctor(9, screwdrivers[0], screwdrivers[1]),
    Doctor(10, screwdrivers[1], screwdrivers[2]),
    Doctor(11, screwdrivers[2], screwdrivers[3]),
    Doctor(12, screwdrivers[3], screwdrivers[4]),
    Doctor(13, screwdrivers[4], screwdrivers[0]),
]

# Запускаем всех Докторов
for doctor in doctors:
    doctor.start()

# Ждем завершения всех потоков
for doctor in doctors:
    doctor.join()

print("Все Докторы завершили свои задачи!") #закомментировать для примера с бесконечным циклом