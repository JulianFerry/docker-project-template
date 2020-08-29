# Build requirements
.PHONY: build
build: .venv
.venv:
	@poetry install

# Create local mysql database
.PHONY: db
db:
	@zsh ./make/db.zsh

# Remove database
.PHONY: db-rm
db-rm:
	@docker stop mysql
	@docker rm mysql

# Run tests
.PHONY: tests
tests: build db
	@poetry run pytest tests

# Remove artifacts and database files
.PHONY: clean
clean:
	@sudo rm -rf db
	@rm -rf .pytest_cache
	@rm -rf .venv
	@rm -rf database.egg-info