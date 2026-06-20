# HiTechJobs.CA — local dev + CI helpers.
#
# Quick start:
#   make run          # db + api + web via docker compose (foreground)
#   make up           # same, detached
#   make test         # run all available test suites
#   make precommit    # run pre-commit hooks across all files
#
# Per-app dev (no Docker):
#   make dev-web      # Vite dev server on :5173
#   make test-sync    # uv run pytest (apps/sync; no DB needed)
#   make test-api     # ./mvnw test (apps/api)

.PHONY: help
help: ## Show this help
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# ---------- Docker (full stack) ----------
.PHONY: run up down restart logs build ps
run: ## Start db + api + web (foreground, build first)
	docker compose up --build

up: ## Start db + api + web detached (build first)
	docker compose up -d --build

down: ## Stop and remove containers
	docker compose down

restart: ## Restart all services
	docker compose restart

logs: ## Tail logs for all services
	docker compose logs -f

build: ## Build all service images
	docker compose build

ps: ## List running services
	docker compose ps

# ---------- apps/sync (ingest) ----------
.PHONY: sync sync-dry
sync: ## Run the jobs ingest once (needs the db service up)
	docker compose --profile sync run --rm sync

sync-dry: ## Ingest dry-run (fetch + parse, no DB write)
	docker compose --profile sync run --rm -e SYNC_DRY_RUN=1 sync

# ---------- Tests ----------
.PHONY: test test-sync test-api build-web
test: test-sync test-api build-web ## Run all available test suites

test-sync: ## apps/sync: uv run pytest (no DB needed)
	cd apps/sync && uv sync --extra dev --frozen && uv run pytest -v

test-api: ## apps/api: ./mvnw test (JDK 21 required locally)
	cd apps/api && ./mvnw -B -ntp test

build-web: ## apps/web: npm run build (Vite production bundle)
	cd apps/web && npm ci && npm run build

# ---------- Per-app dev (no Docker) ----------
.PHONY: dev-web dev-api
dev-web: ## apps/web: Vite dev server (http://localhost:5173)
	cd apps/web && npm install && npm run dev

dev-api: ## apps/api: run Spring Boot locally (needs Postgres + env vars)
	cd apps/api && ./mvnw -B -ntp spring-boot:run

# ---------- Hygiene ----------
.PHONY: precommit install-hooks
precommit: ## Run pre-commit hooks across all files
	pre-commit run --all-files

install-hooks: ## Install pre-commit git hooks
	pre-commit install

# ---------- Cleanup ----------
.PHONY: clean
clean: ## Stop containers, remove volumes + build artifacts
	docker compose down -v --remove-orphans
	rm -rf apps/web/dist apps/web/node_modules
	rm -rf apps/api/target
