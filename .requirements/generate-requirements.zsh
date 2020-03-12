#!/bin/zsh

cp ./toml/pyproject.toml .

echo "Installing requirements and adding to pyproject.ml"
poetry add `cat requirements-no-dev.txt`;
poetry add --dev `cat requirements-dev.txt`;

echo "Exporting requirements-poetry.txt and pyproject.toml"
poetry export -f requirements.txt --without-hashes > requirements-poetry.txt;
mv pyproject.toml poetry.lock ../;

