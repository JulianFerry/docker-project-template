# ds-project-template

Project template for data science projects.

Requirements:
- python ^3.7
- poetry ^1.0.5 - install with `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`
- docker ^18.06 (optional) to deploy build images (uses BuildKit)


## Workflow

1. Modify the project name in `pyproject.toml` and run `poetry install --no-root --extras eda` to install the dependencies. This installs:
- pandas, scikit-learn, flask and joblib as dependencies
- jupyter and seaborn as extra dependencies
- flake8, pytest and pytest-cov as dev dependencies

2. New packages can be installed with `poetry add package_name`. This will install the new packages to the `.venv` virtual environment and automatically update the `pyproject.toml` and `poetry.lock` files to capture the project dependencies.

3. Run `source docker/app/docker-build.zsh` to build an image which installs the dependencies listed in `pyproject.toml` (it does not install extra and dev packages) and packages the code in the `app/` folder. By default the image will run `main.py` as its entrypoint. Update `docker/app/Dockerfile` according to your deployment needs.
