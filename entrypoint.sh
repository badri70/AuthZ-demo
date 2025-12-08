#!/bin/sh

echo "Waiting for Postgres to be ready..."
while ! nc -z db 5432; do
  sleep 0.5
done
echo "Postgres is ready!"

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Checking if users already exist..."
USER_COUNT=$(python - <<EOF
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from accounts.models import User
print(User.objects.count())
EOF
)

if [ "$USER_COUNT" = "0" ]; then
    echo "No users found. Loading fixtures..."
    python manage.py loaddata users.json
else
    echo "Users already exist. Skipping fixture load."
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn core.wsgi:application --bind 0.0.0.0:8000