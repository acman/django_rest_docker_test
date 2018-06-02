build:
	docker-compose -f docker-compose-dev.yml build

run:
	docker-compose -f docker-compose-dev.yml up

stop:
	docker-compose -f docker-compose-dev.yml stop
