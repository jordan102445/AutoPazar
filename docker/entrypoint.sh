#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "${AUTO_SYNC_REFERENCE_DATA:-false}" = "true" ]; then
  python manage.py sync_reference_data
fi

if [ "${AUTO_SEED_DEMO_DATA:-false}" = "true" ]; then
  python manage.py seed_demo_data
fi

exec "$@"
