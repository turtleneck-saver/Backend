# Makefile 예시 (backend/ 디렉토리에 있다고 가정)

BACKEND_ROOT := $(shell pwd)

SRC_DIR := $(BACKEND_ROOT)/src

runserver:
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py runserver


makemigrations:
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py makemigrations


migrate:
	PYTHONPATH=$(SRC_DIR): uv run python $(SRC_DIR)/manage.py migrate

commit:
	git add .
	git commit -m "updated $(shell date +%Y-%m-%d)"
	git push origin main

