from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import InputFile
from app.models.base import OrdersDataManager as ODM

import aiosqlite
import os

router = Router()

class RegisterUserStates(StatesGroup):
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
    
    await state.update_data(email=message.text.split())
    await state.set_state(RegisterUserStates.waiting_for_phone)
    await message.answer('Теперь введите название почты: ')