import pandas as pd
import matplotlib.pyplot as plt


names_list = ["Alice", "Bob", "Charlie", "David", "Eva"]
ages_list = [25, 30, 35, 40, 45]
numbers_list = ["+1-202-555-0143", "+1-202-555-0175", "+1-202-555-0198", "+1-202-555-0126", "+1-202-555-0184"]

"""
Создать класс для работы с данными пользователей. Добавление, удаление, поиск.
Использовать pandas для хранения данных. Использовать .xlsx для хранения данных.
*csv файл тоже подойдет
"""
def add_person():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    phone_number = input("Enter phone number: ")
    
    names_list.append(name)
    ages_list.append(age)
    numbers_list.append(phone_number)
    
    print(f"Person {name} added successfully.\n")

# add_person() 

df = pd.DataFrame({"Names": names_list, 
                   "Ages": ages_list, 
                   "Phone Number": numbers_list}, 
                   index=range(1, len(names_list) + 1),
)
# Индекс будет, и у него будет название "ID"
# df.to_excel("people_data.xlsx", index=True, index_label="ID")

print(df)