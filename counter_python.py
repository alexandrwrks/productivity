from products import calories_counter
import telebot
from telebot import types 
from bot_token import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
my_set = set()

# Парсинг сообщения на команду calories
@bot.message_handler(commands=['calories'])
def parcing_text(message):
    result = []
    parts = message.text.split()

    if len(parts) == 1 and parts[0] == '/calories':
        bot.send_message(message.chat.id,
                         f"Для успешного подсчёта КБЖУ напишите как в примере\n"
                         f"/calories макароны 140")
        return

    i = 1
    while i < len(parts):
        product = parts[i]
        grams = 100

        if i + 1 < len(parts) and parts[i + 1].isdigit():
            grams = int(parts[i + 1])
            i += 2
        else:
            bot.send_message(message.chat.id, 
                            f"У '{product}' не был указан вес из-за чего изменили вес на 100 грамм")
            i += 1
        result.append((product, grams))
 
    calc_nutrient(message, result)


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
            if item not in my_set:
                bot.send_message(message.chat.id, f"Продукт '{item}' не найден в базе")
                my_set.add(item)
            continue
        
        product_name = calories_counter[item]
        for i in range(4):
            result[i] += (product_name[i] / 100) * gram
            
    send_message(message, [round(x, 2) for x in result])

# print(f"Каллорийность продуктов - {result1[3]} ккал"
#       f"(белков - {result1[1]}, жиров - {result1[2]}, "
#       f"углеводов - {result1[0]})")

# print(f"Каллорийность продуктов - {result2[3]} ккал"
#       f"(белков - {result2[1]}, жиров - {result2[2]}, "
#       f"углеводов - {result2[0]})")

# def calc_nutrient(food_items):
#     result = [0, 0, 0, 0]
#     processed_items =[]
    
#     for item in food_items:
#         if isinstance(item, str):
#             processed_items.append((item.lower(), 100))
#         elif isinstance(item, (tuple, list)) and len(item) == 2:
#             product_name, gram = item
#             processed_items.append((product_name.lower(), gram))
#         else:
#             print(f"Неверный формат продукта: {item}")

#     for item, gram in processed_items:
#         if item not in calories_counter:
#             if item not in my_set:
#                 print(f"Продукт '{item}' не найден в базе")
#                 my_set.add(item)
#             continue
        
#         product_name = calories_counter[item]
#         for i in range(4):
#             result[i] += (product_name[i] / 100) * gram
            
#     calories([round(x, 2) for x in result])

if __name__ == '__main__':
    print('Бот запущен!')
    bot.polling(none_stop=True)