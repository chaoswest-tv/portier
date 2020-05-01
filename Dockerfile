FROM python:3.8-alpine
WORKDIR /app

# set env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# https://github.com/twbs/bootstrap/issues/30553 don't upgrade jquery to 3.5.0 yet
ENV JQUERY_VERSION=3.4.1
ENV BOOTSTRAP_VERSION=4.4.1
ENV INTER_VERSION=3.13

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

# add static external libraries for frontend
RUN wget http://code.jquery.com/jquery-${JQUERY_VERSION}.min.js -O /app/static/js/jquery.min.js \
    && wget https://stackpath.bootstrapcdn.com/bootstrap/${BOOTSTRAP_VERSION}/js/bootstrap.bundle.min.js -O /app/static/js/bootstrap.bundle.min.js \
    && mkdir -p /tmp/inter /app/static/fonts \
    && cd /tmp/inter && wget https://github.com/rsms/inter/releases/download/v${INTER_VERSION}/Inter-${INTER_VERSION}.zip \
    && unzip Inter-${INTER_VERSION}.zip  && mv /tmp/inter/Inter\ Web/* /app/static/fonts/ \
    && cd - \
    && rm -rf /tmp/inter \
    && chown -R portier:portier /app/static/fonts/

# collect static files and compile localized strings
RUN ./manage.py collectstatic --noinput --link
RUN ./manage.py compilemessages

CMD ["/app/start.sh"]
