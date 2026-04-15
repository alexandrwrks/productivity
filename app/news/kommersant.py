import httpx
import asyncio

from typing import Optional

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from app.news.config import NewsInfo

async def process_vtomsker() -> Optional[NewsInfo]:
    async with httpx.AsyncClient() as client:
        return