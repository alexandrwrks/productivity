from aiogram import Bot
from aiogram.types import Message

import asyncio


class ReminderManager:
    """
    Команда для напоминания. 
    Пользователь вводит время в минутах и текст напоминания, 
    бот устанавливает таймер и отправляет напоминание через указанное время.
    Парсинг сообщения /remind [время в минутах] [напоминание]
    """
    def __init__(self, bot: Bot):
        self.bot = bot
        self.timers = []

    async def remind(self, message: Message):
        """
        Обработка команды /remind
        """
        try:
            """
            Сдедать обработку сообщения с добавлением клавиатуры для удаления напоминания если оно/и есть
            """
            args = message.text.split()
            if len(args) == 1:
                await message.answer(
                    f"Введите напоминание в формате:\n/remind [минуты] [текст]\n\n " \
                    "Пример: /remind 5 Позвонить маме")
                return
                  
            minutes = int(args[1])
            reminder_text = ' '.join(args[2:])

            await message.answer(
                f"⌛ Напоминание установлено на {minutes} минут: {reminder_text}")
            
            task = asyncio.create_task(
                self.set_timer(message.chat.id, minutes, reminder_text)
            )
            self.timers.append(task)

        except (ValueError, IndexError):
            await message.answer(
                "⚡ Пожалуйста, введите время в минутах и текст напоминания."
            )
    
    async def set_timer(self, chat_id : int, minutes : int, text : str):
        """
        Установка асинхронного таймера
        """
        await asyncio.sleep(minutes * 60)
        await self.send_reminder(chat_id, text)
   
    async def send_reminder(self, chat_id : int, text : str):
        """
        Отправка напоминания
        """
        try:
            await self.bot.send_message(chat_id, f"Напоминание: {text}")
        except Exception as e:
            print(f"Ошибка при отправке напоминания: {e}")
    
    async def cancel_all_reminders(self, message: Message):
        """
        Отмена всех напоминаний
        """
        if self.timers:
            count = len(self.timers)
            for task in self.timers:
                task.cancel()
            self.timers.clear()
            await message.answer(f"✅ Удалено {count} напоминаний")
        else:
            await message.answer(f"❌ Активные напоминания отсутствуют")