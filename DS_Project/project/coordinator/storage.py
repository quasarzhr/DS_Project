# 未涉及

tasks = {}
task_id_counter = 1

def create_task(task_type):
    global task_id_counter
    task = {
        "id": task_id_counter,
        "type": task_type,
        "status": "PENDING",
        "result": None
    }
    tasks[task_id_counter] = task
    task_id_counter += 1
    return task

def get_task(task_id):
    return tasks.get(task_id)

def update_task(task_id, status=None, result=None):
    task = tasks.get(task_id)
    if not task:
        return None
    if status:
        task["status"] = status
    if result:
        task["result"] = result
    return task
