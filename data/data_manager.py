"""
Добавить главное меню, возможность добавлять контакты, выход из меню,
показывать весь список пользователей: почта/номер телефона, имя пользователя
*возможность удалять контакты
*поискавая система: по номеру телефона или по имени пользователя

"""
import json

phone_list = {
    "Alexander": "+7 701",
    "Kevin": "+7 702",
    "Charlie": "+7 703",
}

class DataManger(object):
    """
    Можно добавить несколько аргументов в функцию. Пока что не знаю какие аргументы могут понадобится.
    В будущем буду использовать json.
    """
    def __init__(self, list_data):
        self.list_data = list_data
    # Гланвное меню
    def main_menu(self):
        while True:
            print("1. Show all contacts")
            print("2. Add contact")
            print("3. Delete contact")
            print("4. Exit")
            choice = input("Choose an option: ")
            if choice == '1':
                self.show_contacts()
            elif choice == '2':
                self.add_users()
            elif choice == '3':
                self.delete_contact()
            elif choice == '4':
                print("Exiting from program. Goof Bye!")
                break
            else:
                print("Invalid option. Please try again.")
    # Добавление пользователей
    def add_users(self):
        name = input("Enter name: ")
        phone = input("Enter phone: ")
        self.list_data[name] = phone
        self.write_to_file()
        print(f"Contact added successfully.\n")
    # Записаь в файл, нужно изменить на json
    def write_to_file(self):
        with open("phone_list.txt", "w") as f:
            for i, (name, phone) in enumerate(self.list_data.items(), 1):
                f.write(f"{i}: {name} {phone}\n")
    # Показать все контакты
    def show_contacts(self):

        with open("phone_list.txt", "r") as f:
            for i in range(len(phone_list)):
                print(f.readline())
    # Удаление контакта
    def delete_contact(self):
        name = input("Enter the name of the contact to delete: ")
        if name in self.list_data:
            del self.list_data[name]
            self.write_to_file()
            print(f"Contact {name} deleted successfully.")
        else:
            print(f"Contact {name} not found.")

phone_book = DataManger(phone_list)
phone_book.main_menu()
