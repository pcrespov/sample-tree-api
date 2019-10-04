.DEFAULT_GOAL := help

.venv:
	# creating virtual environ
	@python3 -m venv .venv
	@.venv/bin/pip --no-cache install -U pip setuptools wheel


.PHONY: devel
devel: .venv ## builds development environment
	# installing dependencies
	@.venv/bin/pip install -r requirements/_test.txt
	# installing in edit mode
	@.venv/bin/pip install -e .


.PHONY: clean
clean: .check-clean ## cleans unversioned and ignored files
	# remove unversioned
	-@git clean -dfX

.check-clean:
	@git clean -ndfX
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]


.PHONY: help
help: # this colorful help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)


demo:

