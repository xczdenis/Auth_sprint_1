#!/bin/bash

set -e

. ./scripts/helpers.sh
. ./scripts/logger.sh
. ./scripts/run_command_with_logs.sh

check_env_is_activated

log_header "Lint project"
run_command_with_logs "Check black" "black --check ."
run_command_with_logs "Check isort" "isort --check-only ."
run_command_with_logs "Check flake8" "flake8 ."
run_command_with_logs "Check unused imports and variables" "autoflake -r --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports ."
