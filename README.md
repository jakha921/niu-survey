# Survey App

Система управления опросами с интеграцией Google Forms и современным Django Unfold админ-интерфейсом.

## 🚀 Особенности

- **Современный админ-интерфейс** с Django Unfold
- **Интеграция с Google Forms** для создания и управления опросами
- **REST API** для работы с опросами
- **Веб-интерфейс** для просмотра и заполнения опросов
- **Многоязычность** (русский, английский, узбекский)
- **Отслеживание истории** изменений с django-simple-history
- **Кэширование** с Redis
- **Асинхронные задачи** с Celery

## 📋 Требования

- Python 3.10+
- uv (менеджер пакетов)
- Redis (опционально, для кэширования)
- PostgreSQL (для продакшена, SQLite для разработки)

## 🛠 Установка

### 1. Клонирование и настройка окружения

```bash
# Клонируйте репозиторий
git clone <your-repo-url>
cd survey

# Установите зависимости с помощью uv
uv sync

# Активируйте виртуальное окружение
source .venv/bin/activate  # Linux/macOS
# или
.venv\Scripts\activate  # Windows
```

### 2. Настройка переменных окружения

```bash
# Скопируйте файл с примерами переменных
cp env.example .env

# Отредактируйте .env файл
nano .env
```

Основные переменные в `.env`:
```env
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
REDIS_URL=redis://localhost:6379/0
```

### 3. Настройка базы данных

```bash
# Примените миграции
python manage.py migrate

# Создайте суперпользователя
python manage.py createsuperuser
```

### 4. Запуск сервера разработки

```bash
# Запустите Django сервер
python manage.py runserver

# Откройте в браузере
# http://127.0.0.1:8000/ - веб-интерфейс
# http://127.0.0.1:8000/admin/ - админ-панель
```

## 📱 Использование

### Создание опроса

1. Перейдите в админ-панель (`/admin/`)
2. Войдите под учетными данными суперпользователя
3. Перейдите в раздел "Опросы" → "Опросы"
4. Нажмите "Добавить опрос"
5. Заполните поля:
   - **Название опроса**: Краткое описательное название
   - **Ссылка на Google Form**: Полная ссылка на вашу Google Form
   - **Описание**: Дополнительная информация об опросе
   - **Активен**: Отметьте для публикации опроса

### Просмотр опросов

- Главная страница (`/`): Список всех активных опросов
- Детальная страница (`/survey/{id}/`): Просмотр опроса с встроенной Google Form
- Полноэкранный режим (`/survey/{id}/embed/`): Google Form на всю страницу

### API

Доступные эндпоинты:

```bash
# Получить список опросов
GET /api/surveys/?page=1&limit=20&search=название

# Получить конкретный опрос
GET /api/surveys/{id}/

# Статистика опросов
GET /api/surveys/stats/
```

Пример ответа API:
```json
{
    "count": 5,
    "total_pages": 1,
    "current_page": 1,
    "limit": 20,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Опрос удовлетворенности",
            "description": "Оцените качество наших услуг",
            "google_form_url": "https://forms.gle/...",
            "google_form_embed_url": "https://docs.google.com/forms/d/.../viewform?embedded=true",
            "created_at": "2024-01-15T10:30:00Z",
            "created_by": "admin"
        }
    ]
}
```

## 🗂 Структура проекта

```
survey/
├── config/                  # Настройки Django
│   ├── settings.py         # Основные настройки
│   ├── unfold_settings.py  # Настройки Unfold
│   ├── urls.py            # Главные URL
│   ├── wsgi.py            # WSGI конфигурация
│   └── asgi.py            # ASGI конфигурация
├── apps/                   # Django приложения
│   ├── surveys/           # Основное приложение опросов
│   │   ├── models.py      # Модель Survey
│   │   ├── admin.py       # Админ-панель
│   │   ├── views.py       # API и веб-views
│   │   └── urls.py        # URL маршруты
│   └── common/            # Общие компоненты
│       ├── dashboard.py   # Дашборд Unfold
│       └── environment.py # Настройки окружения
├── templates/             # HTML шаблоны
│   ├── base.html         # Базовый шаблон
│   └── surveys/          # Шаблоны опросов
├── static/               # Статические файлы
├── media/               # Загруженные файлы
├── pyproject.toml       # Конфигурация uv
├── manage.py           # Django CLI
└── README.md           # Документация
```

## 🔧 Настройка для продакшена

### 1. Переменные окружения

```env
SECRET_KEY=сложный-секретный-ключ
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/survey_db
REDIS_URL=redis://localhost:6379/0
```

### 2. Настройка PostgreSQL

```bash
# Установите PostgreSQL и создайте базу данных
sudo -u postgres createdb survey_db
sudo -u postgres createuser survey_user
sudo -u postgres psql
```

```sql
ALTER USER survey_user WITH PASSWORD 'ваш_пароль';
GRANT ALL PRIVILEGES ON DATABASE survey_db TO survey_user;
\q
```

### 3. Установка Redis

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# macOS
brew install redis

# Запуск Redis
redis-server
```

### 4. Сбор статических файлов

```bash
python manage.py collectstatic --noinput
```

### 5. Docker Compose (опционально)

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@db:5432/survey_db
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: survey_db
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## 🐛 Решение проблем

### Проблема с загрузкой Google Forms

Если Google Form не загружается в iframe:

1. Убедитесь, что ссылка правильная и форма доступна
2. Проверьте настройки приватности Google Form
3. Используйте кнопку "Открыть в новой вкладке"

### Ошибки Django

```bash
# Проверьте миграции
python manage.py showmigrations

# Примените миграции
python manage.py migrate

# Проверьте логи
tail -f logs/django.log
```

### Проблемы с Redis

```bash
# Проверьте статус Redis
redis-cli ping

# Должен ответить: PONG
```

## 📈 Дополнительные возможности

### Добавление новых языков

1. Добавьте язык в `settings.py`:
```python
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    ('uz', 'O\'zbek'),
    ('kk', 'Қазақша'),  # Новый язык
]
```

2. Создайте переводы:
```bash
python manage.py makemessages -l kk
python manage.py compilemessages
```

### Кастомизация Unfold

Отредактируйте `config/unfold_settings.py` для изменения:
- Цветовой схемы
- Логотипа и иконок
- Структуры меню
- Дашборда

### API расширения

Добавьте новые эндпоинты в `apps/surveys/views.py` и `apps/surveys/urls.py`.

## 🤝 Вклад в проект

1. Форкните проект
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле `LICENSE`.

## 📞 Поддержка

Если у вас есть вопросы или проблемы:

1. Проверьте существующие Issues
2. Создайте новый Issue с подробным описанием
3. Приложите логи и скриншоты при необходимости

---

**Создано с ❤️ с использованием Django, Unfold и Google Forms** 