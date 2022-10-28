#!/bin/sh
set -e

if [ "x$COMPOSE_MODE" = 'xon' ]; then
    echo "\033[94mCOMPOSE_MODE is on\033[00m"
    /scripts/wait-dependencies.sh
    echo "\033[01;32mAll services is up!\033[00m"
    echo ""
fi

python -m flask db upgrade

if [ "x$CREATE_SUPER_USER" = "xTrue" ]; then
    echo ""
    echo "\033[94mCreate superuser\033[00m"
    python -m flask createsuperuser $SUPERUSER_LOGIN $SUPERUSER_PASSWORD
    echo ""
fi

/scripts/start.sh

exec "$@"
