# Contributing to Task API

Thank you for your interest in contributing to Task API! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/gitops-task-api.git
   cd gitops-task-api
   ```

2. **Create a development branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r app/requirements-dev.txt
   ```

4. **Make your changes**

5. **Test your changes**
   ```bash
   pytest
   pytest --cov=app  # with coverage
   ```

6. **Format and lint code**
   ```bash
   black app/ tests/
   isort app/ tests/
   pylint app/main.py
   flake8 app/ tests/
   ```

## Development Workflow

### Branch Naming Convention

- `feature/description` — new features
- `fix/description` — bug fixes
- `docs/description` — documentation updates
- `refactor/description` — code refactoring
- `test/description` — test improvements
- `chore/description` — maintenance tasks

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add GET endpoint for single task
fix: correct validation error in task creation
docs: update API documentation
test: add unit tests for task deletion
refactor: simplify task retrieval logic
chore: update dependencies
```

Format: `type: brief description`

**Types:**
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation
- `test` — tests
- `refactor` — code refactoring
- `chore` — maintenance
- `perf` — performance
- `ci` — CI/CD changes

## Code Style Guide

### Python Code Style

- **Formatter**: Black
- **Sorting**: isort
- **Linter**: pylint
- **Type hints**: Strongly encouraged

```python
from typing import Dict, Optional
from fastapi import HTTPException

def get_task(task_id: int) -> Dict[str, any]:
    """
    Retrieve a single task by ID.
    
    Args:
        task_id: The ID of the task to retrieve.
        
    Returns:
        The task dictionary.
        
    Raises:
        HTTPException: If task not found.
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]
```

### Docstring Style

Use Google-style docstrings:

```python
def create_task(task: Task) -> Task:
    """
    Create a new task.
    
    Args:
        task: Task object to create.
        
    Returns:
        The created task.
        
    Raises:
        HTTPException: If task ID already exists.
    """
```

## Testing Requirements

- Write tests for new features
- Maintain or improve code coverage
- All tests must pass before PR merge
- Test both happy path and error cases

```python
def test_create_task(client):
    """Test successful task creation."""
    task = {"id": 1, "title": "Test", "completed": False}
    response = client.post("/tasks", json=task)
    assert response.status_code == 200
    assert response.json()["title"] == "Test"

def test_create_duplicate_task_fails(client):
    """Test duplicate task ID raises error."""
    task = {"id": 1, "title": "Test", "completed": False}
    client.post("/tasks", json=task)
    response = client.post("/tasks", json=task)
    assert response.status_code == 409
```

## Kubernetes Manifest Guidelines

When modifying K8s manifests:

1. Update base files first in `k8s/base/`
2. Add overlays in `k8s/overlays/` for environment-specific changes
3. Use Kustomize for configuration management
4. Test with: `kubectl apply -k k8s/overlays/dev --dry-run=client`

## Documentation

Update documentation when:
- Adding new features
- Changing API endpoints
- Modifying deployment procedures
- Adding environment variables

Update files:
- `README.md` — main documentation
- Inline code comments for complex logic
- Docstrings for all functions/classes

## Pull Request Process

1. **Create a pull request** with a clear title and description
2. **Link related issues**: "Fixes #123" or "Related to #456"
3. **Provide context**: Explain what and why, not just what changed
4. **Provide testing evidence**: Screenshot or test results
5. **Update documentation** if needed
6. **Self-review** your changes before requesting review

### PR Title Format
```
feat: add update endpoint for tasks
fix: correct 404 error handling
docs: improve API documentation
chore: upgrade dependencies
```

### PR Description Template
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
How to test these changes.

## Checklist
- [ ] Tests pass locally
- [ ] Code is formatted with Black/isort
- [ ] No linting errors
- [ ] Documentation is updated
- [ ] Commit messages are clear
```

## Review Process

PRs require:
- ✅ Code review approval
- ✅ All tests passing
- ✅ No merge conflicts

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation completeness
- No security issues
- Backward compatibility

## Building and Testing Docker Images

Test Docker image locally:

```bash
docker build -t task-api:test ./app
docker run -p 8000:8000 task-api:test
curl http://localhost:8000/health
```

## Kubernetes Testing

Test K8s manifests:

```bash
# Validate syntax
kubectl apply -k k8s/overlays/dev --dry-run=client

# Preview changes
kustomize build k8s/overlays/dev

# Apply (if you have a cluster)
kubectl apply -k k8s/overlays/dev
```

## Reporting Issues

### Bug Reports

Provide:
- Clear, descriptive title
- Reproduction steps
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)
- Error logs/screenshots

### Feature Requests

Include:
- Clear description
- Use case and motivation
- Proposed solution (optional)
- Alternative solutions you've considered

## CI/CD

All PRs automatically trigger:
- ✅ Unit tests
- ✅ Code linting
- ✅ Docker image build
- ✅ Security scanning

Ensure all checks pass before merge.

## Questions?

- 📧 Open a GitHub Discussion
- 💬 Comment on related issue
- 📝 Check existing documentation

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing! 🎉
