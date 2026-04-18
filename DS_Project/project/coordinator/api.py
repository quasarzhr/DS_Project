from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from shared.database import SessionLocal, engine
from shared import models
from shared.schemas import (
    TaskCreateRequest,
    TaskCreateResponse,
    TaskStatusResponse,
    TaskResultResponse,
    WorkerResponse,
)
from coordinator.task_service import (
    create_task,
    get_task,
    list_tasks,
    update_task_status,
    assign_worker_to_task,
    update_task_result,
    update_task_error,
)
from coordinator.worker_registry import get_workers, update_heartbeat
from coordinator.scheduler import select_worker
from coordinator.rpc_dispatcher import dispatch_task_to_worker
from shared.enums import TaskStatus

# Create database tables if they do not already exist.
models.Base.metadata.create_all(bind=engine)

# Create the FastAPI application instance.
app = FastAPI()

# Provide a database session for each request.
def get_db():
    """
    This function opens a new SQLAlchemy session,
    yields it to the API endpoint, and ensures that
    the session is closed after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new task.
@app.post("/tasks", response_model=TaskCreateResponse)
def create_new_task(task: TaskCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new task, select a worker, dispatch the task through XML-RPC,
    and update the task state based on the execution result.
    """
    new_task = create_task(db, task.task_type, task.payload)

    workers = get_workers()
    worker = select_worker(task.task_type, workers)

    if worker is None:
        return {
            "task_id": new_task.id,
            "status": new_task.status,
            "message": "Task created but no available worker found",
        }

    assign_worker_to_task(db, new_task.id, worker["worker_id"])
    update_task_status(db, new_task.id, TaskStatus.ASSIGNED.value)

    dispatch_result = dispatch_task_to_worker(
        worker,
        new_task.id,
        task.task_type,
        task.payload,
    )

    if dispatch_result["status"] == "SUCCESS":
        update_task_result(db, new_task.id, dispatch_result["result"])
    else:
        update_task_error(db, new_task.id, dispatch_result["error"])

    updated_task = get_task(db, new_task.id)

    return {
        "task_id": updated_task.id,
        "status": updated_task.status,
        "message": "Task created",
    }

# Get the current status of a task by its ID.
@app.get("/tasks/{task_id}", response_model=TaskStatusResponse)
def read_task_status(task_id: int, db: Session = Depends(get_db)):
    """
    This endpoint looks up a task by its ID and returns
    its current status and related metadata.
    """
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task.id,
        "task_type": task.task_type,
        "status": task.status,
        "assigned_worker_id": getattr(task, "assigned_worker_id", None),
        "retry_count": getattr(task, "retry_count", 0),
        "created_at": str(getattr(task, "created_at", None)) if getattr(task, "created_at", None) else None,
        "updated_at": str(getattr(task, "updated_at", None)) if getattr(task, "updated_at", None) else None,
    }

# Get the result of a task, if it has completed.
@app.get("/tasks/{task_id}/result", response_model=TaskResultResponse)
def read_task_result(task_id: int, db: Session = Depends(get_db)):
    """
    If the task has been completed, this endpoint returns the final result.
    Otherwise, it returns the current task status and a message indicating
    that the task is not yet completed.
    """
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != "COMPLETED":
        return {
            "task_id": task.id,
            "status": task.status,
            "message": "Task not yet completed",
        }

    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result,
    }

# Get all tasks in the system.
@app.get("/tasks")
def read_all_tasks(db: Session = Depends(get_db)):
    """
    This endpoint returns a simplified list of task records
    for monitoring or inspection purposes.
    """
    tasks = list_tasks(db)
    return [
        {
            "task_id": task.id,
            "task_type": task.task_type,
            "status": task.status,
            "assigned_worker_id": getattr(task, "assigned_worker_id", None),
            "retry_count": getattr(task, "retry_count", 0),
        }
        for task in tasks
    ]

# Get all registered workers.
@app.get("/workers", response_model=list[WorkerResponse])
def read_workers():
    """
    This endpoint returns the current worker list,
    including their status, capabilities, and heartbeat data.
    """
    return get_workers()

# Receive a heartbeat from a worker and update its last heartbeat time
@app.post("/workers/{worker_id}/heartbeat")
def receive_heartbeat(worker_id: int):
    worker = update_heartbeat(worker_id)
    if worker is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    return {
        "message": f"Heartbeat received from worker {worker_id}",
        "worker_id": worker_id,
        "status": worker["status"],
        "last_heartbeat": worker["last_heartbeat"],
    }