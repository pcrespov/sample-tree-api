#
#
#

.DEFAULT_GOAL := help
DEFAULT_PORT  ?= 8081

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
src/simcore_service_tree.egg-info: .venv
	# installing dependencies
	@.venv/bin/pip install -r requirements/_test.txt
	# installing in edit mode
	@.venv/bin/pip install -e .

up-devel: devenv ## starts server in development mode
	@.venv/bin/simcore-service-api --port=${DEFAULT_PORT}


.PHONY: tests
tests: devenv ## run unit tests
	@.venv/bin/pytest -vv -x --pdb tests/test_data_nodes.py

.PHONY: shell
shell: ## python shell
	@.venv/bin/python3


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

