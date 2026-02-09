from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import settings, get_logger

logger = get_logger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A production-ready task management API with GitOps support"
)

tasks = {}


class Task(BaseModel):
    """Task model for request/response bodies."""
    id: int
    title: str
    completed: bool = False


@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    logger.info(
        f"Starting {settings.app_name} v{settings.app_version} "
        f"in {settings.environment.value} environment"
    )


@app.get("/")
def root():
    """Root endpoint returns API status and version."""
    logger.debug("GET / called")
    return {
        "message": f"{settings.app_name} is running",
        "version": settings.app_version,
        "environment": settings.environment.value
    }


@app.get("/health")
def health():
    """Health check endpoint for Kubernetes probes."""
    logger.debug("Health check called")
    return {"status": "healthy", "environment": settings.environment.value}


@app.get("/tasks")
def get_tasks():
    """Retrieve all tasks."""
    logger.debug(f"GET /tasks - returning {len(tasks)} tasks")
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Retrieve a single task by ID."""
    logger.debug(f"GET /tasks/{task_id}")
    if task_id not in tasks:
        logger.warning(f"Task {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]


@app.post("/tasks")
def create_task(task: Task):
    """Create a new task."""
    logger.info(f"Creating task {task.id}: {task.title}")
    if task.id in tasks:
        logger.warning(f"Task {task.id} already exists")
        raise HTTPException(status_code=409, detail="Task already exists")
    tasks[task.id] = task
    logger.info(f"Task {task.id} created successfully")
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    """Update an existing task."""
    logger.info(f"Updating task {task_id}")
    if task_id not in tasks:
        logger.warning(f"Task {task_id} not found for update")
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task
    logger.info(f"Task {task_id} updated successfully")
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by ID."""
    logger.info(f"Deleting task {task_id}")
    if task_id not in tasks:
        logger.warning(f"Task {task_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    logger.info(f"Task {task_id} deleted successfully")
    return {"message": "Task deleted"}