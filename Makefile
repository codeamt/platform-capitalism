# Platform Capitalism Simulation - Makefile
.PHONY: help install dev test build docker-build docker-run deploy-vercel deploy-lightsail deploy-terraform clean

# Variables
SERVICE = platform-capitalism
REGION = us-east-1
GITHUB_USER = YOUR_USERNAME
IMAGE = ghcr.io/$(GITHUB_USER)/$(SERVICE):latest
PORT = 5001

# Colors for output
BLUE = \033[0;34m
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m # No Color

##@ General

help: ## Display this help message
	@echo "$(BLUE)Platform Capitalism Simulation$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf "Usage:\n  make $(GREEN)<target>$(NC)\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2 } /^##@/ { printf "\n$(YELLOW)%s$(NC)\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development

install: ## Install dependencies with uv
	@echo "$(BLUE)Installing dependencies...$(NC)"
	uv sync

dev: ## Run development server
	@echo "$(BLUE)Starting development server on port $(PORT)...$(NC)"
	uv run python main.py

dev-uvicorn: ## Run with uvicorn (production-like)
	@echo "$(BLUE)Starting uvicorn server on port 8080...$(NC)"
	uvicorn main:app --reload --host 0.0.0.0 --port 8080

test: ## Run pytest test suite
	@echo "$(BLUE)Running pytest...$(NC)"
	uv run pytest tests/ -v

test-manual: ## Run manual validation script
	@echo "$(BLUE)Running manual validation...$(NC)"
	python tests/validate_simulation.py

test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	uv run pytest tests/ -v --cov=simulation --cov-report=term-missing

##@ Docker

docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image...$(NC)"
	docker build -t $(IMAGE) .

docker-run: ## Run Docker container locally
	@echo "$(BLUE)Running Docker container on port 8080...$(NC)"
	docker run -p 8080:8080 --rm $(IMAGE)

docker-push: ## Push Docker image to GitHub Container Registry
	@echo "$(BLUE)Pushing image to GHCR...$(NC)"
	docker push $(IMAGE)

##@ Deployment - Vercel (Demo)

deploy-vercel: ## Deploy to Vercel (demo)
	@echo "$(BLUE)Deploying to Vercel...$(NC)"
	vercel

deploy-vercel-prod: ## Deploy to Vercel production
	@echo "$(BLUE)Deploying to Vercel (production)...$(NC)"
	vercel --prod

##@ Deployment - AWS Lightsail (Research)

deploy-lightsail-build: ## Build and push to Lightsail
	@echo "$(BLUE)Building for Lightsail...$(NC)"
	cd deploy/lightsail && bash lightsail_build.sh

deploy-lightsail: ## Deploy to Lightsail manually
	@echo "$(BLUE)Deploying to Lightsail...$(NC)"
	cd deploy/lightsail && bash deploy_lightsail.sh

lightsail-logs: ## View Lightsail container logs
	@echo "$(BLUE)Fetching Lightsail logs...$(NC)"
	aws lightsail get-container-log \
		--service-name $(SERVICE) \
		--region $(REGION)

##@ Deployment - Terraform (Recommended for Research)

terraform-init: ## Initialize Terraform
	@echo "$(BLUE)Initializing Terraform...$(NC)"
	cd deploy/terraform && terraform init

terraform-plan: ## Plan Terraform deployment
	@echo "$(BLUE)Planning Terraform deployment...$(NC)"
	cd deploy/terraform && terraform plan

terraform-apply: ## Apply Terraform deployment
	@echo "$(BLUE)Applying Terraform deployment...$(NC)"
	cd deploy/terraform && terraform apply

terraform-destroy: ## Destroy Terraform infrastructure
	@echo "$(YELLOW)Destroying Terraform infrastructure...$(NC)"
	cd deploy/terraform && terraform destroy

terraform-output: ## Show Terraform outputs
	@cd deploy/terraform && terraform output

##@ Utilities

clean: ## Clean up temporary files
	@echo "$(BLUE)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .ruff_cache

format: ## Format code with ruff
	@echo "$(BLUE)Formatting code...$(NC)"
	ruff format .

lint: ## Lint code with ruff
	@echo "$(BLUE)Linting code...$(NC)"
	ruff check .

health-check: ## Check if deployed service is healthy
	@echo "$(BLUE)Checking service health...$(NC)"
	@curl -f http://localhost:8080/health || echo "$(YELLOW)Service not running locally$(NC)"

##@ Quick Deploy Commands

quick-demo: docker-build docker-run ## Build and run Docker locally for quick demo

quick-vercel: deploy-vercel ## Quick deploy to Vercel

quick-research: terraform-init terraform-apply ## Quick deploy to AWS Lightsail via Terraform

##@ Documentation

docs: ## Open deployment documentation
	@echo "$(BLUE)Opening deployment guide...$(NC)"
	@open deploy/DEPLOYMENT_GUIDE.md || cat deploy/DEPLOYMENT_GUIDE.md

docs-serve: ## Serve MkDocs documentation locally
	@echo "$(BLUE)Starting MkDocs server...$(NC)"
	uv run mkdocs serve

docs-build: ## Build MkDocs documentation
	@echo "$(BLUE)Building MkDocs site...$(NC)"
	uv run mkdocs build

docs-deploy: ## Deploy documentation to GitHub Pages
	@echo "$(BLUE)Deploying docs to GitHub Pages...$(NC)"
	uv run mkdocs gh-deploy --force

##@ Default

.DEFAULT_GOAL := help
