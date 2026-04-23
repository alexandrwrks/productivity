"""
Скрипт для парсинга всех источников и сохранения новостей в БД

"""

import asyncio

from aiogram import Bot

from app.news.euronews import euro_news
from app.news.kommersant import kommersant_news
from app.news.vtomske import vtomske_news

from app.news.config_news import NAME_OF_SOURCE, SOURCES

from app.database.config_db import logger

from app.repo.news import news_repo
from app.repo.subscription import subs_repo

class NewsChecker:
    async def _notify_subscribers(self, bot: Bot, news_info):
        user_ids = await subs_repo.get_active_user_ids_by_source(news_info.source)
        if not user_ids:
            return

        source_name = SOURCES.get(news_info.source, news_info.source)
        message_text = (
            f"Новая новость из {source_name}\n\n"
            # f"{news_info.title}\n"
            # f"{news_info.url}\n"
            f"<a href=\"{news_info.url}\"><b>{news_info.title}</b>"
        )

        for user_id in user_ids:
            try:
                await bot.send_message(
                    chat_id=user_id,
                    text=message_text,
                    parse_mode="HTML",
                    disable_web_page_preview=True)
            except Exception as e:
                logger.exception(f"Send news error to user {user_id}: {e}")

    async def check_vtomske(self, bot: Bot):
        while True:
            try:
                logger.info(f"The beginning of parsing: {NAME_OF_SOURCE[0]}")
                vtomske_news_info = await vtomske_news.parsing_vtomske()

                for news_info in vtomske_news_info:
                    is_new = await news_repo.exists_news_in_database(news_info)
                    if is_new:
                        await self._notify_subscribers(bot, news_info)
                    
                logger.info(f"End of parsing: {NAME_OF_SOURCE[0]}")
            except Exception as e:
                logger.exception(f"Error during parsing: {e}")

            await asyncio.sleep(600)

    async def check_kommersant(self, bot: Bot):
        while True:
            try:
                logger.info(f"The beginning of parsing: {NAME_OF_SOURCE[1]} и ")
                kommersant_news_info = await kommersant_news.parsing_kommersant()

                for news_info in kommersant_news_info:
                    is_new = await news_repo.exists_news_in_database(news_info)
                    if is_new:
                        await self._notify_subscribers(bot, news_info)

                logger.info(f"End of parsing: {NAME_OF_SOURCE[1]}")
            except Exception as e:
                logger.exception(f"Error during parsing: {e}")
            
            await asyncio.sleep(240)
        
    async def check_euronews(self, bot: Bot):
        while True:
            try:
                logger.info(f"The beginning of parsing: {NAME_OF_SOURCE[2]}")
                euronews = await euro_news.parsing_euronews()

                for news_info in euronews:
                    is_new = await news_repo.exists_news_in_database(news_info)
                    if is_new:
                        await self._notify_subscribers(bot, news_info)

                logger.info(f"End of parsing: {NAME_OF_SOURCE[2]}")
            except Exception as e:
                logger.exception(f"Error during parsing: {e}")

            await asyncio.sleep(240)


news_checker = NewsChecker()



async def run_all(bot: Bot):
    await asyncio.gather(
        news_checker.check_vtomske(bot)
        , news_checker.check_kommersant(bot)
        , news_checker.check_euronews(bot)
    )
