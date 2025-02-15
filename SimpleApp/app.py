import socket
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

app = FastAPI()

tasks = {}
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: str
    completed: bool = False

@app.post("/tasks/")
def create_task(task: Task):
    global task_id_counter
    task_id = task_id_counter
    tasks[task_id] = task.dict()
    task_id_counter += 1
    return {"id": task_id, **tasks[task_id]}

@app.get("/tasks/")
def get_tasks():
    return tasks

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = task.dict()
    return {"id": task_id, **tasks[task_id]}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
    return {"message": "Task deleted"}

@app.get("/ip")
def read_ip():
    return {"ip": socket.gethostbyname(socket.gethostname())}