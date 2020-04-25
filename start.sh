#!/bin/sh

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

migrate() {
  python manage.py makemigrations
  python manage.py migrate
}

wait_for_redis
wait_for_database
migrate
supervisord -n -c /etc/supervisord.conf
