#!/bin/sh
set -e

. ./scripts/colors.sh
. ./scripts/logger.sh
. ./scripts/helpers.sh


check_service "Postgres" "${POSTGRES_HOST}" "${POSTGRES_PORT}"
check_service "Redis" "${REDIS_HOST}" "${REDIS_PORT}"

log_success "All services is up!"
echo ""

exec "$@"
