#!/bin/sh

# Add the web_backend to the PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PWD/web_backend

# Remove the previous .coverage file
coverage erase
# Generate the .coverage file with the tests coverage
# All the Python packages under the web_backend folder whose test coverage want to be known must be added to the --source option, separated by commas
coverage run --branch --source=web_backend,web_backend/apis,web_backend/wrapper tests/run_all_tests.py
# Generate the coverage.xml file using the .coverage file
coverage xml -i
