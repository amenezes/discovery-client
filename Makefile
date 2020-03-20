.DEFAULT_GOAL := about
DTYPE=server

lint:
	@echo "> running isort..."
	isort -rc discovery
	isort -rc tests
	@echo "> running black..."
	black discovery
	black tests
	@echo "> running flake8..."
	flake8 discovery
	flake8 tests
	@echo "> running mypy..."
	mypy discovery

tests:
	@echo "--- unittest ---"
	python -m pytest -v --cov-report xml --cov-report term --cov=discovery tests

docs: 
	@echo "> generate project documentation..."
	portray $(DTYPE)

install-deps:
	@echo "> installing development dependencies..."
	pip install -r requirements-dev.txt

about:
	@echo "> discovery-client"
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
ifeq ($(CI), true)
	@echo "--- download CI dependencies ---"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "--- report upload ---"
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: install-deps ci docs

.PHONY: lint tests docs about ci all
