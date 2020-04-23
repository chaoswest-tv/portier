FROM python:3.8-alpine
WORKDIR /app

# set env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev gettext postgresql-client

# install dependencies
ADD ./requirements.txt .
RUN pip install -r requirements.txt

# add user
RUN addgroup -S portier && adduser -S portier -G portier

# add code
ADD --chown=portier:portier . /app

RUN ./manage.py collectstatic --noinput --link
RUN ./manage.py compilemessages
USER portier

CMD ["/app/start.sh", "migrate_start"]
