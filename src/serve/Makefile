# Default
.PHONY: default
default: local

# Build requirements
.PHONY: build
build: .venv
.venv:
	@poetry install

# Run local server
.PHONY: local
local: export preprocessor_path = '../preprocess/pickle/preprocessor.pkl'
local: export model_path = '../train/pickle/model.pkl'
local: build
	@poetry run python -m serve

# GET local server
.PHONY: get
get:
	curl localhost:8080

# POST local server
.PHONY: post
post:
	curl -X POST -F data=@../../data/raw/test.csv http://127.0.0.1:8080/

# Run tests
.PHONY: tests
tests: build
	@poetry run pytest tests

# Remove artifacts
.PHONY: clean
clean:
	@rm -rf .pytest_cache
	@rm -rf .venv
	@rm -rf serve.egg-info