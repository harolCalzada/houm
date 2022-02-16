FROM python:3.10-slim-buster
RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y \
    build-essential gcc libffi-dev make cmake python3-dev musl-dev libsodium-dev libpq-dev\
    binutils libproj-dev gdal-bin \
    postgresql python-psycopg2

RUN mkdir /www
WORKDIR /www

RUN groupadd webapps
RUN useradd webapp -G webapps
RUN mkdir -p /www/logs/ && chown -R webapp /www/logs/ && chmod -R u+rX /www/logs/


COPY ./src/ ./src
COPY ./requirements ./requirements
RUN pip install -r ./requirements/local.txt
COPY ./server-config/local/entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh
# CMD ["sh", "./entrypoint.sh"]
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
