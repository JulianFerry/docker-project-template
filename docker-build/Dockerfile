# syntax=docker/dockerfile:experimental
FROM python:3.8-slim-buster

LABEL MAINTAINER="Julian Ferry <julianferry94@gmail.com>"

# The `apt update` cache will be invalidated when packages are added to `apt-get install`
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
  apt update && apt-get --no-install-recommends install -y curl

# Install poetry
# Warning: build caching means updates to the script will not be caught by docker
RUN --mount=type=cache,target=/root/.poetry/ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - -y
ENV PATH="/root/.poetry/bin:/opt/venv/bin:$PATH"

# Install python packages common to data science projects - cached with BuildKit
COPY requirements-poetry.txt opt/
RUN --mount=type=cache,target=/root/.cache/pip bin/bash -c \
  "python -m venv /opt/venv && \
  source /opt/venv/bin/activate && \
  pip install -U pip && \
  pip install -r opt/requirements-poetry.txt"

# Create project directory and set as working directory
VOLUME /opt/project
WORKDIR /opt/project

# Run jupyter notebook
CMD jupyter notebook --ip='0.0.0.0' --port=8888 --allow-root --no-browser
