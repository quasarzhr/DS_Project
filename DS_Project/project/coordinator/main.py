import uvicorn
from coordinator.api import app
from coordinator.heartbeat_monitor import start_monitor

if __name__ == "__main__":
    start_monitor()
    uvicorn.run(app, host="127.0.0.1", port=8000)