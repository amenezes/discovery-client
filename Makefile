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
	pip install -r requirements-dev.txt

develop: install-deps
	pip install virtualenv	
	virtualenv venv
	source venv/bin/activate

about:
	@echo "> discovery-client"
	@echo ""
	@echo "version: 0.2.0"
	@echo "project page: https://github.com/amenezes/discovery-client"
	@echo "pypi: https://pypi.org/project/discovery-client/"

ci: all
	@echo "--- download CI dependencies ---"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "--- report upload ---"
	codecov --file coverage.xml -t $CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $CC_TEST_REPORTER_ID

all: flake tests doc

.PHONY: flake tests doc develop about all
