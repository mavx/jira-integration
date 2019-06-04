#!/bin/bash

# Define status check for each test
exit_if_error() {
    local exit_code=$?
    if (( $exit_code )); then
        printf '\e[91mCheck failed!'
        exit 1
    fi
}

echo "PyTest - Running tests"
pipenv run python -m pytest;
exit_if_error

echo "MyPy - Checking type hints"
pipenv run mypy --ignore-missing-imports .
exit_if_error

#echo "Flake8 - Checking for PEP8 compliance"
#flake8 --max-line-length=88 .
#exit_if_error

echo "Running pre-commit jobs"
pipenv run pre-commit run --all
