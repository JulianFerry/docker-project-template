# Default
.PHONY: default
default: notebook

# Build requirements
.PHONY: build
build: .venv
.venv:
	@poetry install --extras eda --extras db

# Jupyter notebook
.PHONY: notebook
notebook: build
	@poetry run jupyter notebook --notebook-dir="notebooks"

# Run tests
.PHONY: tests
tests: build
	@poetry run pytest tests

# Remove artifacts
.PHONY: clean
clean:
	@rm -rf .pytest_cache
	@rm -rf .venv
	@rm -rf pickle/preprocessor.pkl
	@rm -rf preprocess.egg-info