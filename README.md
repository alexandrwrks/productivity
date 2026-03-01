productivity-tracker/
│
├── main.py                 # Точка входа FastAPI
├── config.py               # Настройки приложения
├── database.py             # Работа с БД (SQLite)
├── models.py               # Pydantic модели
├── auth.py                 # Регистрация/логин (добавим позже)
├── utils.py                # Вспомогательные функции
│
├── static/                 # Статические файлы
│   ├── css/
│   │   ├── style.css       # Основные стили
│   │   └── themes.css      # Разные темы оформления
│   ├── js/
│   │   ├── main.js         # Общий JS
│   │   ├── todo.js         # Логика TODO
│   │   └── charts.js       # Графики
│   └── images/
│
├── templates/              # HTML шаблоны Jinja2
│   ├── base.html           # Базовый шаблон (навигация, подвал)
│   ├── index.html          # Главная (дашборд)
│   ├── week.html           # Недельный обзор
│   ├── day.html            # Детали одного дня
│   ├── todo.html           # Управление задачами
│   ├── stats.html          # Статистика и графики
│   ├── habits.html         # Привычки (если добавим)
│   ├── login.html          # Вход
│   ├── register.html       # Регистрация
│   └── 404.html            # Страница ошибки
│
├── requirements.txt        # Зависимости
└── .env                    # Переменные окружения (секреты)


Написать нормально README.md