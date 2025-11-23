# Базовый образ Python
FROM python:3.11-slim

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-openbsd \
    gcc \
    python3-dev \
    musl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r django && useradd -r -g django django

# Создание рабочей директории
WORKDIR /app

# Создание директорий для логов, статики и медиа с правильными правами
RUN mkdir -p /app/logs /app/staticfiles /app/media && \
    chown -R django:django /app

# Копирование requirements.txt
COPY --chown=django:django requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY --chown=django:django . .

# Установка прав на директории
RUN chmod -R 755 /app && \
    chmod -R 775 /app/logs /app/staticfiles /app/media && \
    chown -R django:django /app/logs /app/staticfiles /app/media

# Копирование и установка прав на entrypoint скрипты
COPY --chown=django:django entrypoint.sh /entrypoint.sh
COPY --chown=django:django entrypoint-celery.sh /entrypoint-celery.sh
RUN chmod +x /entrypoint.sh /entrypoint-celery.sh

# Переключение на пользователя django
USER django

# Экспонирование порта
EXPOSE 8000

# Запуск entrypoint скрипта
ENTRYPOINT ["/entrypoint.sh"]
