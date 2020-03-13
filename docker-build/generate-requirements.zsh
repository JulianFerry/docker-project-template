#!/bin/zsh

cp ../pyproject.toml .

echo "Exporting requirements-poetry.txt from pypoetry.toml"
poetry export -f requirements.txt --without-hashes > requirements-poetry.txt;
rm pyproject.toml poetry.lock
