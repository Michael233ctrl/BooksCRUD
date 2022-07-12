restart: down up

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

test:
	docker-compose run web pytest

migrate:
	docker-compose exec web alembic upgrade head

migrations:
	docker-compose exec web alembic revision
