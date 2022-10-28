ARG env=${ENVIRONMENT:-production}

FROM app-movies-auth-img as builder

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

ARG HOME_DIR=/src
WORKDIR $HOME_DIR

RUN poetry config virtualenvs.create false \
    && poetry install --only tests

COPY ./docker/tests/scripts /scripts
RUN chmod -R 777 /scripts

FROM builder as development

FROM builder as production
COPY ./src .

FROM ${env}

ENTRYPOINT ["/scripts/entrypoint.sh"]
