# docker-project-template

Project template to build development images containing jupyter notebook and data science tools

## Workflow

1. To build the base image run `export DOCKER_BUILDKIT=1; docker build -t jupyter-ds .`. This will create an image called `jupyter-ds` which contains 

2. To run the container call `source docker-run.zsh jupyter-ds`. This will run a jupyter notebook server at port 8888. The project directory will be mounted to the `/opt/project` folder in the container. The `docker-run.zsh` script uses the script directory name as the container name. The last argument is used as the image name, if nothing is specified it will default to `jupyter-ds`

3. Once the container has been launched, any new packages should be installed with `poetry add package_name`. This will install them to the virtual environment at `opt/venv`, as well as update the `pyproject.toml` and `poetry.lock` files. To persist your changes, commit the container to a new image with `docker commit mycontainer myimage`. E.g. you could use `docker commit project_name project_name:v0`.
