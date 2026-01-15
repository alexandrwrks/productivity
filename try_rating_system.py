"""
Сделать систему оценивания продуктивности
Внедрить эту систему в основную программу
"""

point = 0

task = [
    "Написать резюме",
    "Откликнуться на вакансии",
    "Приготовить поесть"
]

def tasks(task):
    global point
    for index, job in enumerate(task, 1):
        print(f"{index}. {job}")

    while True:
        try:
            choice = int(input("Выберите номер задачи, которую ВЫ выполнили: "))
            if 1 <= choice <= len(task):
                completed_task = task[choice - 1]
                print(f"'{completed_task}' была удалена из списка")
                del task[choice - 1]
                point += 1
                break
            else:
                print("ENTER_ERROR")
        except ValueError:
            print("ENTER_ERROR")

tasks(task)
