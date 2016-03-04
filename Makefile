.PHONY: all
all: start

.PHONY: start
start:
	. ./tools/scripts/setup.sh

.PHONY: validate
validate: lint

.PHONY: lint
lint:
	echo "Linting via PEP8"
	pep8

.PHONY: pip
pip:
	pip install -r requirements.txt
