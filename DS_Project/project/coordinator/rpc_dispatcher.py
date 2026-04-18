from xmlrpc.client import ServerProxy


def dispatch_task_to_worker(worker: dict, task_id: int, task_type: str, payload: dict):
    """
    Dispatch a task to a worker through XML-RPC.

    The worker address is taken from the worker registry.
    The RPC method execute_task(task_id, task_type, payload) is called.
    """
    try:
        server = ServerProxy(worker["address"], allow_none=True)
        result = server.execute_task(task_id, task_type, payload)
        return {"status": "SUCCESS", "result": result}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}