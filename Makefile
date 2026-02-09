.PHONY: help install dev test test-cov lint format build run clean docker-build docker-run k8s-dev k8s-staging

## Variable definitions
PYTHON := python3
PIP := pip3
DOCKER_IMAGE := task-api:v1
DOCKER_REGISTRY := docker.io
KUSTOMIZE_DEV := k8s/overlays/dev
KUSTOMIZE_STAGING := k8s/overlays/staging

help: ## Show this help message
	@echo "Task API - Make Commands\n"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

## Development Commands

install: ## Install dependencies
	$(PIP) install -r app/requirements.txt
	$(PIP) install -r app/requirements-dev.txt

dev: ## Run development server with auto-reload
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

install-pre-commit: ## Install pre-commit hooks
	pre-commit install

## Testing Commands

test: ## Run all tests
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ --cov=app --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

test-watch: ## Run tests in watch mode
	pytest-watch tests/

## Code Quality

lint: ## Run linters (pylint, flake8)
	pylint app/main.py || true
	flake8 app/ tests/ || true
	mypy app/ || true

format: ## Format code with Black and isort
	black app/ tests/
	isort app/ tests/

format-check: ## Check formatting without applying changes
	black --check app/ tests/
	isort --check-only app/ tests/

## Docker Commands

docker-build: ## Build Docker image
	docker build -t $(DOCKER_IMAGE) ./app

docker-run: docker-build ## Build and run Docker container
	docker run -p 8000:8000 $(DOCKER_IMAGE)

docker-clean: ## Remove Docker image
	docker rmi $(DOCKER_IMAGE) || true

docker-inspect: ## Inspect Docker image size and layers
	docker inspect $(DOCKER_IMAGE)
	docker history $(DOCKER_IMAGE)

## Kubernetes Commands

k8s-validate: ## Validate Kubernetes manifests
	kubectl apply -k $(KUSTOMIZE_DEV) --dry-run=client
	kubectl apply -k $(KUSTOMIZE_STAGING) --dry-run=client

k8s-preview: ## Preview Kustomize build output
	@echo "=== Dev Environment ===" && kustomize build $(KUSTOMIZE_DEV)
	@echo "\n=== Staging Environment ===" && kustomize build $(KUSTOMIZE_STAGING)

k8s-apply-dev: ## Apply dev environment to cluster
	kubectl apply -k $(KUSTOMIZE_DEV)

k8s-apply-staging: ## Apply staging environment to cluster
	kubectl apply -k $(KUSTOMIZE_STAGING)

k8s-delete-dev: ## Delete dev environment from cluster
	kubectl delete -k $(KUSTOMIZE_DEV)

k8s-delete-staging: ## Delete staging environment from cluster
	kubectl delete -k $(KUSTOMIZE_STAGING)

k8s-logs: ## Stream logs from task-api pods
	kubectl logs -f deployment/task-api-deployment --all-containers=true

k8s-status: ## Show deployment status
	kubectl get deployments task-api-deployment
	kubectl get pods -l app=task-api
	kubectl describe deployment task-api-deployment

## Cleanup

clean: ## Clean up build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .coverage htmlcov/ .tox/ build/ dist/ *.egg-info/
	docker-clean

deep-clean: clean ## Remove virtual environments
	rm -rf venv/ env/ .venv

## CI/CD Commands

ci: lint test ## Run CI pipeline locally (lint + test)

ci-docker: ci docker-build ## Run CI with Docker build

## Quick Start

setup: install install-pre-commit ## Complete setup for development
	@echo "✓ Development environment ready!"
	@echo "  Run: make dev"

all: clean install lint test docker-build ## Run complete pipeline

## Info Commands

info: ## Show project information
	@echo "Task API Project Information"
	@echo "============================="
	@echo "Python version: $$($(PYTHON) --version)"
	@echo "Pip version: $$($(PIP) --version)"
	@echo "Docker version: $$(docker --version)"
	@echo "kubectl version: $$(kubectl version --client --short || echo 'not installed')"
	@echo "kustomize version: $$(kustomize version || echo 'not installed')"

.SILENT: help
