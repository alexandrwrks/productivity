"""
Создать класс в котором я буду запрашивать у пользователя данные для регистрации его аккаунта
для дальнейшего использования как в боте так и для сайта.
Использовать БД для регистрации/авторизации пользователей.
Сделать правильные натсройки полученных данных чтобы не было проблема с получение str в int.
Адаптировать как для ТГ бота так и для сайта.

Настройка полученных данных. Проверка данных. Добваление в БД. Доработка, убрать баги.
"""
from aiogram import Bot
from aiogram.types import Message

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from works_with_all_tables import UsersDataManager

import uvicorn
import os

# UDM = UsersDataManager()

# input_users_data = "какие-то данные упорядоченные для точной работы"
# UDM.add_user_to_db(input_users_data)