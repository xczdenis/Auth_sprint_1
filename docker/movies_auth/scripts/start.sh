#!/bin/sh
. ./scripts/logger.sh


if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    log_info "Run in development mode"
    python src/movies_auth/main.py
else
    log_info "Run in production mode"
    gunicorn -b "$APP_HOST":"$APP_PORT" -w 4 src.movies_auth.wsgi:app
fi
