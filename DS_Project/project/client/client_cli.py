# 客户端命令行入口: 用户怎么操作、结果怎么展示
# 被调用1，使用2
'''
接收用户输入
组织命令菜单
调用 client_api.py 里的 REST 请求函数
把结果以清晰的终端形式输出给用户
'''

# 整个 client_cli.py 最核心的控制函数
from typing import Any
from client.client_api import (
    submit_task,
    get_task_status,
    get_task_result,
    get_workers,
    get_tasks,
)

def main():
    '''
    启动 CLI
    显示主菜单
    循环接收用户操作
    根据用户选择调用不同功能
    直到用户选择退出
    '''
    # 涉及到要用的函数 2
    '''
    show_menu()
    get_user_choice()
    handle_submit_task()
    handle_query_task_status()
    handle_get_task_result()
    handle_list_workers()
    handle_list_tasks()
    handle_demo_requests()（如果你想在 CLI 里提供演示入口）
    print_exit_message()
    '''
    
    while True:
        show_menu()
        choice = get_user_choice()

        if choice == "1":
            handle_submit_task()
        elif choice == "2":
            handle_query_task_status()
        elif choice == "3":
            handle_get_task_result()
        elif choice == "4":
            handle_list_workers()
        elif choice == "5":
            handle_list_tasks()
        elif choice == "0":
            print("Exiting client. Goodbye.")
            break
        else:
            print("Invalid choice. Please select a valid menu option.")

# -------功能处理类---核心函数-------（未实现）

# 处理“提交任务”的完整交互流程
def handle_submit_task() -> None:
    '''
    处理用户提交任务的流程
    获取用户输入的任务类型
    调用 client_api.py 里的 submit_task() 函数发送请求
    显示提交结果（成功/失败、任务 ID 等）
    '''
    '''
    可能涉及到的函数:
    prompt_task_type() 2
    build_payload_for_task(task_type) 2
    print_submit_result(response) 2
    client_api.submit_task(task_type, payload) 1
    main() 1
    '''
    try:
        task_type = prompt_task_type()
        payload = build_payload_for_task(task_type)
        response = submit_task(task_type, payload)
        print_submit_result(response)
    except Exception as e:
        print(f"Error: {e}")

# 处理“查询任务状态”的用户交互
def handle_query_task_status() -> None:
    '''
    读取用户输入的 task_id
    调用 API 查询当前任务状态
    打印状态结果
    涉及的其他函数
    prompt_task_id() 2
    print_task_status(response) 2
    client_api.query_task_status(task_id) 1
    main() 1
    '''
    try:
        task_id = prompt_task_id()
        response = get_task_status(task_id)
        print_task_status(response)
    except Exception as e:
        print(f"Error: {e}")

# 处理“获取任务结果”的用户交互
def handle_get_task_result() -> None:
    '''
    获取用户输入的 task_id
    调用 client_api.py 里的 get_task_result() 函数发送请求
    显示任务结果（如果任务完成）或提示信息（如果任务未完成或失败）
    '''
    '''
    可能涉及到的函数:
    prompt_task_id() 2
    print_task_result(response) 2
    client_api.get_task_result(task_id) 1
    main() 1
    '''
    try:
        task_id = prompt_task_id()
        response = get_task_result(task_id)
        print_task_result(response)
    except Exception as e:
        print(f"Error: {e}")

# 处理“查看所有 worker 状态”的交互
def handle_list_workers() -> None:
    '''
    调用 client_api.py 里的 list_workers() 函数获取当前注册的 worker 列表
    打印 worker 信息（ID、状态、能力、最近 heartbeat 时间等）
    '''
    '''
    可能涉及到的函数:
    print_workers(workers_data) 2
    client_api.list_workers() 1
    main() 1
    '''
    try:
        response = get_workers()
        print_workers(response)
    except Exception as e:
        print(f"Error: {e}")

# 处理“查看所有任务”的交互
def handle_list_tasks() -> None:
    '''
    调用 client_api.py 里的 list_tasks() 函数获取当前系统中的任务列表
    打印每个任务的基本信息（ID、类型、状态等）
    task_id
    task_type
    status
    assigned_worker_id
    retry_count
    '''
    '''
    可能涉及到的函数:
    print_tasks(tasks_data) 2
    client_api.list_tasks() 1
    main() 1
    '''
    try:
        response = get_tasks()
        print_task_list(response)
    except Exception as e:
        print(f"Error: {e}")

# 可选但很有用的功能：提供一个演示入口，自动提交一些预设任务并展示结果
# 不是基础功能必须，但很适合后面录视频
def handle_demo_requests():
    '''
    这个函数可以在 CLI 里提供一个选项，自动提交一些预设任务（比如 word_count、sort_numbers 等），
    然后轮询查询它们的状态，最后展示结果。这样用户可以快速看到系统的功能和效果。
    从 CLI 里直接触发一组预设演示请求
    方便演示正常任务、混合任务、并发任务等场景
    '''
    '''
    方式一：
    直接调用：
    client_api.submit_task(...)
    方式二：
    调用脚本层或其他函数：
    demo_requests.run_demo()
    如果你后面会做 scripts/demo_requests.py
    '''
    pass

# -------菜单与输入类---辅助函数-------

# 只负责展示，不负责处理输入，打印主菜单选项
def show_menu() -> None:
    print("\n=== Distributed Job System Client ===")
    print("1. Submit a task")
    print("2. Query task status")
    print("3. Get task result")
    print("4. List workers")
    print("5. List tasks")
    print("0. Exit")

# 读取用户输入的菜单选项
def get_user_choice() -> str:
    return input("Enter your choice: ").strip()

# 让用户输入或选择任务类型，并检查是否合法
def prompt_task_type() -> str:
    supported_types = {
        "word_count",
        "keyword_search",
        "sort_numbers",
        "prime_search",
    }

    while True:
        print("\nSupported task types:")
        print("- word_count")
        print("- keyword_search")
        print("- sort_numbers")
        print("- prime_search")

        task_type = input("Enter task type: ").strip()
        if task_type in supported_types:
            return task_type

        print("Invalid task type. Please enter one of the supported task types.")

# 让用户输入任务 ID，并检查输入是否是合法整数
def prompt_task_id() -> int:
    while True:
        raw = input("Enter task ID: ").strip()
        if raw.isdigit():
            return int(raw)
        print("Invalid task ID. Please enter a positive integer.")

# 读取一组数字输入，并转换成整数列表
def prompt_numbers_input() -> list[int]:
    while True:
        raw = input("Enter numbers separated by spaces: ").strip()
        if not raw:
            print("Numbers input cannot be empty.")
            continue

        try:
            return [int(x) for x in raw.split()]
        except ValueError:
            print("Invalid input. Please enter integers only.")

# 读取 prime_search 所需的上限值
def prompt_limit_input() -> int:
    while True:
        raw = input("Enter limit: ").strip()
        if raw.isdigit() and int(raw) > 1:
            return int(raw)
        print("Invalid limit. Please enter an integer greater than 1.")

# -------数据整理类---辅助函数-------

# 根据任务类型，构建对应的payload
def build_payload_for_task(task_type: str) -> dict[str, Any]:
    if task_type == "word_count":
        text = input("Enter text: ").strip()
        while not text:
            print("Text cannot be empty.")
            text = input("Enter text: ").strip()
        return {"text": text}

    if task_type == "keyword_search":
        text = input("Enter text: ").strip()
        while not text:
            print("Text cannot be empty.")
            text = input("Enter text: ").strip()

        keyword = input("Enter keyword: ").strip()
        while not keyword:
            print("Keyword cannot be empty.")
            keyword = input("Enter keyword: ").strip()

        return {
            "text": text,
            "keyword": keyword,
        }

    if task_type == "sort_numbers":
        return {"numbers": prompt_numbers_input()}

    if task_type == "prime_search":
        return {"limit": prompt_limit_input()}

    raise ValueError(f"Unsupported task type: {task_type}")

# -------输出展示类---辅助函数-------

# 打印“任务提交成功后”的返回结果
def print_submit_result(response: dict[str, Any]) -> None:
    print("\n=== Task Submitted ===")
    print(f"Task ID: {response.get('task_id', 'N/A')}")
    print(f"Status : {response.get('status', 'N/A')}")
    if "message" in response:
        print(f"Message: {response['message']}")

# 打印任务状态查询结果
def print_task_status(response: dict[str, Any]) -> None:
    print("\n=== Task Status ===")
    print(f"Task ID          : {response.get('task_id', 'N/A')}")
    print(f"Task Type        : {response.get('task_type', 'N/A')}")
    print(f"Status           : {response.get('status', 'N/A')}")
    print(f"Assigned Worker  : {response.get('assigned_worker_id', 'N/A')}")
    print(f"Retry Count      : {response.get('retry_count', 'N/A')}")
    print(f"Created At       : {response.get('created_at', 'N/A')}")
    print(f"Updated At       : {response.get('updated_at', 'N/A')}")

# 打印任务结果查询结果
def print_task_result(response: dict[str, Any]) -> None:
    print("\n=== Task Result ===")
    print(f"Task ID: {response.get('task_id', 'N/A')}")
    print(f"Status : {response.get('status', 'N/A')}")

    if "result" in response:
        print(f"Result : {response['result']}")
    if "message" in response:
        print(f"Message: {response['message']}")

# 打印所有 worker 的信息列表
def print_workers(workers_data: list[dict[str, Any]]) -> None:
    print("\n=== Workers ===")
    if not workers_data:
        print("No workers found.")
        return

    for worker in workers_data:
        print("-" * 40)
        print(f"Worker ID      : {worker.get('worker_id', 'N/A')}")
        print(f"Address        : {worker.get('address', 'N/A')}")
        print(f"Capabilities   : {worker.get('capabilities', 'N/A')}")
        print(f"Status         : {worker.get('status', 'N/A')}")
        print(f"Last Heartbeat : {worker.get('last_heartbeat', 'N/A')}")

# 打印任务列表
def print_task_list(tasks_data: list[dict[str, Any]]) -> None:
    print("\n=== Tasks ===")
    if not tasks_data:
        print("No tasks found.")
        return

    for task in tasks_data:
        print("-" * 40)
        print(f"Task ID         : {task.get('task_id', 'N/A')}")
        print(f"Task Type       : {task.get('task_type', 'N/A')}")
        print(f"Status          : {task.get('status', 'N/A')}")
        print(f"Assigned Worker : {task.get('assigned_worker_id', 'N/A')}")
        print(f"Retry Count     : {task.get('retry_count', 'N/A')}")

if __name__ == "__main__":
    main()