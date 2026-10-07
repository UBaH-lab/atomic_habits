# Atomic Habits API

REST API для сервиса учёта привычек (Django REST Framework).
Планировщик рассылки напоминаний в Telegram через Celery Beat.

## Стек

- Python 3.12, Django 5, DRF, SimpleJWT
- PostgreSQL 16, Redis 7, Celery (worker + beat)
- Nginx + Gunicorn (продакшен)
- Docker, Docker Compose
- CI/CD: GitHub Actions

## Переменные окружения

Скопируйте шаблон и заполните значения:

    cp .env.template .env

| Переменная | Назначение |
|---|---|
| SECRET_KEY | секретный ключ Django |
| DEBUG | True/False — режим отладки (в проде False) |
| ALLOWED_HOSTS | разрешённые хосты через запятую |
| DB_ENGINE | django.db.backends.postgresql (пусто — SQLite) |
| DB_NAME / DB_USER / DB_PASSWORD | данные БД |
| DB_HOST / DB_PORT | хост и порт БД (в Docker: db / 5432) |
| POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD | контейнер PostgreSQL |
| CELERY_BROKER_URL / CELERY_RESULT_BACKEND | Redis (в Docker: redis://redis:6379/0) |
| TELEGRAM_BOT_TOKEN | токен Telegram-бота |

## Запуск локально (Docker)

    docker compose up -d --build
    docker compose exec web python manage.py migrate
    docker compose exec web python manage.py createsuperuser

Приложение доступно через Nginx: http://localhost/
Админка: http://localhost/admin/

## Запуск без Docker

    python -m venv venv
    source venv/bin/activate        # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py.py runserver

## CI/CD (GitHub Actions)

При каждом push/PR выполняется конвейер:

1. **tests** — прогон тестов проекта
2. **lint** — проверка flake8
3. **build** — сборка Docker-образа
4. **deploy** — только при push в `main`: деплой на удалённый сервер
   по SSH (git pull → docker compose up -d --build → migrate → collectstatic)

## Деплой на сервер

- Виртуальная машина Yandex Cloud (Ubuntu 24.04, IP выдается при создании)
- Доступ по SSH-ключу, firewall: порты 22, 80, 443 (ufw + группа безопасности)
- Docker + Docker Compose на сервере
- Секреты репозитория: SSH_HOST, SSH_USER, SSH_PRIVATE_KEY
- `.env` создаётся на сервере (в git не хранится)
- Контейнеры с `restart: always` — авто-перезапуск

После merge в `main` приложение обновляется автоматически
и доступно по адресу сервера.
