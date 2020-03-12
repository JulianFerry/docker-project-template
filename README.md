# docker-project-template

Project template to build development images  containing jupyter notebook and data science tools

To build the image just run:
```
docker build -t myimage .
```

Optionally if you need to modify which packages are installed, edit the *-no-dev* and *-dev* requirements files in *.requirements/* and regenerate *pyproject.toml*, *poetry.lock* and *requirements-poetry.txt* with:
```
source .requirements/generate-requirements.zsh
```

TO DO: write script which rebuilds the image from a container once new packages have been installed with `poetry add`.
