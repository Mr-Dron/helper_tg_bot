# Helper TG Bot

Telegram-бот — менеджер задач: компании (списки), сотрудники, задачи со статусами. Проект на чистом энтузиазме, в активной разработке.

| | |
|---|---|
| **Версия** | `pre-alpha 1.0.1` |
| **Статус** | ранняя разработка, не для продакшена |
| **Стек** | Python 3 · aiogram 3 · SQLAlchemy 2 (async) · PostgreSQL · Alembic |

---

## Для себя: быстрый срез

Используй этот блок как «панель состояния» после каждого дня кодинга: обновляй версию, галочки и [журнал](#журнал-разработки).

### Версии

| Версия | Дата | Кратко |
|--------|------|--------|
| pre-alpha 1.0.1 | 2026-05-23 | Профиль: обновление имени, рефакторинг `user` → `profile`, дубли хендлеров ещё не убраны |
| pre-alpha 1.0.0 | 2026-05-19 | Старт, `/start`, эхо-режим, middleware пользователя, схема БД под компании и задачи |

### Уже сделано

- [x] Точка входа, polling (`app/main.py`)
- [x] Middleware: сессия БД + автосоздание пользователя по `telegram_id`
- [x] Команда `/start`, приветствие, главное меню
- [x] Просмотр «Моя информация» (профиль)
- [x] Обновление имени (ручной ввод + «взять из Telegram»)
- [x] Эхо-режим (FSM) для проверки состояний
- [x] Модели и миграции: `users`, `companies`, `employees_company`, `tasks`
- [x] Docker Compose для PostgreSQL
- [x] Alembic, настройки через `.env` (pydantic-settings)
- [x] Доделать обновление `username` и `telegram_url`

### В работе / дальше по плану

- [ ] Убрать дублирование хендлера `me` (`main.py` vs `profile.py`)
- [ ] Хендлер «Мои компании» (`callback_data=my_companies`)
- [ ] CRUD компаний и задач в боте
- [ ] Добавить `aiogram` в `requirements.txt`, описать версию
- [ ] README / `.env.example` синхронизировать с реальным запуском
- [ ] (опционально) FastAPI-слой — зависимости уже есть, приложения пока нет

---

## О проекте

Бот помогает не терять задачи: напоминания, списки по «компаниям» (это может быть семья, команда или личный список). Сейчас реализован каркас и профиль пользователя; доменная логика компаний и задач заложена в БД, UI для них — впереди.

**Архитектура (кратко):**

```
Telegram → Dispatcher → DBUserMiddleware → handlers → services → SQLAlchemy → PostgreSQL
```

| Папка | Назначение |
|-------|------------|
| `app/handlers/` | Роутеры aiogram (команды, callback, FSM) |
| `app/services/` | Бизнес-логика |
| `app/repositories/` | Запросы к БД (пока минимально) |
| `app/models/` | ORM-модели |
| `app/keyboards/` | Inline / reply-клавиатуры |
| `app/states/` | FSM-состояния |
| `app/middleware/` | Сессия и пользователь на каждый апдейт |
| `app/core/` | Настройки, engine, `TaskStatus` |
| `migrations/` | Alembic |

---

## Технологии

| Компонент | Технология |
|-----------|------------|
| Бот | [aiogram](https://docs.aiogram.dev/) 3.x |
| БД | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 (async), `asyncpg` |
| Миграции | Alembic |
| Конфиг | `pydantic-settings`, `.env` |
| Контейнер БД | Docker Compose |
| Задел под API | FastAPI в зависимостях (пока не используется в рантайме) |

Зависимости Python: см. [`requirements.txt`](requirements.txt).  
**Важно:** `aiogram` сейчас нужно ставить отдельно — в `requirements.txt` его ещё нет. Пример:

```bash
pip install aiogram
```

---

## Локальный запуск

### Требования

- Python 3.11+ (рекомендуется)
- Docker и Docker Compose (для Postgres)
- Токен бота от [@BotFather](https://t.me/BotFather)

### 1. Клонирование и окружение

```bash
git clone <url-репозитория> helper_tg_bot
cd helper_tg_bot

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install aiogram
```

### 2. Переменные окружения

Создай файл `.env` в корне проекта:

```env
# PostgreSQL (для docker-compose)
POSTGRES_USER=helper
POSTGRES_PASSWORD=helper_secret
POSTGRES_DB=helper_db
POSTGRES_PORT=5432

# SQLAlchemy async URL
DATABASE_URL=postgresql+asyncpg://helper:helper_secret@localhost:5432/helper_db

# Telegram
BOT_TOKEN=123456:ABC-DEF...
```

`DATABASE_URL` должен использовать драйвер **asyncpg** (`postgresql+asyncpg://...`).

### 3. База данных

```bash
docker compose up -d
alembic upgrade head
```

Проверка, что контейнер поднят:

```bash
docker compose ps
```

### 4. Запуск бота

Из корня репозитория (чтобы импорты `app.*` работали):

```bash
python -m app.main
```

Остановка: `Ctrl+C`.

---

## Как протестировать у себя

1. Запусти Postgres и миграции (см. выше).
2. Запусти бота.
3. В Telegram открой своего бота → `/start`.
4. Проверь по чек-листу:

| Действие | Ожидание |
|----------|----------|
| `/start` | Приветствие + inline-меню |
| «Моя информация» | ID, имя, username, ссылка |
| «Обновить данные» → «Изменить имя» | FSM, ввод или «взять из профиля» |
| «Мои компании» | Пока без хендлера — кнопка может не отвечать |

После первого сообщения пользователь создаётся в таблице `users` (middleware).

Логи SQL при `echo=True` в `app/core/database.py` — для отладки; в проде позже выключить.

---

## Миграции

```bash
# применить все
alembic upgrade head

# откатить один шаг
alembic downgrade -1

# новая ревизия (после изменения models)
alembic revision --autogenerate -m "описание"
```

Текущая цепочка: `3a75b88465da` (users) → `b29a4bc938bc` (companies, tasks, …).

---

## Журнал разработки

Новые записи — **сверху**. Шаблон на день:

```markdown
### YYYY-MM-DD

**Версия:** pre-alpha x.x.x (если менялась)

**Сделано:**
- ...

**Проблемы / долги:**
- ...

**Завтра / идеи:**
- ...
```

---

### 2026-05-23

**Версия:** pre-alpha 1.0.1

**Сделано:**
- README: структура проекта, запуск, чек-лист, журнал
- Модуль профиля: `handlers/profile.py`, `services/profile.py`, клавиатуры и FSM для имени
- Рефакторинг: `services/user.py` → профильный сервис

**Проблемы / долги:**
- Два хендлера на `callback_data=me` (`main` и `profile`)
- `aiogram` не в `requirements.txt`
- Кнопка «Мои компании» без обработчика

**Завтра / идеи:**
- Убрать дубли, дописать username/url
- Начать хендлеры компаний

---

## Известные ограничения

- Версия **pre-alpha**: возможны поломки схемы и UX без предупреждения.
- `responsible_id` в миграции: `SET NULL`, но колонка в модели без `nullable=True` — при отладке удалений учитывать.
- FastAPI-зависимости (`app/dependencies/`) не подключены к боту.
- README и приветствие в боте могут расходиться по номеру версии — сверяй таблицу версий выше.

---

## Полезные команды (шпаргалка)

```bash
# venv
source venv/bin/activate

# БД
docker compose up -d
docker compose down

# Бот
python3 -m app.main

# Миграции
alembic revision autogenerate -m "..."
alembic upgrade head
```

---

## Участие и наблюдение

Проект открыт для просмотра и идей. Для локального теста достаточно своего `BOT_TOKEN` и Postgres. История изменений — в git и в [журнале разработки](#журнал-разработки) выше.

---

*Последнее обновление README: 2026-05-23 · версия документации: pre-alpha 1.0.1*
