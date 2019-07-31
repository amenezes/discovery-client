.DEFAULT_GOAL := about

flake:
	@echo "--- code style checking ---"
	flake8 discovery
	flake8 tests

tests:
	@echo "--- unittest ---"
	python -m pytest -v --cov-report xml --cov-report term --cov=discovery tests

doc: 
	@echo "> generate project documentation..."

install-deps:
	@echo "> installing development dependencies..."
	pip install -r requirements-dev.txt

develop: install-deps
	@echo "> preparing local development environment"
	pip install virtualenv	
	virtualenv venv
	source venv/bin/activate

about:
	@echo "> `cat setup.py| grep name= | cut -d'"' -f2` [`cat setup.py| grep version= | cut -d'"' -f2`]"
	@echo ""
	@echo "project page: `cat setup.py | grep url= | cut -d'"' -f2`"
	@echo "pypi: https://pypi.org/project/discovery-client/"
	@echo "license: `cat setup.py| grep License | awk '{print tolower($$6), tolower($$7), tolower($$8)}' | cut -d '"' -f1`"

ci: all
	@echo "--- download CI dependencies ---"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "--- report upload ---"
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID

all: flake tests doc

.PHONY: flake tests doc develop about all
