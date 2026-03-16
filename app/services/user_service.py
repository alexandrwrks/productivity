from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import InputFile
from app.models.base import UsersDataManager as UDM

import aiosqlite
import os

router = Router()

class RegisterUserStates(StatesGroup):
    """
    Полная регистрация пользователя: почта, номер телефона, имя, город проживания 
    для полноценной работы с ботом и в дальнейшем с сайтом
    """
    waiting_for_name = State()
    waiting_for_email = State()
    waiting_for_phone = State()
    waiting_for_city = State()

@router.message(Command('reg'))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(RegisterUserStates.waiting_for_name)
    await message.answer('Введите Ваше имя: ')

@router.message(RegisterUserStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Введите имя: ')
        return
    
    await state.update_data(name=message.text.strip())
    await state.set_state(RegisterUserStates.waiting_for_email)
    await message.answer('Теперь введите вашу почту: ')

@router.message(RegisterUserStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Введите почту:')
        return
    
    await state.update_data(email=message.text.strip())
    await state.set_state(RegisterUserStates.waiting_for_phone)
    await message.answer('Теперь введите номер телефона: ')

@router.message(RegisterUserStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Введите номер телефона:')
        return
    
    await state.update_data(phone=message.text.strip())
    await state.set_state(RegisterUserStates.waiting_for_city)
    await message.answer('Введите ваш город:')

@router.message(RegisterUserStates.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    if not message.text:
        await message.answer('Введите город:')
        return
    
    await state.update_data(city=message.text.strip())
    
    # Получаем все данные
    data = await state.get_data()
    
    # Сохраняем в БД
    await ODM.add_user(data)  # Или другой менеджер
    
    await message.answer(f"✅ Регистрация завершена!\n"
                        f"Имя: {data['name']}\n"
                        f"Email: {data['email']}\n"
                        f"Телефон: {data['phone']}\n"
                        f"Город: {data['city']}")
    
    await state.clear()