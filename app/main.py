from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Task API", version="1.0.0")

tasks = {}

class Task(BaseModel):
    id: int
    title: str
    completed: bool = False

@app.get("/")
def root():
    return {"message": "Task API is running", "version": "1.0.0"}   

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/health")
def health():
    return {"status": "healthy"}