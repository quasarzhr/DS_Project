from datetime import datetime
from shared.enums import WorkerStatus

# In-memory worker registry used by the coordinator.
workers = [
    {
        "worker_id": 1,
        "address": "http://localhost:9001",
        "capabilities": ["word_count", "keyword_search"],
        "status": WorkerStatus.ALIVE.value,
        "last_heartbeat": None,
    },
    {
        "worker_id": 2,
        "address": "http://localhost:9002",
        "capabilities": ["sort_numbers", "prime_search"],
        "status": WorkerStatus.ALIVE.value,
        "last_heartbeat": None,
    },
    {
        "worker_id": 3,
        "address": "http://localhost:9003",
        "capabilities": [
            "word_count",
            "keyword_search",
            "sort_numbers",
            "prime_search",
        ],
        "status": WorkerStatus.ALIVE.value,
        "last_heartbeat": None,
    },
]


def get_workers():
    """
    Return the full worker list.
    """
    return workers


def get_worker_by_id(worker_id: int):
    """
    Return a worker by its ID.
    If the worker does not exist, return None.
    """
    for worker in workers:
        if worker["worker_id"] == worker_id:
            return worker
    return None


def update_heartbeat(worker_id: int):
    """
    Update the last heartbeat timestamp of a worker
    and mark it as ALIVE.
    """
    worker = get_worker_by_id(worker_id)
    if worker is None:
        return None

    worker["last_heartbeat"] = datetime.utcnow().isoformat()
    worker["status"] = WorkerStatus.ALIVE.value
    return worker


def mark_down(worker_id: int):
    """
    Mark a worker as DOWN.
    """
    worker = get_worker_by_id(worker_id)
    if worker is None:
        return None

    worker["status"] = WorkerStatus.DOWN.value
    return worker


def mark_alive(worker_id: int):
    """
    Mark a worker as ALIVE.
    """
    worker = get_worker_by_id(worker_id)
    if worker is None:
        return None

    worker["status"] = WorkerStatus.ALIVE.value
    return worker


def mark_busy(worker_id: int):
    """
    Mark a worker as BUSY.
    """
    worker = get_worker_by_id(worker_id)
    if worker is None:
        return None

    worker["status"] = WorkerStatus.BUSY.value
    return worker