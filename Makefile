BACKEND_ROOT := $(shell pwd)

SRC_DIR := $(BACKEND_ROOT)/src

run:
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py runserver

migrate:
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py makemigrations
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py migrate

commit:
	git add .
	git commit -m "updated $(shell date +%Y-%m-%d)"
	git push origin master

app:
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py startapp $(name)

test:
	PYTHONPATH=$(SRC_DIR): uv run pytest

admin:
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py createsuperuser

env:
	@echo source .venv/bin/activate
	