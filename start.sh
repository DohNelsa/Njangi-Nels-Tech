#!/usr/bin/env bash
# Startup script for Render - runs migrations then starts gunicorn

set -e

echo "Running startup migrations..."
python manage.py migrate --no-input || {
    echo "WARNING: Migrations failed at startup"
}

echo "Starting gunicorn..."
exec gunicorn nja_platform.wsgi

