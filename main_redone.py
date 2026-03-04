"""
Пережделанный код main.py с добавлением классов 
"""

import task_manager as tm
import productivity_tracker as pt

def main_menu():

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
            pt.productivity_function.run_productivity_tracker()
        elif choice == 2:
            # Запуск менеджера задач
            tm.task_board.main_list_task()
        elif choice == 3:
            print("До свидания!")
            break
        else:
            print("Неверный выбор")
main_menu()