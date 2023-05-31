SERVICE = redis

start:
	@docker compose up -d --remove-orphans

stop:
	@docker compose down

restart: stop start

shell:
	@docker compose exec $(SERVICE) bash

cli:
	@docker compose exec $(SERVICE) redis-cli

