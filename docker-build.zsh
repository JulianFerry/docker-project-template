#!/bin/zsh

# Reset pyproject.toml version
sed 's/version = .*/version = "0.1.0"/' pyproject.toml > pyproject-v0.toml

# Build image
docker build -t ${1:-jupyter-ds} .
