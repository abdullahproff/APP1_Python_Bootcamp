import random  # Для генерации случайных чисел.

def turrets_generator():
    """Функция-генератор для создания объектов Turret."""
    
    # Локальная функция для вычисления случайных черт, сумма которых равна 100.
    def generate_personality_traits():
        traits = [random.randint(0, 100) for _ in range(5)]  # Генерируем 5 случайных чисел.
        total = sum(traits)  # Суммируем их.
        return [int(trait / total * 100) for trait in traits]  # Нормализуем их до 100.

    # Генерируем новый экземпляр динамического класса.
    while True:
        # Определяем личностные черты.
        personality_traits = generate_personality_traits()
        attributes = dict(zip(
            ['neuroticism', 'openness', 'conscientiousness', 'extraversion', 'agreeableness'], 
            personality_traits
        ))

        # Методы действия.
        def shoot(self):
            print("Shooting")
        
        def search(self):
            print("Searching")
        
        def talk(self):
            print("Talking")

        # Создаем динамический класс Turret.
        Turret = type(
            "Turret",  # Имя класса.
            (object,),  # Родительский класс.
            {
                **attributes,  # Добавляем личностные черты как атрибуты класса.
                "shoot": shoot,  # Метод стрельбы.
                "search": search,  # Метод поиска.
                "talk": talk,  # Метод разговора.
            }
        )

        # Возвращаем экземпляр нового класса.
        yield Turret()

if __name__ == "__main__":
    # Создаем генератор турелей.
    generator = turrets_generator()
    
    # Генерируем несколько турелей и демонстрируем их функциональность.
    for _ in range(3):
        turret = next(generator)  # Создаем новую турель.
        print("Generated Turret:")
        print(f"Neuroticism: {turret.neuroticism}")
        print(f"Openness: {turret.openness}")
        print(f"Conscientiousness: {turret.conscientiousness}")
        print(f"Extraversion: {turret.extraversion}")
        print(f"Agreeableness: {turret.agreeableness}")
        
        # Демонстрация действий.
        turret.shoot()
        turret.search()
        turret.talk()
        print("-" * 30)
