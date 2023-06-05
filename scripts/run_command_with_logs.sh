#!/bin/bash


. ./scripts/colors.sh

run_command_with_logs() {
    header=${1}
    command=${2}

    echo ""
    echo "[= ${color_blue}${header}${color_reset} =]"
    echo "${color_yellow}run command: ${color_purple}${command}${color_reset}"
    eval ${command} || true
}
