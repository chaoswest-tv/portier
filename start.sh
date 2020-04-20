#!/bin/sh

migrate() {
  python manage.py makemigrations
  python manage.py migrate
}

case $1 in
  "create_superuser" )
    python manage.py createsuperuser --no-input --username "${ADMIN_USER:-admin}" --email "${ADMIN_EMAIL:-post@chaoswest.tv}"
    ;;
  "migrate_start" )
    migrate
    gunicorn -w 4 --bind 0.0.0.0:${EXPOSE_PORT:-8000} portier.wsgi
    ;;
  "only_start" )
    gunicorn -w 4 --bind 0.0.0.0:${EXPOSE_PORT:-8000} portier.wsgi
    ;;
esac
