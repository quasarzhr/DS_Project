from enum import Enum

# Enum for task lifecycle states
class TaskStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"

# Enum for worker availability states
class WorkerStatus(str, Enum):
    ALIVE = "ALIVE"
    BUSY = "BUSY"
    DOWN = "DOWN"