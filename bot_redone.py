from telebot import types
from bot_token import BOT_TOKEN

import telebot
import random
import threading

bot = telebot.TeleBot(BOT_TOKEN)

"""
Главное меню. Игра. Напоминалка. Помощь. 
Обработка сообщений для каждого пункта меню.
Обработка функций для каждой функции меню.
"""

@bot.message_handler(commands=['start'])
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    game = types.KeyboardButton('Игра')
    remind = types.KeyboardButton('Напоминалка')
    helper = types.KeyboardButton('Помощь')
    markup.add(game, remind)
    markup.add(helper)
    bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)
    
@bot.message_handler(commands=['remind'])
def remind(message):
    # Парсинг сообщения /remind [время в минутах] [напоминание]
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

@bot.message_handler(func=lambda message: True)
def handle_message(message):

    if message.text == 'Игра' or message.text == '/game':
        bot.send_message(message.chat.id, 'Вы выбрали игру!')
        start_game(message)
    elif message.text == 'Напоминалка':
        bot.send_message(message.chat.id, 'Вы выбрали напоминалку!')
        bot.send_message(message.chat.id, 
                        "Введите напоминание в формате:\n/remind [минуты] [текст]\n\n"
                        "Пример: /remind 5 Позвонить маме")

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
 

if __name__ == '__main__':
    print('Бот запущен!')
    bot.polling(none_stop=True)