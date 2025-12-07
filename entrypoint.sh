#!/bin/sh

echo "Waiting for Postgres to be ready..."
until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "Postgres is ready!"

echo "Applying migrations..."
poetry run python manage.py migrate --noinput

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
