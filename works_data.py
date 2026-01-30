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
class DataManager():
    def init(self):
        pass

    def save_to_excel(self, filename = "people_data.xlsx"):
        df = pd.DataFrame({"Names": names_list, 
                           "Ages": ages_list, 
                           "Phone Number": numbers_list}, 
                           index=range(1, len(names_list) + 1),
        )
        df.to_excel(filename, index=True, index_label="ID")
        print(f"Data saved to {filename} successfully.\n")

    def add_person(self):
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        phone_number = input("Enter phone number: ")
        
        names_list.append(name)
        ages_list.append(age)
        numbers_list.append(phone_number)
        
        self.save_to_excel()
        
        print(f"Person {name} added successfully.\n")

    def delete_person(self):
        name = input("Введите имя для удаления: ")
        if name in names_list:
            index = names_list.index(name)
            names_list.pop(index)
            ages_list.pop(index)
            numbers_list.pop(index)
            print(f"Person {name} deleted successfully.\n")
        else:
            print(f"Person {name} not found.\n")

        self.save_to_excel()

    def show_pesons(self):
        # df = pd.DataFrame({"Names": names_list, 
        #                    "Ages": ages_list, 
        #                    "Phone Number": numbers_list}, 
        #                    index=range(1, len(names_list) + 1),
        # )
        
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