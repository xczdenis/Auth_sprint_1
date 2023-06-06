ARG env=production
ARG img=python:3.11-slim
ARG work_dir=app
ARG pckg_name=movies_auth

FROM ${img} as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.5.0

ARG env
ARG work_dir
ARG pckg_name

WORKDIR ${work_dir}


FROM base as builder

COPY ./scripts ./scripts
COPY ./docker/${pckg_name}/scripts ./scripts
RUN chmod -R 777 ./scripts

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-dev \
        libpq-dev \
        build-essential \
    && pip install poetry==${POETRY_VERSION} \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock README.md ./

RUN mkdir -p /${work_dir}/src/${pckg_name} && touch /${work_dir}/src/${pckg_name}/__init__.py

RUN poetry config virtualenvs.in-project true \
    && poetry install --only main


FROM base as final

COPY --from=builder /${work_dir}/scripts ./scripts
COPY --from=builder /${work_dir}/.venv ./.venv


FROM final as development


FROM final as production

COPY ./src/${pckg_name} ./src/${pckg_name}


FROM ${env}

ENTRYPOINT ["./scripts/entrypoint.sh"]
