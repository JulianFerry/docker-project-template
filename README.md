# docker-project-template

Project template to build development images  containing jupyter notebook and data science tools

To build the image run `export DOCKER_BUILDKIT=1; cd docker-build; docker build -t myimage .`

To run the container call `source docker-run.zsh myimage`. This will run a jupyter notebook server at port 8888. The `docker-run.zsh` script uses the script directory name as the container name. If you do not specify myimage it will default to `jupyter-ds`.

Optionally if you need to modify which packages are installed, edit the `pyproject.toml` file and call and call `source docker-build/generate-requirements.zsh` to generate `docker-build/requirements-poetry.txt`

TO DO: write script which rebuilds the image from a container once new packages have been installed with `poetry add`.
