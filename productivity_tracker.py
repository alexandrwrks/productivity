"""
Пережделанный код main.py с добавлением классов 
"""

class ProductivityFunction(object):
    def __init__(self, productivity, weekday, ENTER_ERROR):
        self.productivity = productivity
        self.weekday = weekday
        self.ENTER_ERROR = ENTER_ERROR

    # Функция для нахождения среднего значения в словаре
    def average(self):
        total = 0
        for score in self.productivity.values(): # Цикл для добавления значения в переменную total
            total += score
        return total / len(self.productivity)

    # Функция для нахождения дней с минимальной/максимальной продуктивностью
    def extremal_days(self, find_min=True):
        first_day = list(self.productivity.keys())[0]
        extreme_score = self.productivity[first_day]
        extreme_days = [first_day]

        for day, score in self.productivity.items():
            if (find_min and score < extreme_score) or (not find_min and score > extreme_score):
                extreme_score = score
                extreme_days = [day]
            elif score == extreme_score and day != first_day:
                extreme_days.append(day)

        if len(extreme_days) >= 1:
            days = ", ".join(extreme_days)
        else:
            days = extreme_days[0]
        return days, extreme_score
    
    # Функция для старта трекера продуктивности
    def run_productivity_tracker(self):
        for index, day in enumerate(self.weekday, 1):
            while True:  # Цикл повторения для конкретного дня
                try:
                    a = float(input(f"{day}\n\tОценка продуктивности {index}-го дня недели(по шкале от 1 до 10): "))
                    if a >= 1 and a <= 10:
                        self.productivity[day] = a # Добавление ключ-значения в словарь
                        break
                    else:
                        print(f"{self.ENTER_ERROR}\n")
                except ValueError:
                    print(self.ENTER_ERROR)

        avg = self.average()
        print(f"\nСреднее значение продуктивности этой недели составило: {avg:.2f}\n")

        max_day, max_score = self.extremal_days(find_min = False)
        min_day, min_score = self.extremal_days(find_min = True)

        if max_score and min_score == 1:
            point = "балл"
        elif 1 < max_score and min_score <= 5:
            point = "балла"
        else:
            point = "баллов"
        print(f"Максимальная продуктивность: {max_day} - {max_score} {point}\n"
            f"Минимальная продуктивность: {min_day} - {min_score} {point}\n")

productivity_function = ProductivityFunction(
    productivity = {},
    weekday = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
    ENTER_ERROR = "Ошибка ввода! Пожалуйста, введите число от 1 до 10.")

