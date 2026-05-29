PROJECT_REF=woyfmgshczlytjtojkvf

install:
	pip install -e ".[dev]"

dev:
	uvicorn app.main:app --reload --port 8000

lint:
	ruff check .

test:
	pytest

# --- DB Migrations (Supabase CLI) ---

db-link:
	npx supabase link --project-ref $(PROJECT_REF)

db-push:
	npx supabase db push

db-new:
	@read -p "Migration name: " name; \
	npx supabase migration new $$name

db-status:
	npx supabase migration list

db-reset:
	npx supabase db reset
