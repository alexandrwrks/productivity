from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import InputFile
from app.models.base import ItemsDataManager as IDM

import aiosqlite
import os

router = Router()

class ProductStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_price = State()
    waiting_for_photo = State()
    confirming_order = State()

@router.message(Command('order'))
async def cmd_order(message: Message, state: FSMContext):
    await state.set_state(ProductStates.waiting_for_name)
    await message.answer('Введите название товара: ')

@router.message(ProductStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 3:
        await message.answer("Введите название товара: ")
        return
    
    await state.update_data(name=message.text.strip())
    await state.set_state(ProductStates.waiting_for_description)
    await message.answer("Теперь введите описание: ")

@router.message(ProductStates.waiting_for_description)
async def procees_descriprion(message: Message, state: FSMContext):
    if not message.text or len(message.text.strip()) < 10:
        await message.answer("Слишком короткое описание товара: ")
        return

    await state.update_data(description=message.text.strip())
    await state.set_state(ProductStates.waiting_for_price)
    await message.answer('Введите цену товара: ')

@router.message(ProductStates.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = float(message.text.strip())
        if price <= 0:
            await message.answer("Цена должна быть положительна")
            return 
        
        await state.update_data(price=price)
        await state.set_state(ProductStates.waiting_for_photo)
        await message.answer("Отправьте фото товара: ")

    except ValueError:
        await message.answer("❌ Введите число")

@router.message(ProductStates.waiting_for_photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]  # Берем самое большое фото
    
    await state.update_data(photo_file_id=photo.file_id)

    data = await state.get_data()

    await message.answer_photo(
        photo=photo.file_id,
        caption=f"✅ Товар готов к публикации!\n\nНавзание: {data['name']}\nЦена: {data['price']}\nОписание: {data.get('description', 'Нет описания')}"
    )

    await state.get_state(ProductStates.confirming_order)
        
@router.message(ProductStates.waiting_for_photo)
async def process_photo_invalid(message: Message):
    await message.answer("Пожалуйста, отправьте фото")

@router.message(Command('confirm_order'), ProductStates.confirming_order)
async def confirm_order(message: Message, state: FSMContext):
    data = await state.get_data()

    # user_data = (name = data['name'], description = data['description'], price = data['price'], photo = data['photo_file_id'])
    user_data = tuple(data.values())
    # Сохранить данные в БД
    await IDM.add_item(user_data)

    await message.answer("✅ Заказ создан!")
    await state.clear()


@router.message(Command('cancel'))
async def cancell_order(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Нет автивного заказа")
        return
    
    await state.clear()
    await message.answer("❌ Заказ отменён")