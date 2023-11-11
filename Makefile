.DEFAULT_GOAL := about
VERSION := $(shell cat discovery/__init__.py | grep version | cut -d'"' -f2)

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort discovery --profile black
	isort tests --profile black
	@echo "> running black..."
	black discovery
	black tests
endif
	@echo "> running flake8..."
	flake8 discovery
	flake8 tests
	@echo "> running mypy..."
	mypy discovery

tests:
	@echo "> running tests"
	python -m pytest -vv --no-cov-on-fail --color=yes --cov-report xml --cov-report term --cov=discovery tests

ci: lint tests
ifeq ($(GITHUB_HEAD_REF), false)
	@echo "--- codecov report ---"
	codecov --file coverage.xml -t $$CODECOV_TOKEN
endif

docs: 
	@echo "> generate project documentation..."
	@cp README.md docs/index.md
	mkdocs serve -a 0.0.0.0:8000

tox:
	@echo "> running tox..."
	tox -r -p all

install-deps:
	@echo "> installing dependencies..."
	pip install -r requirements-dev.txt
	pre-commit install

about:
	@echo "> discovery-client $(VERSION)"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Execute tests"
	@echo "make ci           - Runs: [make lint > make tests]"
	@echo "make tox          - Runs tox"
	@echo "make docs         - Generate project documentation"
	@echo "make install-deps - Install development dependencies."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

all: ci tox

.PHONY: lint tests ci tox docs all
