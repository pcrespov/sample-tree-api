#
#
#
.DEFAULT_GOAL := help

export APP_NAME=tree-api
export APP_VERSION=$(shell cat VERSION)

export DOCKER_IMAGE_NAME=local/tree-api:latest

export BUILD_DATE:=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
export VCS_URL:=$(shell git config --get remote.origin.url)
export VCS_REF:=$(shell git rev-parse HEAD)

# TODO: cannot build if dirty
export VCS_IS_DIRTY=$(shell git status -s)


# TODO: this is the outdir from supermash!
SRC_DIR=$(abspath ${HOME}/devp/group-crespo/supermash)
BUILD_DIR=${SRC_DIR}-build
BUILD_BIN_DIR=${BUILD_DIR}/_bin


# CREATING DEVEL ENVIRON ---------------

.venv:
	# creating virtual environment
	@python3 -m venv .venv
	@.venv/bin/pip --no-cache install -U pip setuptools wheel


.PHONY: devenv
devenv: .venv ## builds development environment
	# extra tools
	@.venv/bin/pip --no-cache install \
		bump2version \
		pip-tools
	# installed packages
	@.venv/bin/pip list


.PHONY: install-dev install-prod install-ci
install-dev install-prod install-ci: ## install app in development/production or CI mode
	# installing in $(subst install-,,$@) mode
	@.venv/bin/pip3 install -r requirements/$(subst install-,,$@).txt



# RUNNING IN DEVEL ENVIRON ---------------

# lib environs for py-smash
export LD_LIBRARY_PATH=${BUILD_BIN_DIR}
export PYTHONPATH=${BUILD_BIN_DIR}
DEFAULT_PORT  ?= 8081

up-devel: ## starts server in development mode
	@.venv/bin/$(APP_NAME) --port=${DEFAULT_PORT}

.PHONY: tests
tests: ## run unit tests
	@.venv/bin/pytest -vv -x -s --pdb tests/test_data_nodes.py



# DOCKER ---------------

.PHONY: build
build: docker-compose.yml
	# building ${DOCKER_IMAGE_NAME}
	@docker-compose -f $< build
	# Adding swiss.itisfoundation.python.requirements label
	@export PIP_REQUIREMENTS="$(shell docker run -it --entrypoint python ${DOCKER_IMAGE_NAME} -m pip list --format=json)"; docker-compose -f $< build


.PHONY: version-patch version-minor version-major

define bumpversion
	# upgrades as $(subst version-,,$@) version, commits and tags
	@bump2version --verbose --list $(subst version-,,$@)
	@git log -1 --pretty
endef

version-patch: ## bug fixes not affecting the API/minor/major version
	$(bumpversion)
version-minor: ## backwards-compatible API addition or changes
	$(bumpversion)
version-major: ## backwards-INcompatible API changes
	$(bumpversion)




.PHONY: info
info: ## info
	@echo "APP_NAME    = ${APP_NAME}"
	@echo "APP_VERSION = ${APP_VERSION}"
	@docker image inspect ${DOCKER_IMAGE_NAME} | jq .[0].Config.Labels

## docker inspect -f "{{json .Config.Labels }}" ${DOCKER_IMAGE_NAME}


.PHONY: clean
clean: .check-clean ## cleans unversioned and ignored files
	# remove unversioned
	-@git clean -dfx

.check-clean:
	@git clean -ndfx
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]


.PHONY: help
help: ## this colorful help
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
