install:
	pip install -e ".[dev]"

dev:
	uvicorn app.main:app --reload --port 8000

lint:
	ruff check .

test:
	pytest
