# Atomic Habits 🎯

Проект для управления привычками с отправкой уведомлений в Telegram.

## Технологии
- Python 3.12 + Django 6.0
- PostgreSQL 16
- Redis 7
- Celery (worker + beat)
- Docker Compose
- DRF + JWT
- Swagger/OpenAPI (drf-spectacular)

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone git@github.com:UBaH-lab/atomic_habits.git
cd atomic_habits
```

### 2. Создать .env файл
Создай файл `.env` в корне проекта:

```env
SECRET_KEY=твой_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_ENGINE=django.db.backends.postgresql
DB_NAME=atomic_habits
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

TELEGRAM_BOT_TOKEN=твой_токен_от_botfather
```

### 3. Запустить проект
```bash
docker-compose up --build
```

### 4. Выполнить миграции (в новом терминале)
```bash
docker-compose exec web python manage.py migrate
```

### 5. Создать суперпользователя
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Открыть в браузере
- Админка: http://127.0.0.1:8000/admin/
- Swagger UI: http://127.0.0.1:8000/api/docs/
- API: http://127.0.0.1:8000/api/

## Структура проекта
```
atomic_habits/
├── config/          # Настройки Django, Celery
├── habits/          # Приложение привычек
├── users/           # Приложение пользователей
├── Dockerfile
├── docker-compose.yml
├── .env
└── requirements.txt
```

## Telegram уведомления
Celery Beat отправляет задачу каждую минуту.
Celery Worker проверяет привычки и отправляет уведомления в Telegram.

⚠️ В России api.telegram.org заблокирован. Нужен VPN или рабочий прокси.