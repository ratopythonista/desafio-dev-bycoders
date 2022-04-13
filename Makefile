install:
	pip install pylama pytest pytest-cov requests black bandit
	pip install -e .

build:
	docker-compose build

start-api:
	docker-compose -f api-docker-compose.yml up -d
	docker logs -f cnab-parser

stop-api:
	docker-compose -f api-docker-compose.yml down

start-database:
	docker-compose -f database-docker-compose.yml up -d

stop-database:
	docker-compose -f database-docker-compose.yml down

run-unit-test:
	docker-compose -f unit-test-docker-compose.yml up

lint:
	pylama -m 120 .

format:
	black --line-length=120 .

security:
	bandit .