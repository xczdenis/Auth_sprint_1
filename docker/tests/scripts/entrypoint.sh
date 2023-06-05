#!/bin/sh
set -e

. ./scripts/logger.sh

./scripts/wait-dependencies.sh

. ./.venv/bin/activate

log_info "Upgrade database"
echo "${FLASK_APP}"
FLASK_APP=src/movies_auth/main.py python -m flask db upgrade
echo ""

./scripts/start.sh

exec "$@"
