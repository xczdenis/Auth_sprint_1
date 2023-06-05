#!/bin/bash

set -e

. ./scripts/helpers.sh
. ./scripts/logger.sh
. ./scripts/run_command_with_logs.sh

check_env_is_activated

log_header "Format project"
run_command_with_logs "Remove unused imports and variables" "autoflake -i -r --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports ."
run_command_with_logs "Format with black" "black ."
run_command_with_logs "Isort" "isort ."
