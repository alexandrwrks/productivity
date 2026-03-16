import aiogram
from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.models.base import UsersDataManager, ItemsDataManager, OrdersDataManager
from app.bot.keyboards import KeyBoardManager
from app.services import user_service
from aiogram.fsm.context import FSMContext

main_router = Router()

class HandleManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.UDM = UsersDataManager()
        self.IDM = ItemsDataManager()
        self.ODM = OrdersDataManager()
        self.keyboard = KeyBoardManager

        main_router.include_router(user_service.router)

        self._setup_handlers_()

    def _setup_handlers_(self):
        @main_router.message(Command('start'))
        async def get_start(message: Message):            
            text = (f"Привет, я бот-помощник.\nПомогаю людям с покупками в интернет магазинах")

            await message.answer(
                text, 
                reply_markup=self.keyboard.get_start_keyboard()
            )

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

        @main_router.message(Command('profile'))
        async def get_profile():
            """
            Функция для вывода профоля пользователя/админа.
            После /profile [username] будет выводить профиль того человека который будет указан в [].
            В профиле будет указан рейтинг пользователя. Его username. Количество заказво(если пользователь),
            количество товаров и соответсвенно товары(для админов)
            """
            pass
        

        @main_router.message(Command('order'))
        async def get_catalog(bot: Bot, user_id: int, product_data: dict,):
            await bot.send_photo(
                chat_id=user_id,
                photo=product_data['photo_file_id'],
                caption=f"{product_data['item_name']}\nЦена: {product_data['price']}\n{product_data['description']}\nПродавец: @{product_data['username']}"
            )

        @main_router.message(Command('catalog'))
        async def get_catalog(message: Message):
            """
            После /catalog. Пользователю приходят сообщения с предеметами которые сейчас находятся в продаже(имеют active = True/1)
            Парсинг сообщения выглядит как карточка товара: фото, номер товара, username продавца, ниже описание и цена(в рублях)

            """
            await self.IDM.init_db()
            catalog = await self.IDM.get_items_data()

            if not catalog:
                await message.answer("Нет активных объявлений")
                return

            # text = "Активные объявления:"
            for item_id, item_name, username, price in catalog:
                await message.answer(
                    f"№{item_id} от <i>@{username}</i>\n\n"
                    f"Название: <b>{item_name}</b>\n"
                    f"Стоимость: {price}", 
                    parse_mode='HTML')


        @main_router.message(Command('support'))
        async def get_support(message: Message):
            await message.answer("Введите сообщение в котором ")

        @main_router.message(Command('order'))
        async def do_order(message: Message):
            """
            Пользователь вводит по очереди название предмета, описание, стоимость, фото.
            Сделать проверку 
            """
            await message.answer("Введите название предмета: (обязательно)")
            await message.answer("Введите описание предмета: (обязательно)")
            await message.answer("Введиете стоимость: (обязательно)")
            await message.answer("Добавьте фото для товара: (обязательно)")

            
        @main_router.message(F.text == '💾 Закончить регистрацию')
        async def fihish_registration(message: Message, state: FSMContext):
            """Обработчик кнопки завершения регистрации"""
            current_state = await state.get_state()
            if current_state:
                await state.clear()
                await message.answer("Регистрация прервана!")
            else:
                await message.answer("Нет активной регистрации")



__all__ = ['main_router']