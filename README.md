# Task API - GitOps Ready Application

A production-ready FastAPI microservice for task management, containerized with Docker and deployed via Kubernetes with GitOps principles. This project demonstrates modern DevOps practices including CI/CD, IaC, and multi-environment deployments.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Local Development](#local-development)
- [Testing](#testing)
- [Docker](#docker)
- [Kubernetes Deployment](#kubernetes-deployment)
- [GitOps with Kustomize](#gitops-with-kustomize)
- [CI/CD Pipeline](#cicd-pipeline)
- [Contributing](#contributing)

## 🎯 Overview

Task API is a RESTful microservice built with FastAPI for managing tasks. It's designed to be:
- **Cloud-native**: Containerized and Kubernetes-ready
- **GitOps-friendly**: Infrastructure as code using Kustomize
- **Production-ready**: Includes health checks, logging, and error handling
- **Scalable**: Configured for multi-replica deployments across environments

## ✨ Features

- ✅ Full CRUD operations for tasks
- ✅ Health check endpoint (`/health`)
- ✅ Comprehensive error handling with HTTP status codes
- ✅ Liveness and readiness probes for Kubernetes
- ✅ Structured logging
- ✅ Environment-specific configurations (dev, staging)
- ✅ Automated testing with pytest
- ✅ GitHub Actions CI/CD pipeline
- ✅ Docker image optimization with multi-stage builds
- ✅ Resource limits and requests defined

## 🏗️ Architecture

```
gitops-task-api/
├── app/                          # Application code
│   ├── main.py                   # FastAPI application
│   ├── requirements.txt           # Python dependencies (pinned versions)
│   └── Dockerfile                # Optimized multi-stage Docker build
├── k8s/                          # Kubernetes manifests
│   ├── base/                     # Base Kustomize configuration
│   │   ├── deployment.yaml       # Deployment specification
│   │   ├── service.yaml          # Service definition
│   │   └── kustomization.yaml    # Base kustomization
│   └── overlays/                 # Environment-specific overlays
│       ├── dev/                  # Development environment
│       │   ├── kustomization.yaml
│       │   └── patches/
│       └── staging/              # Staging environment
│           ├── kustomization.yaml
│           └── patches/
├── tests/                        # Test suite
│   ├── conftest.py              # Pytest fixtures
│   ├── test_api.py              # API endpoint tests
│   └── test_health.py           # Health check tests
├── .github/
│   └── workflows/               # GitHub Actions
│       └── ci-cd.yaml           # CI/CD pipeline
├── Makefile                     # Common commands
├── .pre-commit-config.yaml      # Pre-commit hooks
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- kubectl & Kubernetes cluster (for K8s deployment)
- Kustomize 5.0+ (for GitOps)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/bosofisan/gitops-task-api.git
cd gitops-task-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r app/requirements.txt
pip install -r app/requirements-dev.txt  # For development/testing
```

4. **Run the application**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. **Visit the API**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## 📡 API Endpoints

### Health Check
```http
GET /health
```
**Response**: `{"status": "healthy"}`

### Get All Tasks
```http
GET /tasks
```
**Response**: 
```json
{
  "1": {
    "id": 1,
    "title": "Buy groceries",
    "completed": false
  }
}
```

### Get Single Task
```http
GET /tasks/{task_id}
```
**Response**: 
```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false
}
```

### Create Task
```http
POST /tasks
Content-Type: application/json

{
  "id": 1,
  "title": "Buy groceries",
  "completed": false
}
```

### Update Task
```http
PUT /tasks/{task_id}
Content-Type: application/json

{
  "id": 1,
  "title": "Buy groceries",
  "completed": true
}
```

### Delete Task
```http
DELETE /tasks/{task_id}
```
**Response**: `{"message": "Task deleted"}`

## 🛠️ Local Development

### Make Commands
```bash
make help          # Show all available commands
make install       # Install dependencies
make dev           # Run development server
make test          # Run tests
make test-cov      # Run tests with coverage
make lint          # Run linters
make format        # Auto-format code
make build         # Build Docker image
make run           # Run Docker container
make clean         # Clean up build artifacts
```

### Code Style
This project uses:
- **Black** for code formatting
- **isort** for import sorting
- **pylint** for linting
- **pytest** for testing

Run all checks:
```bash
make lint
```

## 🐳 Docker

### Build Image
```bash
docker build -t task-api:v1 ./app
```

### Run Container
```bash
docker run -p 8000:8000 task-api:v1
```

### Build with Docker Compose
```bash
docker-compose build
docker-compose up
```

## ☸️ Kubernetes Deployment

### Prerequisites
- kubectl configured to your cluster
- Docker image pushed to a registry (or available locally)

### Deploy to Kubernetes

#### Using Kustomize (Recommended)

**Dev environment:**
```bash
kubectl apply -k k8s/overlays/dev
```

**Staging environment:**
```bash
kubectl apply -k k8s/overlays/staging
```

#### Check Deployment Status
```bash
kubectl get deployments
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

#### Port Forward to Access API
```bash
kubectl port-forward svc/task-api-service 8000:8000
```

#### Health Check
```bash
kubectl get pods -w  # Watch pods (liveness/readiness probes)
```

## 🔧 GitOps with Kustomize

This project uses Kustomize for environment-specific configurations:

### Structure
```
k8s/base/                    # Common configuration
├── deployment.yaml
├── service.yaml
└── kustomization.yaml

k8s/overlays/dev/            # Dev-specific overrides
├── kustomization.yaml
└── patches/
    └── replicas.yaml

k8s/overlays/staging/        # Staging-specific overrides
├── kustomization.yaml
└── patches/
    └── replicas.yaml
```

### Generate Manifests
```bash
kustomize build k8s/overlays/dev
kustomize build k8s/overlays/staging
```

### GitOps Workflow
1. Modify manifests in `k8s/` directory
2. Commit changes to Git
3. Sync with ArgoCD or use `kubectl apply -k`
4. Changes propagate to cluster

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The `.github/workflows/ci-cd.yaml` pipeline:
- ✅ Runs tests on every push/PR
- ✅ Builds Docker image
- ✅ Pushes to Docker registry
- ✅ Generates SBOM (Software Bill of Materials)
- ✅ Security scanning with Trivy
- ✅ Semantic versioning

### Manual Trigger
```bash
git push origin feature-branch
# OR
gh workflow run ci-cd.yaml
```

### Workflow Status
View in: https://github.com/bosofisan/gitops-task-api/actions

## 🧪 Testing

### Run Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
# Report: htmlcov/index.html
```

### Run Specific Test
```bash
pytest tests/test_api.py::test_create_task -v
```

### Test Structure
```
tests/
├── conftest.py              # Pytest fixtures & configuration
├── test_api.py              # API endpoint tests
├── test_health.py           # Health check tests
└── test_error_handling.py   # Error handling tests
```

## 📊 Monitoring & Observability

### Health Checks
- **Liveness Probe**: `/health` - checks if app is responsive
- **Readiness Probe**: `/health` - checks if app is ready to serve traffic

### Logs
View container logs:
```bash
kubectl logs deployment/task-api-deployment
kubernetes logs -f deployment/task-api-deployment
```

### Metrics (Future)
The application will soon expose Prometheus metrics at `/metrics`

## 🔐 Security

### Best Practices Implemented
- ✅ Non-root user in Docker
- ✅ No hardcoded secrets (use environment variables or secrets)
- ✅ Input validation with Pydantic
- ✅ HTTPS-ready (configure reverse proxy)
- ✅ Minimal Docker image (python:3.12-slim)

### Scanning
- Docker image scanned with Trivy
- Dependencies checked for vulnerabilities
- SBOM generated in CI/CD

## 📈 Performance

### Resource Configuration
Default limits (tunable via Kustomize patches):
- **Memory Request**: 128Mi (Limit: 256Mi)
- **CPU Request**: 100m (Limit: 200m)

Adjust for your environment:
```yaml
# k8s/overlays/production/patches/resources.yaml
- op: replace
  path: /spec/template/spec/containers/0/resources
  value:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi"
      cpu: "1000m"
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Development setup
- Code style
- Testing requirements
- Commit conventions
- Pull request process

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

- **Lulu Osofisan** — DevOps Engineer
- GitHub: [@bosofisan](https://github.com/bosofisan)
- Portfolio: [Your Portfolio URL]

## 🆘 Support & Issues

- 📄 Check [existing issues](https://github.com/bosofisan/gitops-task-api/issues)
- 💬 Open a new [GitHub issue](https://github.com/bosofisan/gitops-task-api/issues/new)
- 📧 Email: boluosofisan@gmail.com
## 🗺️ Roadmap

- [ ] Add database persistence (PostgreSQL)
- [ ] Implement JWT authentication
- [ ] Add Prometheus metrics
- [ ] Deploy with ArgoCD
- [ ] Add Helm charts
- [ ] Implement request logging middleware
- [ ] Add API rate limiting
- [ ] Setup log aggregation (ELK/Loki)

---

**Star this repo** ⭐ if you find it useful for your DevOps journey!
