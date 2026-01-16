"""
Изменить структуру кода, внедрить систему оценивание,
добавить БД,
"""
ENTER_ERROR = "Некорректный ввод! Попробуйте ещё раз."

weekday = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
# productivity = {}
# task = []
# Функция для нахождения среднего значения в словаре
def average(array):
    total = 0
    for score in array.values(): # Цикл для добавления значения в переменную total
        total += score
    return total / len(array)

# Функция для нахождения дней с минимальной/максимальной продуктивностью
def extremal_days(array, find_min=True):
    first_day = list(array.keys())[0]
    max_score = array[first_day]
    max_day = first_day

    max_days = []
    for day, score in array.items():
        if score > max_score:
            max_score = score
            max_days = [day]
        elif score == max_score:
            max_days.append(day)

    if len(max_days) >= 1:
        days = ", ".join(max_days)
    else:
        days = max_days[0]
    return days, max_score

def run_productivity_tracker():
    for index, day in enumerate(weekday, 1):
        while True:  # Цикл повторения для конкретного дня
            try:
                a = float(input(f"{day}\n\tОценка продуктивности {index}-го дня недели(по шкале от 1 до 10): "))
                if a >= 1 and a <= 10:
                    productivity[day] = a # Добавление ключ-значения в словарь
                    break
                else:
                    print(f"{ENTER_ERROR}\n")
            except ValueError:
                print(ENTER_ERROR)

#avg_value = average(productivity) # Сохраняем значения функции в переменные
# max_day, max_score = find_max_day(productivity)
# min_day, min_score = find_min_day(productivity)
#
# print(f"\nСреднее значение продуктивности этой недели составило: {average(productivity):.2f}\n")
#
# if max_score and min_score == 1:
#     point = "балл"
# elif max_score and min_score > 1 and max_score and min_score < 5:
#     point = "балла"
# else:
#     point = "баллов"
# print(f"Максимальная продуктивность: {max_day} - {max_score} {point}\n"
#       f"Минимальная продуктивность: {min_day} - {min_score} {point}\n")

def add_task(task):
    job = input("Введите название задачи: ")

    task.append(job)
# Функция для удаления задач из списка
def delete_task(task):
    if not task:
        print("Ошибка: задач в списке нет")
        return
    show_task(task)
    try:
        job = int(input("Выберите номер задачи для удаления: "))
        if 1 <= job <= len(task):
            removed = task.pop(job - 1)
            print(f"Задача '{removed}' удалена\n")
        else:
            print("Неверный номер задачи")
    except ValueError:
        print("Введите число")

# Функция для выполнения задач
def complete_task(task):
    if not task:
        print("Ошибка: задач в списке нет")
        return
    show_task(task)
    try:
        job = int(input("Выберите номер задачи, которую Вы завершили: "))
        if 1 <= job <= len(task):
            removed = task.pop(job - 1)
            print(f"Задача '{removed}' завершена\n")
        else:
            print("Неверный номер задачи")
    except ValueError:
        print("Введите число")

# Функция для показа задач
def show_task(task):
    if not task:
        print("Список пуст")
        return
    else:
        for index, item in enumerate(task, 1):
            print(f"{index}. {item}")

# Основная функция для работы с задачами
def list_task(task):
    while True:
        # show_task
        print("\n"+ "="*35)
        print("\tЗадачи на сегодняшний день:")
        #4print("="*35)
        if len(task) == 0:
            print("\n\tОтсутствуют")
        else:
            for index, job in enumerate(task, 1):
                print(f"Задача №{index} - {job}")
        print("="*35)
        print("\n1. Добавить задача\n"
                "2. Завершить задачу\n"
                "3. Показать задачи\n"
                "4. Удалить задачу\n"
                "0. Выйти из меню\n")

        try:
            choice = int(input("Выберите действие: "))
        except ValueError:
            print("Пожалуйста, введите число")
            continue  # вернуться к началу цикла

        # Проверка диапазона
        if choice not in [0, 1, 2, 3, 4]:
            print("Неверный выбор. Выберите от 0 до 4")
            continue
        if choice == 1:
            add_task(task)
        elif choice == 2:
            complete_task(task)
        elif choice == 3:
            show_task(task)
        elif choice == 4:
            delete_task(task)
        elif choice == 0:
            if len(task) == 0:
                print(f"У Вас нет задач на сегодня!\n"
                      f"Хорошего дня!")
                break
            if len(task) >= 1:
                print("Список задач на сегодня:")
                show_task(task)
                print("Хорошего дня!")
                break

def main_menu():

    productivity = {}
    tasks = []

    while True:
        print("\n" + "=" * 50)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 50)
        print("1. Трекер продуктивности")
        print("2. Управление задачами")
        print("3. Выйти")

        try:
            choice = int(input("Выберите раздел: "))
        except (ValueError, KeyboardInterrupt):
            print("Некорректный ввод")
            continue

        if choice == 1:
            # Запуск трекера продуктивности
            run_productivity_tracker(productivity)
        elif choice == 2:
            # Запуск менеджера задач
            list_task(tasks)
        elif choice == 3:
            print("До свидания!")
            break
        else:
            print("Неверный выбор")


# Start program
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершила свою работу. "
              "\nДо свидания!")