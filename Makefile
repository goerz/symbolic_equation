.PHONY: help clean clean-build clean-pyc clean-test clean-venvs lint test flake8-check pylint-check black-check black isort-check isort coverage test-upload upload pre-commit-hooks  release dist dist-check install uninstall develop
.DEFAULT_GOAL := help
TESTENV = MATPLOTLIBRC=tests
TESTOPTIONS = --doctest-modules --cov=symbolic_equation
TESTS = src tests

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-z0-9A-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:  ## show this help
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-venvs ## remove all build, test, coverage, and Python artifacts, as well as environments
	@echo "Done cleaning"

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	rm -fr src/*.egg-info
	rm -fr pip-wheel-metadata/
	find tests src -name '*.egg-info' -exec rm -fr {} +
	find tests src -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find tests src -name '*.pyc' -exec rm -f {} +
	find tests src -name '*.pyo' -exec rm -f {} +
	find tests src -name '*~' -exec rm -f {} +
	find tests src -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/

clean-venvs: ## remove testing/build environments
	rm -fr .tox
	rm -fr .venv

flake8-check: ## check style with flake8
	tox -e run-flake8

pylint-check: ## check style with pylint
	tox -e run-pylint

test: test36 test37 ## run tests on every supported Python version

test36: ## run tests for Python 3.6
	tox -e py36-test

test37: ## run tests for Python 3.7
	tox -e py37-test

pre-commit-hooks: ## install pre-commit hooks
	tox -e run-cmd -- pre-commit install

black-check: ## Check all src and test files for complience to "black" code style
	tox -e run-blackcheck

black: ## Apply 'black' code style to all src and test files
	tox -e run-black

isort-check: ## Check all src and test files for correctly sorted imports
	tox -e run-isortcheck

isort: ## Sort imports in all src and test files
	tox -e run-isort

coverage: test37  ## generate coverage report in ./htmlcov
	tox -e coverage
	@echo "open htmlcov/index.html"

test-upload: clean-build clean-pyc dist ## package and upload a release to test.pypi.org
	tox -e run-cmd -- twine check dist/*
	tox -e run-cmd -- twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload: clean-build clean-pyc dist ## package and upload a release to pypi.org
	tox -e run-cmd -- twine check dist/*
	tox -e run-cmd -- twine upload dist/*

release: ## Create a new version, package and upload it
	python3.7 -m venv .venv/release
	.venv/release/bin/python -m pip install click gitpython pytest
	.venv/release/bin/python ./scripts/release.py

dist: ## builds source and wheel package
	tox -e run-cmd -- python setup.py sdist
	tox -e run-cmd -- python setup.py bdist_wheel
	ls -l dist

dist-check: ## Check all dist files for correctness
	tox -e run-cmd -- twine check dist/*

install: clean-build clean-pyc ## install the package to the active Python's site-packages
	pip install .

uninstall:  ## uninstall the package from the active Python's site-packages
	pip uninstall symbolic_equation

develop: clean-build clean-pyc ## install the package to the active Python's site-packages, in develop mode
	PIP_USE_PEP517=false pip install -e .[dev]

develop-test: develop ## run tests within the active Python environment
	$(TESTENV) py.test -v $(TESTOPTIONS) $(TESTS)


jupyter-notebook: ## run a notebook server for editing the examples
	tox -e run-cmd -- jupyter notebook --config=/dev/null

jupyter-lab: ## run a jupyterlab server for editing the examples
	tox -e run-cmd -- pip install jupyterlab
	tox -e run-cmd -- jupyter lab --config=/dev/null
