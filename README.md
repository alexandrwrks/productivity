# World News Bot

Telegram-бот для получения новостей из нескольких источников с подписками на источники.

## Функции

- Парсинг новостей из 3 источников
- Хранение новостей в PostgreSQL
- Подписки пользователя на источники (`/subs`)
- Авто-отправка новых новостей ждя подписчиков
- Просмотр последних новостей (`/news`)
- Список источников (`/sources`)

## Стек

- Python 3.11+
- Aiogram 2
- SQLAlchemy 2 (async)
- Alembic
- PostgreSQL
- httpx + BeautifulSoup4

# Быстрый старт 

### 1. Клонирование репозитория

```bash
git clone https://github.com/alexandrwrks/productivity.git
python -m venv venv
python -m pip install -r requirements.txt
```

### 2. Настройка .env

Создать в корне проекта (`.env`) и записать 

```bash
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/database_name
SYNC_DATABASE_URL=postgresql://postgres:password@localhost:5432/database_name
```

### 3. Миграции 

```bash
python -m alembic upgrade head
```

### 4. Запуск

```bash
python -m app.main
```

## Docker run

1. Copy `.env.example` to `.env` and set `BOT_TOKEN`.
2. Start services:

```bash
docker compose up --build -d
```

3. Check logs:

```bash
docker compose logs -f bot
```

4. Stop services:

```bash
docker compose down
```

Notes:
- Migrations are applied automatically on bot container start.
- PostgreSQL data is stored in Docker volume `postgres_data`.
