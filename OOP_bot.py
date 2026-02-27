from products import calories_counter
from telebot import types
from bot_token import BOT_TOKEN

import telebot
import random
import threading


class HandleManager:
    def __init__(self):
        """
        Создание объектов каждой основной функции ТГ бота для удобной работы в дальнейшем. 

        """
        self.bot = telebot.TeleBot(BOT_TOKEN) 
        self.CALORIES = CaloriesManager(self.bot)
        self.REMIND = ReminderManager(self.bot)
        self.GAME = GameManager(self.bot)
        self.HELP = HelpManager(self.bot)
        self.MENU = MenuManager(self.bot)
        self._setup_handlers()

    def run(self):
        """Запуск бота!"""
        print("Бот запущен!")
        self.bot.polling(none_stop=None)

    def _setup_handlers(self):  
        """
        Хэндлер для обработки команд.
        self.название_объекта.стартовая_программа(message)
        """
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.MENU.main_menu(message)

        @self.bot.message_handler(commands=['remind'])
        def handle_remind(message):
            self.REMIND.remind(message)
        
        @self.bot.message_handler(commands=['game'])
        def handle_game(message):
            self.GAME.start_game(message)

        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            self.HELP.comand_help(message)

        @self.bot.message_handler(commands=['calories'])
        def handle_calories(message):
            self.CALORIES.parcing_text(message)
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_message(message):
            """
            Главный хэндлер для ВСЕХ сообщений от пользователя.
            
            """
            if message.text == 'Игра':
                self.bot.send_message(message.chat.id, 'Вы выбрали игру!')
                self.GAME.start_game(message)

            elif message.text == 'Напоминалка':
                self.bot.send_message(message.chat.id, 'Вы выбрали напоминалку!')
                self.bot.send_message(message.chat.id, 
                                "Введите напоминание в формате:\n\n/remind [минуты] [текст]\n\n"
                                "Пример: /remind 5 Позвонить маме")
                
            elif message.text == 'Счётчик калорий':
                self.bot.send_message(message.chat.id, 'Вы выбрали счётчик калорий')
                self.bot.send_message(message.chat.id, 
                                "Введите счётчик в формате:\n\n/calories [продукт] [грам]\n\n" \
                                "Пример: /calories макароны 150")

            elif message.text == 'Помощь':
                self.HELP.comand_help(message)

            elif message.text == 'Главное меню':
                self.MENU.main_menu(message)

            elif message.text == 'Играть снова':
                self.GAME.start_game(message)

            elif message.text in ['Камень', 'Ножницы', 'Бумага']:
                self.GAME.game(message)

            else:
                self.bot.send_message(message.chat.id, 'Пожалуйста, выберите пункт меню.')

class ReminderManager:
    """
    Команда для напоминания. 
    Пользователь вводит время в минутах и текст напоминания, 
    бот устанавливает таймер и отправляет напоминание через указанное время.
    Парсинг сообщения /remind [время в минутах] [напоминание]
    """
    def __init__(self, bot):
        self.bot = bot
        self.timers = []

    def remind(self, message):
        """
        Обработка команды /remind
        """
        try:
            args = message.text.split()
            if len(args) == 1:
                self.bot.send_message(
                    message.chat.id, 
                    f"Введите напоминание в формате:\n/remind [минуты] [текст]\n\n " \
                    "Пример: /remind 5 Позвонить маме")
                return
                  
            minutes = int(args[1])
            reminder_text = ' '.join(args[2:])

            self.bot.send_message(
                message.chat.id, 
                f"⌛ Напоминание установлено на {minutes} минут: {reminder_text}")
            
            self.set_timer(message.chat.id, minutes, reminder_text)

        except (ValueError, IndexError):
            self.bot.send_message(
                message.chat.id, 
                "⚡ Пожалуйста, введите время в минутах и текст напоминания.")
    
    def set_timer(self, chat_id : int, minutes : int, text : str):
        """
        Установка таймера
        """
        timer = threading.Timer(
            minutes * 60,
            self.send_reminder,
            args=[chat_id, text]
        )
        timer.daemon = True # Таймер завершится при выходе из программы
        timer.start()
        self.timers.append(timer)
   
    def send_reminder(self, chat_id : int, text : str):
        """
        Отправка напоминания
        """
        try:
            self.bot.send_message(chat_id, f"⏰ Напоминание: {text}")
        except Exception as e:
            print(f"Ошибка при отправке напоминания: {e}")
    
    def cancel_all_reminders(self):
        """
        Отмена всех напоминаний
        """
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()
    
class CaloriesManager:
    def __init__(self, bot):
        self.bot = bot
        self.calories_counter = calories_counter
        self.unsuitable_products = set() # Создание множества для продктов которых ещё нет в основном списке

    def send_message(self, message, result):
        """
        Вывод подсчёта КБЖУ.
        """
        self.bot.send_message(message.chat.id, 
                        f"Каллорийность продуктов - {result[3]} ккал"
                        f"(белков - {result[1]}, жиров - {result[2]}, "
                        f"углеводов - {result[0]})")
        
    def calc_nutrient(self, message, food_items):
        """
        Подсчёт КБЖУ и сохранение результатов в списов для дальнейшего вывода.
        """
        result = [0, 0, 0, 0]
        processed_items = []
        
        for item in food_items:
            if isinstance(item, str):
                processed_items.append((item.lower(), 100))
            elif isinstance(item, (tuple, list)) and len(item) == 2:
                product_name, gram = item
                processed_items.append((product_name.lower(), gram))
            else:
                self.bot.send_message(message.chat.id, f"Неверный формат продукта: {item}")

        for item, gram in processed_items:
            if item not in self.calories_counter:
                if item not in self.unsuitable_products:
                    self.bot.send_message(message.chat.id, f"Продукт '{item}' не найден в базе")
                    self.unsuitable_products.add(item)
                continue
            
            product_name = self.calories_counter[item]
            for i in range(4):
                result[i] += (product_name[i] / 100) * gram
                
        self.send_message(message, [round(x, 2) for x in result])
    
    def parcing_text(self, message):
        """
        Отправка парсинг сообщения, как должно выглядеть сообщение.
        Основная программа для "правильного" получение данных от пользователя.
        """
        result = []
        parts = message.text.split()

        if len(parts) == 1 and parts[0] == '/calories':
            self.bot.send_message(message.chat.id,
                            "Введите счётчик в формате:\n\n/calories [продукт] [грам]\n\n" \
                            "Пример: /calories макароны 150")
            return

        default_weight = []
        i = 1

        while i < len(parts):
            product = parts[i]
            grams = 100

            if i + 1 < len(parts) and parts[i + 1].isdigit():
                grams = int(parts[i + 1])
                i += 2
            else: 
                default_weight.append(product)
                i += 1
            result.append((product, grams))

        if default_weight:
            str_default = ', '.join(default_weight)
            self.bot.send_message(message.chat.id, 
                        f"Для продуктов {str_default} не был предоставлен вес из-за чего вес был изменён на 100")
        
        self.calc_nutrient(message, result)

class MenuManager:
    """
    Главное меню.
    Главное меню. Игра. Напоминалка. Помощь. 
    Обработка сообщений для каждого пункта меню.
    Обработка функций для каждой функции меню.
    """
    def __init__(self, bot):
        self.bot = bot

    def main_menu(self, message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        game = types.KeyboardButton('Игра')
        remind = types.KeyboardButton('Напоминалка')
        helper = types.KeyboardButton('Помощь')
        calories = types.KeyboardButton('Счётчик калорий')
        markup.add(game, remind)
        markup.add(calories, helper)
        self.bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)
    
class HelpManager:
    """
    Парсинг помощи, казывает на функции которые есть в боте
    """
    def __init__(self, bot):
        self.bot = bot
        
    def comand_help(self, message):
        help_text = f"Для чего нужен этот бот\n\n" \
                    f"/start - для стрта бота\n"\
                    f"/remind - напоминалка\n" \
                    f"/game - игра камень, ножницы, бумага\n\n" \
                    f"Выберите что хотите сделать" \
                    
        self.bot.send_message(message.chat.id, help_text)

class GameManager:
    """
    Создание клавиатуры в ТГ боте. Начало работы игры: случайный выбор игрока и бота.
    Функцонал победы и проигрыша.
    """
    def __init__(self, bot):
        self.bot = bot

    def start_game(self, message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        rock = types.KeyboardButton('Камень')
        scissors = types.KeyboardButton('Ножницы')
        paper = types.KeyboardButton('Бумага')
        keyboard.add(rock, scissors, paper)
        self.bot.send_message(message.chat.id, 'Выберите: ', reply_markup=keyboard)

    def game(self, message):
        list_of_choice = ['Камень', 'Ножницы', 'Бумага']
        user_choice = message.text
        bot_choice = random.choice(list_of_choice)

        self.bot.send_message(message.chat.id, f'Бот выбрал: {bot_choice}')

        if user_choice == bot_choice:
            result = 'Ничья!'
        elif(user_choice == 'Камень' and bot_choice == 'Ножницы') or \
            (user_choice == 'Ножницы' and bot_choice == 'Бумага') or \
            (user_choice == 'Бумага' and bot_choice == 'Камень'):
            result = 'Вы выиграли!'
        else:
            result = 'Вы проиграли!'
        
        self.bot.send_message(message.chat.id, result)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        play_again = types.KeyboardButton('Играть снова')
        main_menu_btn = types.KeyboardButton('Главное меню')
        keyboard.add(play_again, main_menu_btn)

        self.bot.send_message(message.chat.id, 'Хотите сыграть снова?', reply_markup=keyboard)

if __name__ == '__main__':
    bot_manager = HandleManager() # Создание объекта HandleManager()
    bot_manager.run()
