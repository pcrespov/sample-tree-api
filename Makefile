
.venv:
	# creating environ
	@python3 -m venv .venv
	@.venv/bin/pip install -U pip setuptools wheel


install:
	# installing in edit mode
	@.venv/bin/pip install -e .


clean: .check-clean
	# remove environ
	-@rm -rf .venv
	# remove unversioned
	-@git clean -dfX

.check-clean:
	@git clean -ndfX
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
