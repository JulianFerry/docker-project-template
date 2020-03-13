# syntax=docker/dockerfile:experimental
FROM python:3.8-slim-buster

LABEL MAINTAINER="Julian Ferry <julianferry94@gmail.com>"

# Install poetry - apt-get curl is cached by BuildKit (overkill but fun)
# This will not invalidated cache until the command is changed
RUN rm -f /etc/apt/apt.conf.d/docker-clean; \
    echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' \
      > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    apt update && \
    apt-get --no-install-recommends install -y curl && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - -y

# Force poetry to install to /opt/venv virtualenv
RUN python -m venv /opt/venv
ENV PATH="/root/.poetry/bin:/opt/venv/bin:$PATH"
RUN poetry config virtualenvs.create false

# Install python packages - cached with BuildKit
COPY pyproject.toml poetry.lock /opt/build/
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    cd /opt/build && \
    poetry install -vv --no-root --extras eda

# Create project directory and set as working directory
VOLUME /opt/project
WORKDIR /opt/project

# Run jupyter notebook
CMD jupyter notebook --ip='0.0.0.0' --port=8888 --allow-root --no-browser
