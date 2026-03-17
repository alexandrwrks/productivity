import aiogram
from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from app.models.base import UsersDataManager, ItemsDataManager, OrdersDataManager
from app.bot.keyboards import KeyBoardManager
from app.services import user_service, product_service
from app.services.user_service import router as user_router
from app.services.product_service import router as product_router
from aiogram.fsm.context import FSMContext

main_router = Router()

class HandleManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.UDM = UsersDataManager()
        self.IDM = ItemsDataManager()
        self.ODM = OrdersDataManager()
        self.keyboard = KeyBoardManager

        main_router.include_router(user_router, product_router)

        self._setup_handlers_()

    def _setup_handlers_(self):
        @main_router.message(Command('start'))
        async def get_start(message: Message):            
            text = (f"Привет, я бот-помощник.\nПомогаю людям с покупками в интернет магазинах")

            await message.answer(
                text, 
                reply_markup=self.keyboard.get_reg_keyboard()
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
                    f"Стоимость: {price} руб.", 
                    parse_mode='HTML')

        @main_router.message(Command('helper'))
        @main_router.message(F.text == '❔ Помощь')
        async def get_support(message: Message):
            """Добавить FSM для работы поддержки, после введёного собщения, его нужно достваить в службу поддержки пользователя"""
            await message.answer(
                text='Выберите:',
                reply_markup=self.keyboard.help_menu()
            )

        @main_router.message(Command('help'))
        @main_router.message(F.text == '📖 Основные функции бота')
        async def get_help_menu(message: Message):

            text = f"На что способен бот:\n\n" \
                    f"/help - помощь в использлвание бота" \
                    f"/order - создание карточки вашего товара" \
                    f"/"

            await message.answer(text)

        @main_router.message(Command('support'))
        @main_router.message(F.text == '📄 Написать в поддержку')
        async def get_support(message: Message):
            await message.answer(
                text='Опишите вашу проблему и тех. поддержка в скором времени с Вами свяжется'
            )
            

__all__ = ['main_router']