#!/bin/sh
if [ "x$ENVIRONMENT" = 'xdevelopment' ]; then
    echo "\033[94mRun in development mode\033[00m"
    gunicorn -b $APP_HOST:$APP_PORT -w 4 manage:app
else
    echo "\033[94mRun in production mode mode\033[00m"
    gunicorn -b $APP_HOST:$APP_PORT -w 4 wsgi:app
fi
