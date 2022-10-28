ARG env=${ENVIRONMENT:-production}

FROM postgres:14.3-alpine as builder

FROM builder as development
EXPOSE 5432

FROM builder as production

FROM ${env}
