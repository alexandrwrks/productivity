import pandas as pd
import matplotlib.pyplot as plt

# Сделать так чтобы было имя и первая буква фамилии
# Добавить посик пользоваетеля по имени
# Добавить дополнительную колонку с долговременную ходьбу в зал
# С True и False

names_list = ["Alice", "Bob", "Charlie", "David", "Eva"]
ages_list = [25, 30, 35, 40, 45]
numbers_list = ["+1-202-555-0143", "+1-202-555-0175", "+1-202-555-0198", "+1-202-555-0126", "+1-202-555-0184"]
gym_list = [True, False, True, False, True]
"""
Создать класс для работы с данными пользователей. Добавление, удаление, поиск.
Использовать pandas для хранения данных. Использовать .xlsx для хранения данных.
*csv файл тоже подойдет
"""
class DataManager():
    def init(self):
        pass

    def save_to_csv(self, filename = "people_data.csv"):
        df = pd.DataFrame({"Names": names_list, 
                           "Ages": ages_list, 
                           "Phone Number": numbers_list, 
                           "Walk in Gym": gym_list},
                           index=range(1, len(names_list) + 1),
        )
        df.to_csv(filename, index=True, index_label="ID")
        print(f"Data saved to {filename} successfully.\n")

    def add_person(self):
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        phone_number = input("Enter phone number: ")
        walk_in_gym = input("Walk in gym (True/False): ").strip().lower() == 'true'
        
        names_list.append(name)
        ages_list.append(age)
        numbers_list.append(phone_number)
        gym_list.append(walk_in_gym)
        
        self.save_to_csv()
        
        print(f"Person {name} added successfully.\n")

    def delete_person(self):
        name = input("Введите имя для удаления: ")
        if name in names_list:
            index = names_list.index(name)
            names_list.pop(index)
            ages_list.pop(index)
            numbers_list.pop(index)
            gym_list.pop(index)
            print(f"Person {name} deleted successfully.\n")
        else:
            print(f"Person {name} not found.\n")

        self.save_to_csv()

    def show_pesons(self):
        df = pd.DataFrame({"Names": names_list, 
                           "Ages": ages_list, 
                           "Phone Number": numbers_list, 
                           "Walk in Gym": gym_list},
                           index=range(1, len(names_list) + 1),
        )
        
        print(df)
    

    def start_work(self):
        while True:
            print("\nChoose an action:")
            print("1. Add person")
            print("2. Delete person")
            print("3. Show all persons")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == "1":
                self.add_person()
            elif choice == "2":
                self.delete_person()
            elif choice == "3":
                self.show_pesons()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

person_data = DataManager()
person_data.start_work()