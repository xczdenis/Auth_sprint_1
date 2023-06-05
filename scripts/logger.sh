#!/bin/bash


. ./scripts/utils.sh
. ./scripts/colors.sh

get_color_for_log_level() {
    case $1 in
    info)
        printf "${color_info}"
        ;;
    debug)
        printf "${color_debug}"
        ;;
    success)
        printf "${color_success}"
        ;;
    error)
        printf "${color_error}"
        ;;
    white)
        ${color_white}
        ;;
    reset)
        printf "${color_reset}"
        ;;
    *)
        printf "${color_reset}"
        ;;
    esac
}

get_log_level_text_part() {
    case $1 in
    info)
        printf "INFO     "
        ;;
    debug)
        printf "DEBUG    "
        ;;
    success)
        printf "SUCCESS  "
        ;;
    error)
        printf "ERROR    "
        ;;
    *)
        printf ""
        ;;
    esac
}

log() (
    log_level=$1
    text=$2

    text_color=$(get_color_for_log_level "${log_level}")
    text_color_reset=$(get_color_for_log_level "reset")
    log_level_text=$(get_log_level_text_part "${log_level}")
    current_time=$(date +"%Y-%m-%d %H:%M:%S.%3N")

    echo "${color_green}${current_time} ${color_reset}| ${text_color}${log_level_text}${color_reset}| ${text_color}${text}${text_color_reset}"
)

log_debug() (
    text=$1
    log "debug" "${text}"
)

log_info() (
    text=$1
    log "info" "${text}"
)

log_success() (
    text=$1
    log "success" "${text}"
)

log_error() (
    text=$1
    log "error" "${text}"
)

log_header() (
    text=${1}

    echo ""
    echo "${color_white}----------------------------------------${color_reset}"
    echo "${color_blue}${text}${color_reset}"
    echo "${color_white}----------------------------------------${color_reset}"
)
