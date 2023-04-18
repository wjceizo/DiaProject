FROM alpine:3.17

RUN set -eux; \
    apk add --update --no-cache \
        http-parser \
        libev \
        mariadb-connector-c \
        musl \
        py3-alembic \
        py3-click \
        py3-dotenv \
        py3-flask \
        py3-flask-restful \
        py3-jwt \
        py3-pip \
        py3-sqlalchemy \
        py3-werkzeug \
        py3-wheel \
        tini \
    ; \
    apk add --no-cache --virtual .build-deps \
        alpine-sdk \
        http-parser-dev \
        libev-dev \
        mariadb-connector-c-dev \
        python3-dev \
    ; \
    pip install \
        bjoern \
        flask_jwt_extended \
        flask_migrate \
        flask_smorest \
        Flask_SQLAlchemy \
        marshmallow \
        mysqlclient \
    ; \
    pip cache purge; \
    apk del .build-deps

COPY . /app

RUN sed -i "s|127.0.0.1|0.0.0.0|g" /app/Diapp.py

VOLUME /app/records

EXPOSE 5000
WORKDIR /app

ENTRYPOINT ["/sbin/tini", "--", "/app/Diapp.py"]
