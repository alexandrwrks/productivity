import aiogram
from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
from app.models.base import UsersDataManager, ItemsDataManager, OrdersDataManager

router = Router()

class HandleManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.UDM = UsersDataManager()
        self.IDM = ItemsDataManager()
        self.ODM = OrdersDataManager()
        self._setup_handlers_()

    def _setup_handlers_(self):
        @router.message(Command('start'))
        async def get_start(message: Message):            
            user = message.from_user
            user_id = user.id
            username = user.username

            text = (f"Привет, я бот-помощник. Помогаю людям с покупками в интрент магазинах\n\n"
                    f"Твой ID {user_id}"
                    f"Username: {username}")
            
            user_data = (user_id, username)

            await self.UDM.add_user_from_bot(user_data)
            await message.answer(text)

        # @router.message(Command('profile')) 
        # async def get_info(message: Message):
        #     chat_info = await self.bot.get_chat(message.from_user.id)
        #     bio = chat_info.bio

        #     photos = await self.bot.get_user_profile_photos(message.from_user.id)
        #     if photos.total_count > 0:
        #         photo_id = photos.photos[0][0].file_id
        #         await message.answer_photo(photo_id, caption=f"Ваше фото. Био: {bio}")
        #     else:
        #         await message.answer(f"Фото не найдено. Био: {bio}")

        @router.message(Command('profile'))
        async def get_profile(self):
            """
            Функция для вывода профоля пользователя/админа.
            После /profile [username] будет выводить профиль того человека который будет указан в [].
            В профиле будет указан рейтинг пользователя. Его username. Количество заказво(если пользователь),
            количество товаров и соответсвенно товары(для админов)
            """
            pass

        @router.message(Command('catalog'))
        async def get_catalog(message: Message):
            
            catalog = await self.IDM.show_items_data()
            if catalog:
                text = (f"Номер товара: №{catalog[0]} от {catalog[2]}\n\nНазвание: *{catalog[1]}*\n\n Цена: *{catalog[3]}*")
            else:
                text = (f"Активных товаров нет в наличие")
            await message.answer(text, parse_mode='Markdown')
