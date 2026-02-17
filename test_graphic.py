import matplotlib.pyplot as plt
import pandas as pd

names_list = ["Alice", "Bob", "Charlie", "David", "Eva"]
ages_list = [25, 34, 40, 30, 45]
gym_list = [4, 6, 10, 8, 20] # стаж работы в спорт зале
month = ["Feb", "Mar", "Apr", "May", "Jun"]
y = [2, 6, 4, 8, 5]
y1 = [6, 2, 5, 3, 8]
y2 = [4, 8, 3, 6, 2]
y3 = [5, 3, 8, 2, 6]

# plt.plot(month, y, color = "blue", label = "Величина прибыли")
# plt.plot(month, y1, color='red', label = "Величина убытков")
# plt.plot(names_list, ages_list, color="green", label = "Возраст тренеров")
# plt.bar(names_list, gym_list, alpha = 0.7, label = "Стаж работы в спорт зале")

vals = [24, 17, 52, 21, 35, 98]
cars = ["Ford", "Toyota", "BMW", "Audi", "Jaguar", "Hyndai"]

plt.pie(vals, labels=cars, autopct="%1.1f%%")
plt.title("Распределение марок автомоболей на дороге")
# plt.pie(y, labels=month, autopct="%1.1f%%")
# plt.title("Количество человек")


# plt.xlabel("Месяца года")
# plt.ylabel("Прибыль в тыс. руб.")
# plt.title("Прибыль за первые 5 месяцев года")

plt.legend()
plt.show()  