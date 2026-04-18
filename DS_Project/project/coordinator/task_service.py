from sqlalchemy.orm import Session
from shared.models import Task
from shared.enums import TaskStatus

# Create a new task record in the database
def create_task(db: Session, task_type: str, payload: dict):
    """
    The task is created with the initial PENDING status
    and stores the provided task type and payload.
    """
    task = Task(
        task_type=task_type,
        payload=payload,
        status=TaskStatus.PENDING.value,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# Get a task by its ID.
def get_task(db: Session, task_id: int):
    """
    Returns the task object if found, otherwise returns None.
    """
    return db.query(Task).filter(Task.id == task_id).first()

# Get all tasks from the database
def list_tasks(db: Session):
    """
    Returns a list of task records ordered by task ID.
    """
    return db.query(Task).order_by(Task.id.asc()).all()

# Update the status of a task.
def update_task_status(db: Session, task_id: int, status: str):
    """
    Update the status of a task and return the updated task.
    """
    task = get_task(db, task_id)
    if task is None:
        return None

    task.status = status
    db.commit()
    db.refresh(task)
    return task


# Assign a worker to a task.
def assign_worker_to_task(db: Session, task_id: int, worker_id: int):
    """
    Assign a worker to a task and return the updated task.
    """
    task = get_task(db, task_id)
    if task is None:
        return None

    task.assigned_worker_id = worker_id
    db.commit()
    db.refresh(task)
    return task


# Save the final result of a task.
def update_task_result(db: Session, task_id: int, result: dict):
    """
    Store the task result, mark the task as COMPLETED,
    and return the updated task.
    """
    task = get_task(db, task_id)
    if task is None:
        return None

    task.result = result
    task.status = TaskStatus.COMPLETED.value
    db.commit()
    db.refresh(task)
    return task


# Save an error message for a task.
def update_task_error(db: Session, task_id: int, error_message: str):
    """
    Store the error message, mark the task as FAILED,
    and return the updated task.
    """
    task = get_task(db, task_id)
    if task is None:
        return None

    task.error_message = error_message
    task.status = TaskStatus.FAILED.value
    db.commit()
    db.refresh(task)
    return task