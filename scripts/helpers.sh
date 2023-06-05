#!/bin/bash

. ./scripts/logger.sh
. ./scripts/colors.sh

check_service() (
    service_name=$1
    host=$2
    port=$3

    log_info "Waiting the service: ${color_white}${service_name} (url=${host}:${port})"
    ./scripts/wait-for-it.sh "${host}":"${port}" -t 120 --
    log_success "${service_name} is up!${color_reset}"
    echo ""
)

check_env_is_activated() (
    if [[ -z "$VIRTUAL_ENV" ]]; then
        echo "${color_red}ERROR: Python virtual environment is not activated!${color_reset}"
        echo "Please make sure that virtual environment is activated and then run your command again."
        exit 1
    fi
)
