#!/bin/bash

set -e

. ./scripts/helpers.sh
. ./scripts/logger.sh
. ./scripts/run_command_with_logs.sh

check_env_is_activated

log_header "Init project"
run_command_with_logs "Installing dependencies" "poetry install"
run_command_with_logs "Installing pre-commit hooks" "pre-commit install"
run_command_with_logs "Installing pre-commit msg check" "pre-commit install --hook-type commit-msg"
