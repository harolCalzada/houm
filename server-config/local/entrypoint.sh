#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"

python ./src/manage.py migrate  --settings=config.settings.local

python ./src/manage.py runserver 0.0.0.0:8000 --settings=config.settings.local
