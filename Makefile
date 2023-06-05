DEFAULT_PROJECT_NAME=movies_ugc

PREFIX_DEV=dev
PREFIX_TEST=test
PREFIX_PROD=prod

CURRENT_ENVIRONMENT_PREFIX=PREFIX_DEV

DOCKER_COMPOSE_MAIN_FILE=docker-compose.yml
DOCKER_COMPOSE_DEV_FILE=docker-compose.dev.yml
DOCKER_COMPOSE_PROD_FILE=docker-compose.prod.yml
DOCKER_COMPOSE_TEST_FILE_NAME=docker-compose.test.yml
DOCKER_COMPOSE_TEST_DEV_FILE=docker-compose.test.dev.yml

COMPOSE_OPTION_START_AS_DEMON=up -d --build
COMPOSE_PROFILE_DEFAULT=""--profile default""

# define standard colors
ifneq (,$(findstring xterm,${TERM}))
	BLACK        := $(shell printf "\033[30m")
	RED          := $(shell printf "\033[91m")
	GREEN        := $(shell printf "\033[92m")
	YELLOW       := $(shell printf "\033[33m")
	BLUE         := $(shell printf "\033[94m")
	PURPLE       := $(shell printf "\033[95m")
	ORANGE       := $(shell printf "\033[93m")
	WHITE        := $(shell printf "\033[97m")
	RESET        := $(shell printf "\033[00m")
else
	BLACK        := ""
	RED          := ""
	GREEN        := ""
	YELLOW       := ""
	BLUE         := ""
	PURPLE       := ""
	ORANGE       := ""
	WHITE        := ""
	RESET        := ""
endif

# read env variables from .env
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

# looking for docker-compose files
ifeq (,$(wildcard ./${DOCKER_COMPOSE_PROD_FILE}))
	DOCKER_COMPOSE_PROD_FILE=_
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_DEV_FILE}))
	DOCKER_COMPOSE_DEV_FILE=_
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_TEST_FILE_NAME}))
	DOCKER_COMPOSE_TEST_FILE=_
else
	DOCKER_COMPOSE_TEST_FILE=${DOCKER_COMPOSE_TEST_FILE_NAME}
endif
ifeq (,$(wildcard ./${DOCKER_COMPOSE_TEST_DEV_FILE}))
	DOCKER_COMPOSE_TEST_DEV_FILE=_
endif

# set envs if they are not defined
ifeq ($(COMPOSE_PROJECT_NAME),)
	COMPOSE_PROJECT_NAME=$(DEFAULT_PROJECT_NAME)
endif
ifeq ($(DOCKER_BUILDKIT),)
	DOCKER_BUILDKIT=1
endif
ifeq ($(ENVIRONMENT),)
	ENVIRONMENT=production
endif
ifeq ($(ENVIRONMENT), development)
   CURRENT_ENVIRONMENT_PREFIX=${PREFIX_DEV}
else
   CURRENT_ENVIRONMENT_PREFIX=${PREFIX_PROD}
endif


define log
	@echo ""
	@echo "${WHITE}----------------------------------------${RESET}"
	@echo "${BLUE}$(strip ${1})${RESET}"
	@echo "${WHITE}----------------------------------------${RESET}"
endef


define run_docker_compose_for_env
	@if [ $(strip ${2}) != "_" ]; then \
		make run_docker_compose_for_env \
			env=$(strip ${1}) \
			override_file="-f ${2}" \
			cmd=$(strip ${3}); \
    else \
		make run_docker_compose_for_env \
			env=$(strip ${1}) \
			cmd=$(strip ${3}); \
    fi
endef
run_docker_compose_for_env:
	@if [ $(strip ${env}) != "_" ]; then \
		DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
		COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
		docker-compose \
			-f ${DOCKER_COMPOSE_MAIN_FILE} \
			$(strip ${override_file}) \
			$(strip ${cmd}); \
    else \
		DOCKER_BUILDKIT=${DOCKER_BUILDKIT} \
		COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
		docker-compose \
			-f ${DOCKER_COMPOSE_MAIN_FILE} \
			$(strip ${override_file}) \
			$(strip ${cmd}); \
    fi


define run_docker_compose_for_current_env
	@if [ ${CURRENT_ENVIRONMENT_PREFIX} = ${PREFIX_DEV} ]; then \
		if [ "${DOCKER_COMPOSE_DEV_FILE}" != "_" ]; then \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				override_file="-f ${DOCKER_COMPOSE_DEV_FILE}" \
				cmd="$(strip ${1})"; \
		else \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				cmd="$(strip ${1})"; \
		fi \
    elif [ ${CURRENT_ENVIRONMENT_PREFIX} = ${PREFIX_PROD} ]; then \
		if [ "${DOCKER_COMPOSE_PROD_FILE}" != "_" ]; then \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				override_file="-f ${DOCKER_COMPOSE_PROD_FILE}" \
				cmd="$(strip ${1})"; \
		else \
			make run_docker_compose_for_env \
				env=${CURRENT_ENVIRONMENT_PREFIX} \
				cmd="$(strip ${1})"; \
		fi \
    fi
endef


.PHONY: init
init:
	@./src/scripts/init.sh


.PHONY: lint
lint:
	@./src/scripts/lint.sh


.PHONY: format
format:
	@./src/scripts/format.sh


# remove all existing containers, volumes, images
.PHONY: remove
remove:
	@clear
	@echo "${RED}----------------!!! DANGER !!!----------------"
	@echo "Вы собираетесь удалить все неиспользуемые образы, контейнеры и тома."
	@echo "Будут удалены все незапущенные контейнеры, все образы для незапущенных контейнеров и все тома для незапущенных контейнеров"
	@read -p "${ORANGE}Вы точно уверены, что хотите продолжить? [yes/n]: ${RESET}" TAG \
	&& if [ "_$${TAG}" != "_yes" ]; then echo "Nothing happened"; exit 1 ; fi
	docker-compose down --rmi all --volumes --remove-orphans && docker system prune -a --volumes --force


# create .env and .env.local files if they are not exist
.PHONY: env
env:
	@if [ -f .env ]; then \
		read -p "File ${GREEN}.env${RESET} already exists. Overwrite it [y/n]:${RESET} " yn; \
        case $$yn in \
            [Yy]* ) cp .env.template .env; echo "File ${GREEN}.env${RESET} has been overwritten!";; \
            * ) echo "Nothing happened";; \
        esac \
    else \
        cp .env.template .env; \
        echo "File ${GREEN}.env${RESET} created from ${GREEN}.env.template${RESET}!"; \
    fi


# stop and remove all running containers
.PHONY: down _down-prod _down-dev _down-test
down:
	$(call log, Down containers)
	@make _down-prod
	@make _down-dev
	@make _down-test
_down-prod:
	$(call run_docker_compose_for_env, "${PREFIX_PROD}", "${DOCKER_COMPOSE_PROD_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_PROD_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
_down-dev:
	$(call run_docker_compose_for_env, "${PREFIX_DEV}", "${DOCKER_COMPOSE_DEV_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_DEV_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
_down-test:
	$(call run_docker_compose_for_env, "${PREFIX_TEST}", "${DOCKER_COMPOSE_TEST_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")
	$(call run_docker_compose_for_env, "_", "${DOCKER_COMPOSE_TEST_FILE}", "${COMPOSE_PROFILE_DEFAULT} down")


# build and run docker containers in demon mode
.PHONY: run
run: down
	$(call log, Run containers (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, --profile default ${COMPOSE_OPTION_START_AS_DEMON} ${s})


# build and run docker containers in demon mode for db profile
.PHONY: run-db
run-db: down
	$(call log, Run containers for db profile (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, --profile db ${COMPOSE_OPTION_START_AS_DEMON} ${s})


# show container's logs
.PHONY: logs _logs
logs:
	@read -p "${ORANGE}Container name: ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make _logs s="$${_TAG}"; \
	else \
	    echo aborting; exit 1; \
	fi
_logs:
	$(call run_docker_compose_for_current_env, logs ${s})


# run bash into container
.PHONY: bash _bash
bash:
	@read -p "${ORANGE}Container name: ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make _bash s="$${_TAG}"; \
	else \
	    echo aborting; exit 1; \
	fi
_bash:
	$(call run_docker_compose_for_current_env, exec -it ${s} bash)


# stop containers
.PHONY: stop _stop
stop:
	@read -p "${ORANGE}Containers name (press Enter to stop all containers): ${RESET}" _TAG && \
	if [ "_$${_TAG}" != "_" ]; then \
		make _stop s="$${_TAG}"; \
	else \
	    make _stop; \
	fi
_stop:
	$(call log, Stop containers (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, stop ${s})


# show docker-compose configuration
.PHONY: config
config:
	$(call log, Docker-compose configuration (${CURRENT_ENVIRONMENT_PREFIX}))
	$(call run_docker_compose_for_current_env, ${COMPOSE_PROFILE_DEFAULT} config)


# build and run tests in docker
.PHONY: tests-docker
tests-docker: down
	$(call log, Run tests in docker)
	@if [ "${DOCKER_COMPOSE_TEST_FILE}" != "_" ]; then \
		make run_docker_compose_for_env \
			env=${PREFIX_TEST} \
			override_file="-f ${DOCKER_COMPOSE_TEST_FILE}" \
			cmd="--profile default --profile tests build"; \
    	make run_docker_compose_for_env \
			env=${PREFIX_TEST} \
			override_file="-f ${DOCKER_COMPOSE_TEST_FILE}" \
			cmd="--profile default --profile tests run tests"; \
	else \
		echo "${RED}ERROR:${RESET} No such file '${DOCKER_COMPOSE_TEST_FILE_NAME}'. Tests cannot be run."; \
	fi \


.PHONY: tests
tests:
	@cd $(CURDIR) && python -m pytest


.PHONY: db-migrate
db-migrate:
	@read -p "Enter comment for your migration: " comment; \
	if [ -z "$$comment" ]; then \
		echo "Migration comment is required!"; \
	else \
		FLASK_APP=src/movies_auth/main.py python -m flask db migrate -m "$$comment"; \
	fi


.PHONY: db-upgrade
db-upgrade:
	@FLASK_APP=src/movies_auth/main.py python -m flask db upgrade


.PHONY: su
su:
	@FLASK_APP=src/movies_auth/main.py python -m flask createsuperuser ${SUPERUSER_LOGIN} ${SUPERUSER_PASSWORD}


.PHONY: run-local
run-local:
	@python src/movies_auth/main.py
