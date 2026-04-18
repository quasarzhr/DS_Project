'''
This file defines the Pydantic schemas used for REST API request validation
and response formatting, including task creation, task status/result, and worker data.
'''

from typing import Any
from pydantic import BaseModel


class TaskCreateRequest(BaseModel):
    task_type: str
    payload: dict[str, Any]


class TaskCreateResponse(BaseModel):
    task_id: int
    status: str
    message: str

    class Config:
        from_attributes = True


class TaskStatusResponse(BaseModel):
    task_id: int
    task_type: str
    status: str
    assigned_worker_id: int | None = None
    retry_count: int = 0
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        from_attributes = True


class TaskResultResponse(BaseModel):
    task_id: int
    status: str
    result: dict[str, Any] | None = None
    message: str | None = None

    class Config:
        from_attributes = True


class WorkerResponse(BaseModel):
    worker_id: int
    address: str
    capabilities: list[str]
    status: str
    last_heartbeat: str | None = None

    class Config:
        from_attributes = True