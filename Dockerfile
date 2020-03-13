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

# Install python packages common to data science projects - cached with BuildKit
ENV PATH="/root/.poetry/bin:/opt/venv/bin:$PATH"
RUN poetry config virtualenvs.create false

# Add modified pyproject.toml 
COPY pyproject-v0.toml /opt/
RUN --mount=type=cache,target=/root/.cache/pypoetry \
  cd /opt && \
  mv pyproject-v0.toml pyproject.toml && \
  poetry install --no-root

# Create project directory and set as working directory
VOLUME /opt/project
WORKDIR /opt/project

# Run jupyter notebook
CMD jupyter notebook --ip='0.0.0.0' --port=8888 --allow-root --no-browser