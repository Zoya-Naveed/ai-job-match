from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Model for a task used when reading (includes id)
class Task(BaseModel):
    id: int
    title: str
    completed: bool = False
    tag: str = "normal"

# Model for a task when creating/updating (id not required from client)
class TaskCreate(BaseModel):
    title: str
    completed: Optional[bool] = False

tasks: List[Task] = []
task_id_counter = 1

def tag_task(title: str) -> str:
    keywords_urgent = ["urgent", "immediately", "asap", "important"]
    if any(word in title.lower() for word in keywords_urgent):
        return "urgent"
    return "normal"

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate):
    global task_id_counter
    new_task = Task(
        id=task_id_counter,
        title=task.title,
        completed=task.completed or False,
        tag=tag_task(task.title)
    )
    tasks.append(new_task)
    task_id_counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks.pop(i)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: TaskCreate):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks[i].title = updated_task.title
            tasks[i].completed = updated_task.completed or False
            tasks[i].tag = tag_task(updated_task.title)
            return tasks[i]
    raise HTTPException(status_code=404, detail="Task not found")
