from aiogram import Bot
from aiogram.types import Message

import datetime

class CaloriesManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.unsuitable_products = set() # Создание множества для продктов которых ещё нет в основном списке
        self.calories_counter = {
            'макароны': [30, 5, 1, 130],  # [углеводы, белки, жиры, калории]
            'гречка': [30, 4, 1, 120],
            'рис': [28, 2, 0.5, 110],
            'курица': [0, 25, 5, 150],
            # Добавьте остальные продукты по необходимости
        }
        self.file_name = 'calories_data.txt'

    def save_calories_data(self, user_id, date, result):
        """Сохранение калорий за день"""
        with open(self.file_name, 'a', encoding='UTF-8') as data_file:
            data_file.write(f"{user_id}|{date}|{result[3]}|{result[1]}|{result[2]}|{result[0]}\n")

    def get_calories_data(self, user_id, date):
        """
        Получение суммы калорий за день для конкретного пользователя
        """
        total = 0 
        try:
            # Открытие файла для прочтение иф=нформации
            with open(self.file_name, 'r', encoding='UTF-8') as data_file:
                for line in data_file:
                    saved_user, save_date, calories, protein, fats, carb = line.strip().split('|')
                    if saved_user == str(user_id) and save_date == str(date):
                        total += float(calories)
        except FileNotFoundError:
            pass
        return total
    
    async def send_daily_calories(self, message: Message):
        """
        Отправка отчёт-сообщения с калориями
        """
        today = datetime.date.today()
        total = self.get_calories_data(message.chat.id, today)

        await message.answer(
            message.chat.id,
            f"💾 Сумма калорий за сегодня: {total} ккал")

    async def send_message(self, message: Message, result):
        """
        Вывод подсчёта КБЖУ.
        """
        text = (f"Каллорийность продуктов - {result[3]} ккал"
                f"(белков - {result[1]}, жиров - {result[2]}, "
                f"углеводов - {result[0]})")
        
        await message.answer(text)

        today = datetime.date.today()
        self.save_calories_data(message.chat.id, today, result)
        
    async def calc_nutrient(self, message: Message, food_items):
        """
        Подсчёт КБЖУ и сохранение результатов в списов для дальнейшего вывода.
        """
        result = [0, 0, 0, 0]
        processed_items = []
        # Цикл для того чтобы донести информацию до бота в нужном ему виде
        for item in food_items: 
            if isinstance(item, str):
                processed_items.append((item.lower(), 100))
            elif isinstance(item, (tuple, list)) and len(item) == 2:
                product_name, gram = item
                processed_items.append((product_name.lower(), gram))
            else:
                await message.answer(f"Неверный формат продукта: {item}")
                return
            
        # Проверка нахождения продукта в БД/словаре
        for item, gram in processed_items:
            if item not in self.calories_counter:
                if item not in self.unsuitable_products:
                    await message.answer(f"Продукт '{item}' не найден в базе")
                    self.unsuitable_products.add(item)
                continue
            
            product_name = self.calories_counter[item]
            for i in range(4):
                result[i] += (product_name[i] / 100) * gram
                
        rounded_result = [round(x, 2) for x in result]
        await self.send_message(message, rounded_result)
    
    async def parcing_text(self, message: Message):
        """
        Отправка парсинг сообщения, как должно выглядеть сообщение.
        Основная программа для "правильного" получение данных от пользователя.
        """
        result = []
        parts = message.text.split()

        if len(parts) == 1 and parts[0] == '/calories':
            await message.answer(
                "📝 Введите счётчик в формате:\n\n"
                "`/calories продукт [граммы]`\n\n"
                "Примеры:\n"
                "• `/calories макароны 150`\n"
                "• `/calories курица 200 рис 100`\n"
                "• `/calories банан` (вес будет 100г)",
                parse_mode="Markdown"
            )
            return

        result = []
        default_weight = []
        i = 1
        # Обрабтка сообщения от пользователя
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
            await message.answer(f"Для продуктов {str_default} не был предоставлен вес из-за чего вес был изменён на 100")
        
        await self.calc_nutrient(message, result)

    async def delete_data(self, message: Message):
        """
        Функция для удаления данных пользователей
        """
        today = datetime.date.today()

        try:
            lines = []
            deleted = False

            with open(self.file_name, 'r', encoding='UTF-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    saved_user, save_data, *_ = line.strip().split('|')
                    if not (saved_user == str(message.chat.id) and save_data == str(today)):
                        lines.append(line)
                    else:
                        deleted = True

            if deleted:
                with open(self.file_name, 'w', encoding="UTF-8") as f:
                    f.write(lines)
                await message.answer("✅ Данные за сегодня удалены")
            else:
                await message.answer("❌ Нет данных с удалением за сегодня")
        except FileNotFoundError:
            await message.answer("Файл с данными не найден")
        except Exception as e:
            await message.answer(f"❌ Ошибка при удаление: {e}")