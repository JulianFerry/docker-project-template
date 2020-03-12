FROM python:3.7-slim-buster

LABEL MAINTAINER="Julian Ferry <julianferry94@gmail.com>"

# Combine `apt-get update` with `apt-get install` so that modifications to this command get recognised by docker... 
# ... so that the `apt-get update` cache is invalidated and the most recent packages are installed
RUN apt-get update && apt-get install -y curl

# Install poetry
# Warning: build caching means updates to the script will not be caught by docker
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - -y
ENV PATH="/root/.poetry/bin:/project/.venv/bin:$PATH"

# Create project directory and set as working directory
RUN mkdir project
WORKDIR /project

# Add python packages common to most data science projects with poetry
RUN poetry config virtualenvs.in-project true
COPY pyproject.toml .
RUN poetry add pytest flake8 pytest-cov --dev
COPY requirements.txt .
RUN poetry add `cat requirements.txt`

# Copy the project
COPY . .

# Run jupyter notebook
CMD jupyter notebook --ip='0.0.0.0' --port=8888 --allow-root --no-browser
