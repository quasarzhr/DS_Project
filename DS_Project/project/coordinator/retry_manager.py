MAX_RETRY = 2

def should_retry(task):
    if not hasattr(task, "retry_count"):
        task.retry_count = 0

    if task.retry_count < MAX_RETRY:
        task.retry_count += 1
        return True
    return False
