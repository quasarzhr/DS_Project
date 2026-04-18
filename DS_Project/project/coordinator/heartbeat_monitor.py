import time
import threading
from datetime import datetime, timezone

from coordinator.worker_registry import get_workers, mark_down
from shared.enums import WorkerStatus

TIMEOUT = 8  # seconds


def monitor_heartbeats():
    """
    Periodically check worker heartbeats.

    If a worker has not sent a heartbeat within the timeout threshold,
    mark it as DOWN.
    """
    while True:
        now = datetime.now(timezone.utc)

        for worker in get_workers():
            last_heartbeat = worker.get("last_heartbeat")

            if not last_heartbeat:
                continue

            try:
                last_time = datetime.fromisoformat(last_heartbeat)
                if last_time.tzinfo is None:
                    last_time = last_time.replace(tzinfo=timezone.utc)
            except ValueError:
                continue

            if (
                now - last_time
            ).total_seconds() > TIMEOUT and worker["status"] != WorkerStatus.DOWN.value:
                mark_down(worker["worker_id"])
                print(f"Worker {worker['worker_id']} marked DOWN")

        time.sleep(2)


def start_monitor():
    """
    Start the heartbeat monitor in a background daemon thread.
    """
    t = threading.Thread(target=monitor_heartbeats, daemon=True)
    t.start()