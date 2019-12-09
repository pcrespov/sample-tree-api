#
#
#

.DEFAULT_GOAL := help
DEFAULT_PORT  ?= 8081


export APP_NAME=tree-api
export APP_VERSION=$(shell cat VERSION)

export DOCKER_IMAGE_NAME=local/tree-api:latest

export BUILD_DATE:=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
export VCS_URL:=$(shell git config --get remote.origin.url)
export VCS_REF:=$(shell git rev-parse HEAD)

# TODO cannot build if dirty
export VCS_IS_DIRTY=$(shell git status -s)


# SRC_DIR=$(cd "${PWD}/../../group-crespo/supermash"; pwd)
SRC_DIR=/home/crespo/devp/group-crespo/supermash
BUILD_DIR=${SRC_DIR}-build
BUILD_BIN_DIR=${BUILD_DIR}/_bin

# lib environs
export LD_LIBRARY_PATH=${BUILD_BIN_DIR}
export PYTHONPATH=${BUILD_BIN_DIR}

.venv:
	# creating virtual environment
	@python3 -m venv .venv
	@.venv/bin/pip --no-cache install -U pip setuptools wheel


.PHONY: devenv
devenv: src/simcore_service_tree.egg-info ## builds development environment
	# extra tools
	@.venv/bin/pip --no-cache install \
		bump2version \
		pip-tools

src/simcore_service_tree.egg-info: .venv
	# installing dependencies
	@.venv/bin/pip install -r requirements/_test.txt
	# installing in edit mode
	@.venv/bin/pip install -e .

up-devel: devenv ## starts server in development mode
	@.venv/bin/simcore-service-api --port=${DEFAULT_PORT}


.PHONY: tests
tests: devenv ## run unit tests
	@.venv/bin/pytest -vv -x -s --pdb tests/test_data_nodes.py

.PHONY: shell
shell: ## python shell
	@.venv/bin/python3


.PHONY: build
build: docker-compose.yml
	# building ${DOCKER_IMAGE_NAME}
	@docker-compose -f $< build
	# Adding swiss.itisfoundation.python.requirements label
	@export PIP_REQUIREMENTS="$(shell docker run -it --entrypoint python ${DOCKER_IMAGE_NAME} -m pip list --format=json)"; docker-compose -f $< build


.PHONY: info-labels
info-labels:
	## docker inspect -f "{{json .Config.Labels }}" ${DOCKER_IMAGE_NAME}
	docker image inspect ${DOCKER_IMAGE_NAME} | jq .[0].Config.Labels



.PHONY: clean
clean: .check-clean ## cleans unversioned and ignored files
	# remove unversioned
	-@git clean -dfx

.check-clean:
	@git clean -ndfx
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]


.PHONY: help
help: ## this colorful help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

