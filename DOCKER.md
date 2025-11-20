# Docker Configuration для MVS Clothing

## Структура проекта

Проект состоит из следующих сервисов:
- **db_clothing** - PostgreSQL база данных
- **redis_clothing** - Redis для Celery
- **web_clothing** - Django бэкенд (порт 8002)
- **celery_clothing** - Celery worker для фоновых задач
- **frontend_clothing** - Vue.js фронтенд
- **nginx_clothing** - Nginx reverse proxy (порты 8002 и 8443)

## Быстрый старт

### 1. Настройка окружения

Перед запуском убедитесь, что у вас установлены:
- Docker (версия 20.10+)
- Docker Compose (версия 2.0+)

### 2. Настройка переменных окружения

#### Backend (.env уже создан)
```bash
# Файл backend/.env уже существует
# ВАЖНО: Измените следующие значения для продакшена:
# - SECRET_KEY (используйте надежный ключ)
# - DB_PASSWORD (используйте надежный пароль)
```

#### Frontend (.env уже создан)
```bash
# Файл frontend/.env уже существует
# При необходимости измените VITE_API_URL
```

### 3. Запуск в режиме разработки

#### Локальная разработка фронтенда (без Docker)
```bash
cd frontend
npm install
npm run dev
# Фронтенд будет доступен на http://localhost:5173
```

#### Локальная разработка бэкенда (без Docker)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8002
```

### 4. Запуск в Docker (Production-ready)

#### Первый запуск
```bash
# 1. Соберите и запустите все контейнеры
docker-compose up -d --build

# 2. Проверьте статус контейнеров
docker-compose ps

# 3. Просмотрите логи
docker-compose logs -f

# 4. Создайте суперпользователя Django
docker-compose exec web_clothing python manage.py createsuperuser
```

#### Последующие запуски
```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Остановка с удалением volumes (ОСТОРОЖНО: удалит данные БД!)
docker-compose down -v
```

## Управление контейнерами

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис (правильное имя контейнера!)
docker logs mvs-clothing_web -f
docker logs mvs-clothing_frontend -f
docker logs mvs-clothing_nginx -f
docker logs mvs-clothing_db -f
docker logs mvs-clothing_redis -f
docker logs mvs-clothing_celery -f
```

### Выполнение команд внутри контейнеров

```bash
# Django миграции
docker-compose exec web_clothing python manage.py migrate

# Создание суперпользователя
docker-compose exec web_clothing python manage.py createsuperuser

# Django shell
docker-compose exec web_clothing python manage.py shell

# Доступ к PostgreSQL
docker-compose exec db_clothing psql -U mvs_clothing_user -d mvs_clothing_db

# Доступ к bash контейнера
docker-compose exec web_clothing bash
docker-compose exec frontend_clothing sh
```

### Перезапуск сервисов

```bash
# Перезапуск всех сервисов
docker-compose restart

# Перезапуск конкретного сервиса
docker-compose restart web_clothing
docker-compose restart frontend_clothing
docker-compose restart nginx_clothing
```

## Обновление кода

### После изменений в коде

#### Backend
```bash
# Пересобрать и перезапустить бэкенд
docker-compose up -d --build web_clothing celery_clothing

# Применить миграции (если были изменения в моделях)
docker-compose exec web_clothing python manage.py makemigrations
docker-compose exec web_clothing python manage.py migrate

# Собрать статику
docker-compose exec web_clothing python manage.py collectstatic --noinput
```

#### Frontend
```bash
# Пересобрать и перезапустить фронтенд
docker-compose up -d --build frontend_clothing
```

## Проверка работоспособности

### Health checks

```bash
# Проверка статуса контейнеров
docker-compose ps

# Все контейнеры должны показывать статус "healthy" или "Up"
```

### Доступ к приложению

После запуска приложение будет доступно по следующим адресам:

- **Frontend**: http://mvs-clothing.site:8002 или https://mvs-clothing.site:8443
- **Django Admin**: http://mvs-clothing.site:8002/admin или https://mvs-clothing.site:8443/admin
- **API**: http://mvs-clothing.site:8002/api или https://mvs-clothing.site:8443/api
- **Health Check**: http://mvs-clothing.site:8002/health

## Решение проблем

### Контейнер не запускается

1. **Проверьте логи**:
   ```bash
   docker logs mvs-clothing_web --tail 100
   ```

2. **Проверьте, что порты не заняты**:
   ```bash
   lsof -i :8002  # Linux/Mac
   netstat -ano | findstr :8002  # Windows
   ```

3. **Проверьте .env файл**:
   ```bash
   cat backend/.env
   ```

### База данных не подключается

1. **Убедитесь, что контейнер БД запущен**:
   ```bash
   docker-compose ps db_clothing
   ```

2. **Проверьте логи БД**:
   ```bash
   docker logs mvs-clothing_db
   ```

3. **Проверьте подключение**:
   ```bash
   docker-compose exec web_clothing python manage.py dbshell
   ```

### Ошибка "No such container: web_clothing"

**ВАЖНО**: Имя контейнера в docker-compose.yml - `mvs-clothing_web`, а не `web_clothing`!

Используйте правильное имя:
```bash
# Неправильно:
docker logs web_clothing

# Правильно:
docker logs mvs-clothing_web
```

### Frontend не отображается

1. **Проверьте логи nginx**:
   ```bash
   docker logs mvs-clothing_nginx
   ```

2. **Проверьте логи фронтенда**:
   ```bash
   docker logs mvs-clothing_frontend
   ```

3. **Проверьте nginx конфигурацию**:
   ```bash
   docker-compose exec nginx_clothing nginx -t
   ```

### Celery не обрабатывает задачи

1. **Проверьте логи Celery**:
   ```bash
   docker logs mvs-clothing_celery -f
   ```

2. **Проверьте подключение к Redis**:
   ```bash
   docker-compose exec redis_clothing redis-cli -p 6380 ping
   ```

## Бэкап и восстановление

### Бэкап базы данных

```bash
# Создать бэкап
docker-compose exec -T db_clothing pg_dump -U mvs_clothing_user mvs_clothing_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Или с использованием tar
docker-compose exec -T db_clothing pg_dump -U mvs_clothing_user -F t mvs_clothing_db > backup_$(date +%Y%m%d_%H%M%S).tar
```

### Восстановление базы данных

```bash
# Из SQL файла
docker-compose exec -T db_clothing psql -U mvs_clothing_user mvs_clothing_db < backup_file.sql

# Из tar файла
docker-compose exec -T db_clothing pg_restore -U mvs_clothing_user -d mvs_clothing_db < backup_file.tar
```

## Производство (Production)

### Перед деплоем

1. **Обновите SECRET_KEY** в `backend/.env`
2. **Обновите пароли БД** в `backend/.env` и `docker-compose.yml`
3. **Установите DEBUG=False** в `backend/.env`
4. **Настройте SSL сертификаты** для HTTPS
5. **Проверьте ALLOWED_HOSTS** в `backend/.env`
6. **Проверьте CORS_ALLOWED_ORIGINS** в `backend/.env`

### SSL/TLS сертификаты

Для работы HTTPS необходимы SSL сертификаты в `/etc/letsencrypt/`.

Для получения сертификатов используйте Certbot:
```bash
sudo certbot certonly --standalone -d mvs-clothing.site -d www.mvs-clothing.site
```

## Мониторинг

### Использование ресурсов

```bash
# Просмотр использования ресурсов контейнерами
docker stats

# Конкретный контейнер
docker stats mvs-clothing_web
```

### Очистка

```bash
# Очистка неиспользуемых образов
docker image prune -a

# Очистка неиспользуемых volumes
docker volume prune

# Полная очистка (ОСТОРОЖНО!)
docker system prune -a --volumes
```

## Дополнительная информация

- Django Admin: `/admin`
- API документация: `/api/docs` (если настроена)
- Static файлы: `/static/`
- Media файлы: `/media/`

## Контакты и поддержка

При возникновении проблем проверьте:
1. Логи контейнеров
2. Статус health checks
3. Конфигурацию nginx
4. Переменные окружения
