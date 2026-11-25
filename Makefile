.PHONY: help up down build logs frontend backend install lint test clean sandbox

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

up: ## Start all services (docker compose)
	docker compose up --build

down: ## Stop all services
	docker compose down

build: ## Build all Docker images
	docker compose build
	docker compose --profile build-only build sandbox

logs: ## Tail compose logs
	docker compose logs -f

frontend: ## Run Next.js locally (npm)
	cd frontend && npm run dev

backend: ## Run FastAPI locally (uvicorn)
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

install: ## Install frontend + backend deps locally
	cd frontend && npm install
	cd backend && pip install -r requirements.txt -r requirements-dev.txt

lint: ## Lint frontend and backend
	cd frontend && npm run lint
	cd backend && ruff check app tests && black --check app tests

test: ## Run backend unit tests
	cd backend && pytest -q

sandbox: ## Build the code-execution sandbox image
	docker build -t codecraft-sandbox:latest ./sandbox

clean: ## Remove containers, volumes, and caches
	docker compose down -v --remove-orphans
	rm -rf frontend/.next frontend/node_modules backend/.pytest_cache backend/__pycache__
