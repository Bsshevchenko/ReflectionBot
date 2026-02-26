# Reflection Telegram Bot

Telegram бот для личной рефлексии. Записывайте мысли и переживания в течение недели, а каждое воскресенье получайте структурированный AI-анализ.

## Описание

Бот позволяет пользователям вести дневник мыслей прямо в Telegram. Каждое воскресенье в 12:00 МСК бот автоматически анализирует записи через Groq API (модель `llama-3.3-70b-versatile`) и отправляет подробный отчёт с анализом эмоций, триггеров и практическими советами.

## Возможности

- **Запись мыслей** — просто отправьте текстовое сообщение боту в любой момент
- **Автоматический отчёт** — каждое воскресенье в 12:00 МСК
- **Ручной отчёт** — команда `/report` для немедленного анализа
- **Мультипользовательский** — работает с несколькими пользователями одновременно

## Структура недельного отчёта

1. Основные темы недели
2. Анализ эмоций
3. Причины и триггеры
4. Практические советы на следующую неделю

## Команды бота

| Команда | Описание |
|---------|----------|
| `/start` | Регистрация и приветствие |
| `/help` | Справка по командам |
| `/report` | Получить отчёт за текущую неделю |

## Установка и запуск

### Локально

1. Клонируйте репозиторий:
```bash
git clone <repo-url>
cd reflection-bot
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

3. Создайте `.env` файл:
```bash
cp .env.example .env
```

4. Заполните переменные в `.env`:
```
TG_TOKEN=ваш_токен_бота
ANTHROPIC_API_KEY=ваш_ключ_anthropic
```

5. Запустите бота:
```bash
python main.py
```

### Через Docker

1. Создайте `.env` файл с вашими токенами (см. выше)

2. Запустите через docker-compose:
```bash
docker-compose up -d
```

SQLite база данных хранится в volume `./data/bot.db`.

## Переменные окружения

| Переменная | Описание |
|-----------|----------|
| `TG_TOKEN` | Токен Telegram бота (от @BotFather) |
| `GROQ_API_KEY` | API ключ Groq (llama-3.3-70b-versatile) |

## Структура проекта

```
reflection-bot/
├── .env                     # Конфигурация (не коммитить!)
├── .env.example             # Пример конфигурации
├── requirements.txt
├── README.md
├── main.py                  # Entry point
├── bot/
│   ├── handlers/
│   │   ├── commands.py      # /start, /help, /report
│   │   └── entries.py       # Сохранение текстовых сообщений
│   └── scheduler.py         # APScheduler — воскресный отчёт
├── database/
│   ├── connection.py        # Инициализация БД
│   └── queries.py           # CRUD операции
├── ai/
│   └── analyzer.py          # Claude API — генерация отчёта
├── data/                    # SQLite файл (создаётся автоматически)
├── Dockerfile
├── docker-compose.yml
└── .github/
    └── workflows/
        └── deploy.yml       # CI/CD
```

## CI/CD через GitHub Actions

Настройте следующие секреты в репозитории GitHub:

| Secret | Описание |
|--------|----------|
| `SERVER_HOST` | IP-адрес или домен сервера |
| `SERVER_USER` | Пользователь SSH |
| `SSH_PRIVATE_KEY` | Приватный SSH ключ |

При каждом push в ветку `main` происходит автоматический деплой на сервер.

## Проверка работы

```bash
# Проверить записи в БД
sqlite3 data/bot.db "SELECT * FROM entries;"

# Проверить пользователей
sqlite3 data/bot.db "SELECT * FROM users;"
```
