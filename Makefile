PROJECT=powerslack
PYTHON=python
PIP=pip

all: help

help:
	@echo "build - build the project"
	@echo "clean - clean the project"
	@echo "help - show this help"
	@echo "install - install the project"
	@echo "run - run the project"
	@echo "test - run the tests"
	@echo "version - show the version"
	@echo "lint - run the linter"
	@echo "format - black the repo"

venv: venv/touchfile

venv/touchfile:
	test -d venv || python3.10 -m venv venv
	. venv/bin/activate;
	touch venv/touchfile


clean: clean-pyc clean-build
	rm -rf venv

clean-build:
	rm -rf build/ dist/ .eggs/ *.egg-info/

clean-pyc:
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	-find . -type d -name "__pycache__" | xargs rm -r

test: venv
	. venv/bin/activate;

pip-compile-dev: venv
	pip-compile dev-requirements.in

pip-compile: venv
	pip-compile

install: pip-compile-dev pip-compile
	pip-sync

install-dev: pip-compile-dev
	pip-sync dev-requirements.txt

run: install
	python -m app
