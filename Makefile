COMPOSE = docker compose -f infra/docker-compose.yml --project-directory .

.PHONY: help install up down destroy restart ps logs test

help:
	@echo "make install  - create venv and install pinned Python dependencies"
	@echo "make up       - start all infrastructure (Postgres x2, Airflow, MinIO)"
	@echo "make down     - stop infrastructure, keep data volumes"
	@echo "make destroy  - stop infrastructure and wipe all data volumes"
	@echo "make restart  - down + up"
	@echo "make ps       - show status/health of every service"
	@echo "make logs     - follow logs from all services"
	@echo "make test     - run the pytest suite"

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

destroy:
	$(COMPOSE) down -v

restart: down up

ps:
	$(COMPOSE) ps

logs:
	$(COMPOSE) logs -f

test:
	.venv/bin/pytest
