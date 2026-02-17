"""
Игра камень, ножницы, бумага в ТГ боте
Курсы валют. Погода. Новости
Добавить кнопки: Камень, Ножницы и Бумагу
После нашего выбора бот должен, напечатать случайно 1 выбор из 3
Если мы выигрываем то играем дальше, если прогирываем, должен быть вариант играть заново или перестать
"""
import random
import telebot
from telebot import types
import time
import threading

BOT_TOKEN = '8409019240:AAFAHkur6SkRz1R49ejBobpgsBjFe0duDBI'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def main_menu(mes):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    currency_rate = types.KeyboardButton('Напоминалка')
    game = types.KeyboardButton('Игра')
    back_to_main = types.KeyboardButton('В главное меню')
    helper = types.KeyboardButton('Помощь')
    keyboard.add(currency_rate, game)
    keyboard.add(back_to_main, helper)

    bot.send_message(mes.chat.id, 'Выберите действие:', reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def handle_help(mes):
    bot.send_message(mes.chat.id,
                     f"Для чего нужен этот бот\n\n"
                     f"/start - для стрта бота\n"
                     f"/remind - напоминалка\n"
                     f"/game - игра камень, ножницы, бумага\n\n"
                     f"Выберите что хотите сделать")
    
@bot.message_handler(commands=['game'])
def start_game(mes):
    show_game_buttons(mes)

def show_game_buttons(mes):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Камень')
    but2 = types.KeyboardButton('Ножницы')
    but3 = types.KeyboardButton('Бумага')
    markup.add(but1, but2, but3)

    bot.send_message(mes.chat.id, 'Сделайте свой выбор: ', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def game(mes):
    
    list_of_choice = ['Камень', 'Ножницы', 'Бумага']
    user_choice = mes.text

    if user_choice == "Игра" or user_choice == "/game":
        show_game_buttons(mes)
    elif user_choice == "Напоминалка" or user_choice == "/remind":
        example_remind(mes)
    elif user_choice == "В главное меню" or user_choice == "/start":
        main_menu(mes)
    elif user_choice == "Помощь" or user_choice == "/help":
        handle_help(mes)

    elif user_choice in list_of_choice:
        bot_choice = random.choice(list_of_choice)
        bot.send_message(mes.chat.id, f"Бот выбрал:  {bot_choice}")
        
        if user_choice == bot_choice:
            result = "Ничья! Попробуйте ещё раз."
            bot.send_message(mes.chat.id, result)
            time.sleep(0.2)
            show_game_buttons(mes)
        elif ((user_choice == "Ножницы" and bot_choice == "Бумага") or 
              (user_choice == "Камень" and bot_choice == "Ножницы") or 
              (user_choice == "Бумага" and bot_choice == "Камень")):
            result = "Вы выиграли! Играем дальше."
            bot.send_message(mes.chat.id, result)
            time.sleep(0.2)
            show_game_buttons(mes)
        else:
            result = "Вы проиграли!"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton('Играть заново'))
            markup.add(types.KeyboardButton('В главное меню'))
            bot.send_message(mes.chat.id, result, reply_markup=markup)

    elif user_choice == "Играть заново":
        show_game_buttons(mes)
    else:
    # elif user_choice != "Игра" or user_choice not in list_of_choice:
        bot.send_message(mes.chat.id, "Пожалуйста, используйте кнопки для выбора")    

def example_remind(mes):
    bot.reply_to(mes, "Введите напоминание в формате:\n/remind [минуты] [текст]\n\n " \
                      "Пример: /remind 5 Позвонить маме")
    
# Парсинг сообщения /remind [время в минутах] [напоминание]
def send_remind(chat_id, text):
    try:
        print(f"Отправка напоминания: {text}")  # отладка
        bot.send_message(chat_id, f"⏰ Напоминание: {text}")
        print("Напоминание отправлено")  # отладка
    except Exception as e:
        print(f"Ошибка при отправке напоминания {e}")

@bot.message_handler(commands=['remind'])
def set_reminder(mes):
    
    try:
        args = mes.text.split()

        if len(args) == 1:
            example_remind(mes)
            return

        minutes = int(args[1])
        seconds = minutes * 60 
        reminder_text = " ".join(args[2:])
        
        if minutes <= 0:
            bot.reply_to(mes, "Время должно быть положительным числом")
            main_menu(mes)
            return
        
        if not reminder_text:
            bot.reply_to(mes, "Вы не ввели текст напоминания")
            main_menu(mes)
            return

        bot.reply_to(mes, f"⌛ Напоминание установлено на {minutes} минут.")

        main_menu(mes)

        # Запуск таймера в отдельном потоке
        t = threading.Timer(seconds, send_remind, args=[mes.chat.id, reminder_text])
        t.start()

    except ValueError:
        bot.reply_to(mes, "⚡Ошибка минуты должны быть числом!\nФормат: /remind [минуты] [напоминание]")
    except IndexError:
        bot.reply_to(mes, "⚡Ошибка: неполная команда!\nФормат: /remind [минуты] [напоминание]")



if __name__ == '__main__':
    print("Бот запущен!")
    bot.polling(none_stop=True)
