FROM python:3.8-slim-buster

LABEL MAINTAINER="Julian Ferry <julianferry94@gmail.com>"

# Combine `apt-get update` with `apt-get install` so that modifications to this command get recognised by docker... 
# ... so that the `apt-get update` cache is invalidated and the most recent packages are installed
RUN apt-get update && apt-get install -y curl

# Install poetry
# Warning: build caching means updates to the script will not be caught by docker
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - -y
ENV PATH="/root/.poetry/bin:/opt/venv/bin:$PATH"

# Install python packages common to data science projects
COPY .requirements/requirements-poetry.txt opt/
RUN /bin/bash -c "python -m venv /opt/venv && \
  source /opt/venv/bin/activate && \
  pip install -U pip && \
  pip install -r opt/requirements-poetry.txt"

# Create project directory and set as working directory
VOLUME /opt/project
WORKDIR /opt/project

# Run jupyter notebook
CMD jupyter notebook --ip='0.0.0.0' --port=8888 --allow-root --no-browser
