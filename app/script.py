"""
Скрипт для парсинга всех источников

"""

import asyncio

from app.news.euronews import euro_news
from app.news.kommersant import kommersant_news
from app.news.vtomske import vtomske_news

from app.news.config_news import NAME_OF_SOURCE

from app.database.config_db import logger

class NewsChecker:
    async def check_euronews_and_kommersant(self):
        while True:
            try:
                logger.info(f"Начало парсинга: {NAME_OF_SOURCE[1]} и {NAME_OF_SOURCE[2]}")
                await asyncio.gather(
                    euro_news.parsing_euronews(),
                    kommersant_news.parsing_kommersant()
                )
                logger.info(f"Конец парсинга: {NAME_OF_SOURCE[1]} и {NAME_OF_SOURCE[2]}")
            except Exception as e:
                logger.exception(f"Ошибка при парсинге: {e}")
            
            await asyncio.sleep(300)
            
    async def check_vtomske(self):
        while True:
            try:
                logger.info(f"Начало парсинга: {NAME_OF_SOURCE[0]}")
                await vtomske_news.parsing_vtomske()
                logger.info(f"Конец парсинга: {NAME_OF_SOURCE[0]}")
            except Exception as e:
                logger.exception(f"Ошибка при парсинге: {e}")

            await asyncio.sleep(1800)

news_checker = NewsChecker()



async def run_all():
    await asyncio.gather(
        news_checker.check_euronews_and_kommersant(),
        news_checker.check_vtomske()
    )
