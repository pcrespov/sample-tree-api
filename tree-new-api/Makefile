#
# Targets for DEVELOPMENT of tree new api
#

# Makefile config
.DEFAULT_GOAL := help
SHELL = /bin/bash

# Custom variables
export APP_NAME     := $(notdir $(CURDIR))
export APP_VERSION   = $(shell cat VERSION)
APP_CLI_NAME := simcore-service-tree-new-api


# TODO: this is the outdir from supermash!
SRC_DIR=$(abspath ${HOME}/devp/group-crespo/supermash)
BUILD_DIR=${SRC_DIR}-build
BUILD_BIN_DIR=${BUILD_DIR}/_bin

# INSTALLING  ---------------

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

.PHONY: requirements
requirements: ## compiles pip requirements (.in -> .txt)
	@$(MAKE) --directory requirements all


.PHONY: install-dev install-prod install-ci
install-dev install-prod install-ci: openapi-specs ## install app in development/production or CI mode
	# installing in $(subst install-,,$@) mode
	@.venv/bin/pip3 install -r requirements/$(subst install-,,$@).txt


# RUNNING  ---------------

# lib environs for py-smash
export LD_LIBRARY_PATH=${BUILD_BIN_DIR}
export PYTHONPATH=${BUILD_BIN_DIR}
DEFAULT_PORT  ?= 8081

up-devel: ## starts server in development mode
	@.venv/bin/uvicorn simcore_service_tree_new_api.main:app --reload



# TESTING ---------------

PHONY: tests-unit tests-integration
tests-unit: ## runs unit tests
	# running unit tests
	@pytest -vv --exitfirst --failed-first --durations=10 --pdb $(CURDIR)/tests/unit


tests-integration: ## runs integration tests against local+production images
	# running integration tests local/(service):production images ...
	@export DOCKER_REGISTRY=local; \
	export DOCKER_IMAGE_TAG=production; \
	pytest -vv --exitfirst --failed-first --durations=10 --pdb $(CURDIR)/tests/integration



# VERSIONING -----------------

define _bumpversion
	# upgrades as $(subst version-,,$@) version, commits and tags
	@bump2version --verbose --list $(subst version-,,$@)
endef

version-patch: ## commits version with bug fixes not affecting the cookiecuter config
	$(_bumpversion)
version-minor: ## commits version with backwards-compatible API addition or changes (i.e. can replay)
	$(_bumpversion)
version-major: ## commits version with backwards-INcompatible addition or changes
	$(_bumpversion)


.PHONY: info
info: ## displays information
	# installed
	@pip list
	# version
	@cat VERSION


.PHONY: clean clean-all
git_clean_args = -dxf -e .vscode

clean: ## cleans all unversioned files in project and temp files create by this makefile
	# Cleaning unversioned
	@git clean -n $(git_clean_args)
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@echo -n "$(shell whoami), are you REALLY sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	@git clean $(git_clean_args)


#-----------------------------------
.PHONY: help
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
help: ## this colorful help
	@echo "Recipes for '$(notdir $(CURDIR))':"
	@echo ""
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
