#!/bin/bash

# first remove old packages
poetry remove abner

# Clean up build artifacts and cache
rm -rf .venv/
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/

# install the dependencies
poetry install

# build with pyarmor
poetry run pyarmor gen abner/cli.py -O dist/abner --recursive

# now that we have the new package, install it
poetry install
