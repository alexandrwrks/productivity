from products import calories_counter
from telebot import types
from bot_token import BOT_TOKEN

import telebot
import random
import threading

bot = telebot.TeleBot(BOT_TOKEN)
my_set_products = set() # Создание множества для продктов которых ещё нет в основном списке


@bot.message_handler(commands=['start'])
def main_menu(message):
    
    """
    Главное меню.
    Главное меню. Игра. Напоминалка. Помощь. 
    Обработка сообщений для каждого пункта меню.
    Обработка функций для каждой функции меню.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    game = types.KeyboardButton('Игра')
    remind = types.KeyboardButton('Напоминалка')
    helper = types.KeyboardButton('Помощь')
    calories = types.KeyboardButton('Счётчик калорий')
    markup.add(game, remind)
    markup.add(calories, helper)
    bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)
    

@bot.message_handler(commands=['remind'])
def remind(message):
    """
    Команда для напоминания. 
    Пользователь вводит время в минутах и текст напоминания, 
    бот устанавливает таймер и отправляет напоминание через указанное время.
    Парсинг сообщения /remind [время в минутах] [напоминание]
    """
    try:
        args = message.text.split()
        if len(args) == 1:
            bot.send_message(message.chat.id, 
                            f"Введите напоминание в формате:\n/remind [минуты] [текст]\n\n " \
                            "Пример: /remind 5 Позвонить маме")
            return
        minutes = int(args[1])
        reminder_text = ' '.join(args[2:])
        bot.send_message(message.chat.id, f"⌛ Напоминание установлено на {minutes} минут: {reminder_text}")

        # Запуск таймера для отправки напоминания
        timer = threading.Timer(minutes * 60, send_reminder, args=[message.chat.id, reminder_text])
        timer.start()

    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "⚡ Пожалуйста, введите время в минутах и текст напоминания.")

@bot.message_handler(commands=['help'])
def comand_help(message):
    help_text = f"Для чего нужен этот бот\n\n" \
                f"/start - для стрта бота\n"\
                f"/remind - напоминалка\n" \
                f"/game - игра камень, ножницы, бумага\n\n" \
                f"Выберите что хотите сделать" \
                
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['calories'])
def parcing_text(message):
    result = []
    
    parts = message.text.split()

    if len(parts) == 1 and parts[0] == '/calories':
        bot.send_message(message.chat.id,
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
        bot.send_message(message.chat.id, 
                    f"Для продуктов {str_default} не был предоставлен вес из-за чего вес был изменён на 100")
    
    calc_nutrient(message, result)

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    if message.text == 'Игра' or message.text == '/game':
        bot.send_message(message.chat.id, 'Вы выбрали игру!')
        start_game(message)

    elif message.text == 'Напоминалка':
        bot.send_message(message.chat.id, 'Вы выбрали напоминалку!')
        bot.send_message(message.chat.id, 
                        "Введите напоминание в формате:\n\n/remind [минуты] [текст]\n\n"
                        "Пример: /remind 5 Позвонить маме")
        
    elif message.text == 'Счётчик калорий':
        bot.send_message(message.chat.id, 'Вы выбрали счётчик калорий')
        bot.send_message(message.chat.id, 
                        "Введите счётчик в формате:\n\n/calories [продукт] [грам]\n\n" \
                        "Пример: /calories макароны 150")

    elif message.text == 'Помощь':
        comand_help(message)

    elif message.text == 'Главное меню':
        main_menu(message)

    elif message.text == 'Играть снова':
        start_game(message)

    elif message.text in ['Камень', 'Ножницы', 'Бумага']:
        game(message)

    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите пункт меню.')

def start_game(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rock = types.KeyboardButton('Камень')
    scissors = types.KeyboardButton('Ножницы')
    paper = types.KeyboardButton('Бумага')
    keyboard.add(rock, scissors, paper)
    bot.send_message(message.chat.id, 'Выберите: ', reply_markup=keyboard)

def game(message):
    list_of_choice = ['Камень', 'Ножницы', 'Бумага']
    user_choice = message.text
    bot_choice = random.choice(list_of_choice)

    bot.send_message(message.chat.id, f'Бот выбрал: {bot_choice}')

    if user_choice == bot_choice:
        result = 'Ничья!'
    elif(user_choice == 'Камень' and bot_choice == 'Ножницы') or \
        (user_choice == 'Ножницы' and bot_choice == 'Бумага') or \
        (user_choice == 'Бумага' and bot_choice == 'Камень'):
        result = 'Вы выиграли!'
    else:
        result = 'Вы проиграли!'
    
    bot.send_message(message.chat.id, result)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    play_again = types.KeyboardButton('Играть снова')
    main_menu_btn = types.KeyboardButton('Главное меню')
    keyboard.add(play_again, main_menu_btn)
    bot.send_message(message.chat.id, 'Хотите сыграть снова?', reply_markup=keyboard)

def send_reminder(chat_id, text):
    bot.send_message(chat_id, f"⏰ Напоминание: {text}")
 

# def calorie_counter(message):
    """
    Фнкция для подсчета калорий. Пользователь вводит блюдо и количество, бот возвращает калорийность и БЖУ.

    /calorie [блюдо] [вес в граммах]
    Пример: /calorie жареная курица 200
    Вывод: Жареная курица 200г - 400 ккал, Б: 30г, Ж: 20г, У: 10г(пример)

    Сделать так чтобы бот считал всю калорийность за весь день и после выводил если пользователь 
    запросит /calorie_total, бот выводил общую калорийность за день и БЖУ.

    Создать базу даныых с калорийностью и БЖУ для популярных блюд, чтобы бот мог быстро выдавать информацию.
    Пользователь может добавлять свои блюда и их калорийность, чтобы бот мог использовать эту информацию в будущем.

    Dead line: 20.05.2024
    """
def send_message(message, result):
    bot.send_message(message.chat.id, 
                     f"Каллорийность продуктов - {result[3]} ккал"
                     f"(белков - {result[1]}, жиров - {result[2]}, "
                     f"углеводов - {result[0]})")

def calc_nutrient(message, food_items):
    result = [0, 0, 0, 0]
    processed_items = []
    
    for item in food_items:
        if isinstance(item, str):
            processed_items.append((item.lower(), 100))
        elif isinstance(item, (tuple, list)) and len(item) == 2:
            product_name, gram = item
            processed_items.append((product_name.lower(), gram))
        else:
            bot.send_message(message.chat.id, f"Неверный формат продукта: {item}")

    for item, gram in processed_items:
        if item not in calories_counter:
            if item not in my_set_products:
                bot.send_message(message.chat.id, f"Продукт '{item}' не найден в базе")
                my_set_products.add(item)
            continue
        
        product_name = calories_counter[item]
        for i in range(4):
            result[i] += (product_name[i] / 100) * gram
            
    send_message(message, [round(x, 2) for x in result])

if __name__ == '__main__':
    print('Бот запущен!')
    bot.polling(none_stop=True)