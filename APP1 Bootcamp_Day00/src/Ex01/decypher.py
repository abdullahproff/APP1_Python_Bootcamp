from sys import argv # Импортируем argv из модуля sys для работы с аргументами командной строки.


def main(strings: list[str]): 
    """The main entry point.""" # Основная функция программы, которая принимает список строк.

    for string in strings:# Проходим по каждой строке в списке strings.
        answer = "".join([word[0] for word in string.split()]) # Получаем первые буквы каждого слова в строке и объединяем их в одну строку.
        print(answer) # Выводим результат для текущей строки.

if __name__ == "__main__": 
    try:
        main(argv[1:]) # Передаем в main список аргументов командной строки (кроме имени скрипта).
    except Exception as err: # Ловим любую ошибку, если она возникнет.
        print(f"Error: {err}") # Выводим сообщение об ошибке.