from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData

from app.news.config_news import SOURCES

class SubscriptionsCallback(CallbackData, prefix="subsrc"):
    action: str
    source: str | None = None


class SubscriptionsState(StatesGroup):
    choosing_sources = State()

class SubscriptionsSources:
    vtomske: bool = False
    kommersant: bool = False
    euronews: bool = False

    # bool = True значит пользователь выбрал это источник
    # bool =False значит пользователь убрал галочку с источника
