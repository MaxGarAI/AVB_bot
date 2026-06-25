# Dealer.getbiz.me — AI Partner Discovery Agent

AI-агент для автоматического онбординга партнеров платформы getbiz.me.  
Проводит структурированное интервью с владельцем бизнеса, извлекает профиль аудитории, считает Partner Score и генерирует рекомендации.

## 🚀 Быстрый старт

```bash
# 1. Клонировать
git clone https://github.com/MaxGarAI/AVB_bot.git
cd AVB_bot

# 2. Создать виртуальное окружение (если нет)
python -m venv .venv

# 3. Активировать (Windows)
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 4. Добавить API-ключ OpenRouter
# Открой .env и запиши:
# OPENROUTER_API_KEY=sk-or-v1-...
# Ключ получить: https://openrouter.ai/keys

# 5. Убедиться, что тесты проходят
.venv\Scripts\python.exe -m pytest tests -q

# 6. Запустить сервер
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

После запуска открыть в браузере:

| URL | Что это |
|---|---|
| `http://localhost:8000/chat/{token}` | Чат с AI-агентом |
| `http://localhost:8000/admin/sessions` | Админка — все сессии |
| `http://localhost:8000/health` | Health-check |

## 🧠 Как это работает

```
Создать сессию → Получить ссылку → 
Партнер отвечает на вопросы → 
AI извлекает структуру → 
Считается Partner Score → 
Генерируется Executive Summary
```

Бот проводит интервью по **9 стадиям**:

1. **Business Discovery** — название, ниша, локация, сотрудники
2. **Audience Discovery** — количество клиентов, повторные продажи
3. **Segment Discovery** — сегменты аудитории
4. **Needs Discovery** — боли, потребности, что спрашивают
5. **Channel Discovery** — email, SMS, соцсети
6. **Partnership Discovery** — готовность рекомендовать
7. **Compliance Discovery** — ограничения
8. **Summary** — генерация отчёта
9. **Commit** — сохранение в БД

## 🏗 Технологии

| Компонент | Технология |
|---|---|
| Backend | Python 3.11 + FastAPI |
| База данных | SQLite (через SQLAlchemy 2.x) |
| LLM | OpenRouter + meta-llama/llama-3.1b-instruct (бесплатно) |
| UI | Jinja2 шаблоны (HTML + vanilla JS) |
| Тестирование | pytest |

## 📁 Структура проекта

```
AVB_bot/
├── app/                    # Backend-приложение
│   ├── main.py            # Точка входа FastAPI
│   ├── config.py          # Конфигурация (env, OpenRouter, SQLite)
│   ├── db.py              # SQLAlchemy engine
│   ├── api/               # REST-эндпоинты
│   ├── models/            # ORM-модели (10 таблиц)
│   ├── schemas/           # Pydantic-схемы
│   ├── services/          # Бизнес-логика
│   └── templates/         # HTML-шаблоны
├── tests/                 # 26+ тестов
├── databaseAVB.db         # SQLite БД (создаётся автоматически)
└── requirements.txt
```

## 🔐 Безопасность

- API-ключи хранятся только в `.env` (файл добавлен в `.gitignore`)
- Токены сессий генерируются через `secrets.token_urlsafe`
- SQLite-файл не попадает в репозиторий

## 📋 API Endpoints

| Method | Path | Описание |
|---|---|---|
| `GET` | `/health` | Health-check |
| `POST` | `/api/sessions` | Создать сессию интервью |
| `GET` | `/api/sessions/{token}` | Детали сессии |
| `POST` | `/api/chat/{token}/messages` | Отправить сообщение |
| `GET` | `/chat/{token}` | Чат (HTML) |
| `GET` | `/admin/sessions` | Админка — список |
| `GET` | `/admin/sessions/{token}` | Админка — детали |

## ✅ Тесты

```bash
.venv\Scripts\python.exe -m pytest tests -q
# 26 passed
```

## 📄 Лицензия

MIT