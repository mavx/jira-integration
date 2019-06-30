#!/bin/bash

# Run this to manually publish to PyPI
export PYPI_INDEX=http://pypi.xvam.org/
export PYPI_REPO=moneylion
export PYPI_USER=$PYPI_REPO
export PYPI_PASSWORD=$PYPI_REPO

poetry config repositories.$PYPI_REPO $PYPI_INDEX
poetry config http-basic.$PYPI_REPO $PYPI_USER $PYPI_PASSWORD
poetry publish -r $PYPI_REPO --build
