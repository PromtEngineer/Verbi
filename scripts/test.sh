#!/bin/bash
# Script to run tests with Poetry

# Run tests with the desired options
if [ "$1" == "coverage" ]; then
    poetry run pytest --cov=. --cov-branch --cov-report=term-missing:skip-covered --cov-report=html:htmlcov --cov-report=xml:coverage.xml --cov-fail-under=80 "${@:2}"
else
    poetry run pytest "$@"
fi