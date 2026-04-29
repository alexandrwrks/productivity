#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until python -c "import os, psycopg2; psycopg2.connect(os.environ['SYNC_DATABASE_URL']).close()" >/dev/null 2>&1; do
  sleep 2
done

echo "Applying migrations..."
python -m alembic upgrade head

echo "Starting bot..."
python -m app.main
