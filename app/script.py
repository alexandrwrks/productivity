"""
Скрипт для парсинга всех источников и сохранения новостей в БД

"""

import asyncio

from app.news.euronews import euro_news
from app.news.kommersant import kommersant_news
from app.news.vtomske import vtomske_news

from app.news.config_news import NAME_OF_SOURCE

from app.database.config_db import logger

from app.repo.news import news_repo

class NewsChecker:
    async def check_vtomske(self):
        while True:
            try:
                logger.info(f"Начало парсинга: {NAME_OF_SOURCE[0]}")
                vtomske_news_info = await vtomske_news.parsing_vtomske()

                for news_info in vtomske_news_info:
                    await news_repo.exists_news_in_database()
                    
                logger.info(f"Конец парсинга: {NAME_OF_SOURCE[0]}")
            except Exception as e:
                logger.exception(f"Ошибка при парсинге: {e}")

            await asyncio.sleep(1800)

    async def check_kommersant(self):
        while True:
            try:
                logger.info(f"Начало парсинга: {NAME_OF_SOURCE[1]} и ")
                kommersant_news_info = await kommersant_news.parsing_kommersant()

                for news_info in kommersant_news_info:
                    await news_repo.exists_news_in_database(news_info)

                logger.info(f"Конец парсинга: {NAME_OF_SOURCE[1]}")
            except Exception as e:
                logger.exception(f"Ошибка при парсинге: {e}")
            
            await asyncio.sleep(300)
        
    async def check_euronews(self):
        while True:
            try:
                logger.info(f"Начало парсинга: {NAME_OF_SOURCE[2]}")
                euronews = await euro_news.parsing_euronews()

                for news_info in euronews:
                    await news_repo.exists_news_in_database(news_info)

                logger.info(f"Конец парсинга: {NAME_OF_SOURCE[2]}")
            except Exception as e:
                logger.exception(f"Ошибка при парсинге: {e}")

            await asyncio.sleep(300)


news_checker = NewsChecker()



async def run_all():
    await asyncio.gather(
        news_checker.check_vtomske()
        , news_checker.check_kommersant()
        , news_checker.check_euronews()
    )
