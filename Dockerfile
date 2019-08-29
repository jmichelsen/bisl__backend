# Base Image
FROM python:3.6.5-alpine

# Set execution environment
COPY requirements /requirements

# Install dependencies from repository
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
            gcc \
            make \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            postgresql-dev \
            jpeg-dev \
            zlib-dev \
            libffi-dev \
    && python -m venv --upgrade /bisl \
    && /bisl/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/bisl/bin/pip install --no-cache-dir -r /requirements/dev.txt" \
    && run_deps="$( \
            scanelf --needed --nobanner --recursive /bisl \
                    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                    | sort -u \
                    | xargs -r apk info --installed \
                    | sort -u \
    )" \
    && apk add --virtual .python-rundeps $run_deps \
    && apk del .build-deps

RUN apk add --no-cache \
    curl \
    openssh \
    bash \
    git

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
COPY . /code/

ENV IN_DOCKER=True PATH="/usr/sbin:/usr/bin:/sbin:/bin:/bisl/bin"

RUN python manage.py collectstatic --noinput
CMD gunicorn config.wsgi
