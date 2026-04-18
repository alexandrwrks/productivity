from app.bot.handlers.start import router as start_router
from app.bot.handlers.news import router as news_router
from app.bot.handlers.news_source import router as news_source_router
from app.bot.handlers.subs import router as subs_router

routers = (
    start_router,
    news_router,
    news_source_router,
    subs_router
)