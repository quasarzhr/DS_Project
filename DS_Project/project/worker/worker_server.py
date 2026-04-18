from xmlrpc.server import SimpleXMLRPCServer


def execute_task(task_id, task_type, payload):
    """
    Execute a task based on its type and input payload.
    """
    print(f"Executing task {task_id} of type {task_type}")
    
    if task_type == "word_count":
        text = payload.get("text", "")
        result = {"word_count": len(text.split())}

    elif task_type == "keyword_search":
        text = payload.get("text", "")
        keyword = payload.get("keyword", "")
        count = text.split().count(keyword)
        result = {"keyword": keyword, "count": count}

    elif task_type == "sort_numbers":
        numbers = payload.get("numbers", [])
        result = {"sorted_numbers": sorted(numbers)}

    elif task_type == "prime_search":
        limit = payload.get("limit", 0)
        primes = []
        for num in range(2, limit + 1):
            is_prime = True
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        result = {"primes": primes}

    else:
        result = {"error": "Unsupported task type"}

    return result


def ping():
    """
    Return a simple response for liveness checking.
    """
    return "pong"


def get_capabilities():
    """
    Return the supported task types of this worker.

    For now, this version returns all task types.
    Later, you can refine it based on worker_id or configuration.
    """
    return [
        "word_count",
        "keyword_search",
        "sort_numbers",
        "prime_search",
    ]


def start_server(port):
    """
    Start the XML-RPC server for this worker.
    """
    server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    print(f"Worker running on {port}")

    server.register_function(execute_task, "execute_task")
    server.register_function(ping, "ping")
    server.register_function(get_capabilities, "get_capabilities")

    server.serve_forever()