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
	@echo "--- codeclimate report ---"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

docs: 
	@echo "> generate project documentation..."
	@cp README.md docs/index.md
	mkdocs serve

tox:
	@echo "> running tox..."
	tox -r -p all

about:
	@echo "> discovery-client $(VERSION)"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Execute tests"
	@echo "make ci           - Runs: [make lint > make tests]"
	@echo "make tox          - Runs tox"
	@echo "make docs         - Generate project documentation"
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

all: ci tox

.PHONY: lint tests ci tox docs all
