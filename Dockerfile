FROM python:3.8-alpine
WORKDIR /app

# set env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install required packages
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev gettext postgresql-client nginx supervisor

# install dependencies
ADD ./requirements.txt .
RUN pip install -r requirements.txt

# add supervisor and nginx configs
ADD ./docker/nginx.conf /etc/nginx/nginx.conf
ADD ./docker/supervisord.conf /etc/supervisord.conf

# add user
RUN addgroup -S portier && adduser -S portier -G portier

# add code
ADD --chown=portier:portier . /app
RUN ./manage.py collectstatic --noinput --link
RUN ./manage.py compilemessages

CMD ["/app/start.sh", "migrate_start"]
