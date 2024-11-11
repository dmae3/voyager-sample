.PHONY: build create-index search

build:
	docker compose -f docker/docker-compose.yml build

create-index:
	docker compose -f docker/docker-compose.yml run --rm vector-search python -m app.cli create-index

search:
	docker compose -f docker/docker-compose.yml run --rm vector-search python -m app.cli search
