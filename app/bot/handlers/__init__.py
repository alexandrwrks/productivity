from .start import router as start_router
from .news import router as news_router
from .news_source import router as news_source_router

routers = (
    start_router,
    news_router,
    news_source_router,
)