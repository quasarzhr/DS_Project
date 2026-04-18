def select_worker(task_type, workers):
    """
    Select an available worker based on task type.

    Text tasks prefer Worker 1 and fall back to Worker 3.
    Number tasks prefer Worker 2 and fall back to Worker 3.
    Only workers with ALIVE status are considered available.
    """
    preferred_order = []

    if task_type in ["word_count", "keyword_search"]:
        preferred_order = [1, 3]
    elif task_type in ["sort_numbers", "prime_search"]:
        preferred_order = [2, 3]
    else:
        return None

    for worker_id in preferred_order:
        for worker in workers:
            if (
                worker["worker_id"] == worker_id
                and worker["status"] == "ALIVE"
                and task_type in worker["capabilities"]
            ):
                return worker

    return None