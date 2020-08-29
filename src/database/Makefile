



.PHONY: build
build: .venv
.venv:
	@poetry install


.PHONY: tests
tests: build
	@poetry run pytest


.PHONY: db
db:
	@zsh ./make/db.zsh


.PHONY: db-rm
db-rm:
	@docker stop mysql
	@docker rm mysql


clean:
	@rm -rf .pytest_cache
	@sudo rm -rf db
