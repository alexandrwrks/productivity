list_task = []

class TaskBoard(object):
    """
    Класс для управления списком задач
    Показывать задачи, добавлять задачи, удалять задачи, завершать задачи.
    Главное меню для работы с задачами.
    Добавить возможность добавлять здачи в файл(текстовый) или json.
    """
    def __init__(self, task):
        self.task = task

    def show_task(self):
        if not self.task:
            return f"Список пуст"
        else:
            for number, exercise in enumerate(self.task, 1):
                print(f"{number}. {exercise}")

    def add_task(self):

        exercise = input("ВВедите название задачи: ")
        self.task.append(exercise)

    def delete_task(self):
        if not self.task:
            print("Ошибка: задач нет в списке")
            return
        self.show_task()
        try:
            exercise = int(input("Выберите номер задачи для удаления:"))
            if 1<= exercise <= len(self.task):
                removed = self.task.pop(exercise - 1)
                print(f"Задача '{removed}' удалена.")
            else:
                print("Неверный номер задачи.")
        except ValueError:
            print("Введите число")
            return
    
    def complete_task(self):
        if not self.task:
            print("Ошибка: задач в списке нет")
            return
        try:
            exercise = int(input("Выберите номер завершённой задачи: "))
            if 1<= exercise <= len(self.task):
                removed = self.task.pop(exercise - 1)
                print(f"Задача '{removed}' выполнена.")
            else:
                print("Неверный номер задачи.")
        except ValueError:
            print("Введите число")
            return
        
    def main_list_task(self):
        while True:
            print("\n"+ "="*35)
            print("\tЗадачи на сегодняшний день:")
            if len(self.task) == 0:
                print("\n\tОтсутствуют")
            else:
                for index, exercise in enumerate(self.task, 1):
                    print(f"Задача №{index} - {exercise}")
            print("="*35)
            print("\n1. Добавить задача\n"
                    "2. Завершить задачу\n"
                    "3. Показать задачи\n"
                    "4. Удалить задачу\n"
                    "0. Выйти в главное меню\n")

            try:
                choice = int(input("Выберите действие: "))
            except ValueError:
                print("Пожалуйста, введите число")
                continue

            # Проверка диапазона
            if choice not in [0, 1, 2, 3, 4]:
                print("Неверный выбор. Выберите от 0 до 4")
                continue
            if choice == 1:
                self.add_task()
            elif choice == 2:
                self.complete_task()
            elif choice == 3:
                self.show_task()
            elif choice == 4:
                self.delete_task()
            elif choice == 0:
                if len(self.task) == 0:
                    print(f"У Вас нет задач на сегодня!\n"
                        f"Хорошего дня!")
                    break
                if len(self.task) >= 1:
                    print("Список задач на сегодня:")
                    self.show_task()
                    print("Хорошего дня!")
                    break

task_board = TaskBoard(list_task)
task_board.main_list_task()


