.DEFAULT_GOAL := about
VERSION := $(shell cat discovery/__version__.py | cut -d'"' -f2)
DTYPE=server

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort discovery
	isort tests
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
	python -m pytest -v --cov-report xml --cov-report term --cov=discovery tests

docs: 
	@echo "> generate project documentation..."
	portray $(DTYPE)

install-deps:
	@echo "> installing development dependencies..."
	pip install -r requirements-dev.txt

tox:
	@echo "> running tox..."
	tox -r -p all

about:
	@echo "> discovery-client $(VERSION)"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Execute tests"
	@echo "make tox          - Runs tox"
	@echo "make docs         - Generate project documentation [DTYPE=server]"
	@echo "make ci           - Runs: [make lint > make tests]"
	@echo "make install-deps - Install development dependencies"
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

ci: lint tests
ifeq ($(GITHUB_HEAD_REF), false)
	@echo "--- codecov report ---"
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	@echo "--- codeclimate report ---"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: install-deps ci docs

.PHONY: lint tests docs about ci all
