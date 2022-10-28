ARG env=${ENVIRONMENT:-production}

FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

ARG HOME_DIR=/src
WORKDIR $HOME_DIR

COPY ./scripts/wait-for-it.sh /wait-for-it.sh
RUN chmod a+x /wait-for-it.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev=3.9.2-3 \
        libpq-dev=13.8-0+deb11u1 \
        build-essential=12.9 \
    && pip install --no-cache-dir poetry==1.2.2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./pyproject.toml ./poetry.lock /
RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY ./docker/app/scripts /scripts
RUN chmod -R 777 /scripts

FROM builder as development

FROM builder as production
COPY ./src .

FROM ${env}

ENTRYPOINT ["/scripts/entrypoint.sh"]
