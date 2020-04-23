#!/bin/sh

migrate() {
  python manage.py makemigrations
  python manage.py migrate
}

wait_for_redis() {
  echo "Trying to connect to redis at ${REDIS_HOST:-redis}:${REDIS_PORT:-6379} ..."
  while ! nc -z ${REDIS_HOST:-redis} ${REDIS_PORT:-6379};
  do
    sleep 1;
  done;
  echo "Successfully connected to redis. Continuing.";
}

wait_for_database() {
  echo "Trying to connect to database at ${SQL_HOST:-postgres}:${SQL_PORT:-5432} ..."
  while ! nc -z ${SQL_HOST:-postgres} ${SQL_PORT:-5432};
  do
    sleep 1;
  done;
  echo "Successfully connected to database. Continuing.";
}

case $1 in
  "create_superuser" )
    wait_for_redis
    wait_for_database
    python manage.py createsuperuser --no-input --username "${ADMIN_USER:-admin}" --email "${ADMIN_EMAIL:-post@chaoswest.tv}"
    ;;
  "migrate_start" )
    wait_for_redis
    wait_for_database
    migrate
    gunicorn -w 4 --bind 0.0.0.0:${EXPOSE_PORT:-8000} portier.wsgi
    ;;
  "only_start" )
    wait_for_redis
    wait_for_database
    gunicorn -w 4 --bind 0.0.0.0:${EXPOSE_PORT:-8000} portier.wsgi
    ;;
esac
