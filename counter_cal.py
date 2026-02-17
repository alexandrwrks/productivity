"""
Счётчик калорий. Словарь с едой: название : калории(в 100 граммах).
Сделать возсожность работать с разной граммовкой еды. 
Выводить сумму калорий
Добавить БЖУ.(список: калории, белок жиры, углеводы)
Считать калорийность, белки, жиры и углеводы
"""
my_set = set()
calories_counter = {
    #Название продукта : [калории, белки, жиры, углеводы] на 100 грамм продукта
    "Гречневая каша":[101, 4, 1.1, 14.6],
    "Рисовая каша":[144, 2.4, 3.5, 25.8],
    "Макароны":[98, 3.6, 0.4, 20],
    "Куриное яйцо":[157, 12.7, 11.5, 0.7],
    "Авокадо":[160, 2, 14.6, 1.8],  
}

def calc_nutrient(food_items, food_index):

    total = 0
    for item, gram in food_items:

        if item not in calories_counter:
            if item not in my_set:
                print(f"Продукт '{item}' не найден в базе")
                my_set.add(item)
                continue
            else:
                continue
        elif gram is None or gram == 0:  
            gram = 100 

        element = (calories_counter.get(item)[food_index] / 100) * gram
        total += element
    
    return round(total, 2)
# Функции для подсчёта калорий, белка, жиров, углеводов
def calc_calories(food_items):
    return calc_nutrient(food_items, 0)
def calc_protein(food_items):
    return calc_nutrient(food_items, 1)
def calc_fats(food_items):
    return calc_nutrient(food_items, 2)
def calc_carbohedrate(food_items):
    return calc_nutrient(food_items, 3)


my_lunch = ["Макароны", "Авокадо", "Рисовая каша"]
my_lunch2 = [("Макароны", 150), ("Авокадо", 80), ("Рисовая каша", 170), ("Творог", 0)]

print(f"Калорийность продуктов - {calc_calories(my_lunch2)} ккал"
      f"(белков - {calc_protein(my_lunch2)}, жиров - {calc_fats(my_lunch2)}, углеводов - {calc_carbohedrate(my_lunch2)})")

# print(f"Каллорийность продуктов - {calc_calories(my_lunch)} ккал"
#       f"(белков - {calc_protein(my_lunch)}), жиров - {calc_fats(my_lunch2)}, углеводов - {calc_carbohedrate(my_lunch2)})")