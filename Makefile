build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f
lint:
	uv run ruff check .

format:
	uv run ruff format .