all: build migrate test run

build:
	docker-compose -f docker-compose-dev.yml build

run:
	docker-compose -f docker-compose-dev.yml up

stop:
	docker-compose -f docker-compose-dev.yml stop

shell:
	docker-compose -f docker-compose-dev.yml run --rm web_api bash

migrate:
	docker-compose -f docker-compose-dev.yml run --rm web_api python manage.py migrate

test:
	docker-compose -f docker-compose-dev.yml run --rm web_api python manage.py test
