import threading
from worker.worker_server import start_server
from worker.heartbeat_sender import send_heartbeat
import sys

worker_id = int(sys.argv[1])
port = int(sys.argv[2])

# heartbeat线程
threading.Thread(target=send_heartbeat, args=(worker_id,), daemon=True).start()

# 启动RPC
start_server(port)
