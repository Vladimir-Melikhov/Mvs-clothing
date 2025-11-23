#!/bin/bash

set -e

echo "Waiting for PostgreSQL..."
REDIS_HOST=$(echo $CELERY_BROKER_URL | sed 's|redis://||' | cut -d':' -f1)
REDIS_PORT=$(echo $CELERY_BROKER_URL | sed 's|redis://||' | cut -d':' -f2 | cut -d'/' -f1)
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 0.1
done
echo "Redis started"

echo "Creating logs directory..."
mkdir -p /app/logs
chmod 775 /app/logs

echo "Starting Celery..."
exec "$@"
