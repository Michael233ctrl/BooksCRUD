DOCKER_COMPOSE_LEGACY := $(shell docker-compose --version 2> /dev/null)
DOCKER_COMPOSE := $(shell docker compose version && echo "new client detected" 2> /dev/null)

ifdef DOCKER_COMPOSE_LEGACY
DOCKER_COMPOSE_PATH := docker-compose
else
ifdef DOCKER_COMPOSE
DOCKER_COMPOSE_PATH := docker compose
else
$(error "no docker-compose executable found")
endif
endif


restart: down up

up:
	$(DOCKER_COMPOSE_PATH) up -d

down:
	$(DOCKER_COMPOSE_PATH) down

build:
	$(DOCKER_COMPOSE_PATH) build

test:
	$(DOCKER_COMPOSE_PATH) run web pytest

migrate:
	$(DOCKER_COMPOSE_PATH) exec web alembic upgrade head

migrations:
	$(DOCKER_COMPOSE_PATH) exec web alembic revision
