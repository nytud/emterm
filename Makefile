# Bash is needed for time
SHELL := /bin/bash -o pipefail
DIR := ${CURDIR}
red := $(shell tput setaf 1)
green := $(shell tput setaf 2)
sgr0 := $(shell tput sgr0)
all:
	@echo "See Makefile for possible targets!"

dist/*.whl dist/*.tar.gz:
	@echo "Building package..."
	python3 setup.py sdist bdist_wheel

build: dist/*.whl dist/*.tar.gz

install-user: build
	@echo "Installing package to user..."
	pip3 install dist/*.whl

test:
	@echo "Running tests..."
	time (cd /tmp && python3 -m emterm --term-list ${DIR}/test_termlist.tsv -i $(DIR)/tests/test_input.xtsv | \
	 diff - $(DIR)/tests/test_output.xtsv 2>&1 | head -n100)

install-user-test: install-user test
	@echo "$(green)The test was completed successfully!$(sgr0)"

ci-test: install-user-test

uninstall:
	@echo "Uninstalling..."
	pip3 uninstall -y emterm

install-user-test-uninstall: install-user-test uninstall

clean:
	rm -rf dist/ build/ emterm.egg-info/

clean-build: clean build
