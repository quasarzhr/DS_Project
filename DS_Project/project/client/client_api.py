'''
封装 client 对 coordinator 的 REST 请求
不处理菜单和输入
只负责“发请求 + 收响应 + 返回结果”
给 client_cli.py 调用
'''

import requests
from typing import Any

BASE_URL = "http://127.0.0.1:8000"

# 发送 POST /tasks 请求, 提交一个新任务
def submit_task(task_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        f"{BASE_URL}/tasks",
        json={
            "task_type": task_type,
            "payload": payload,
        },
        timeout=5,
    )
    response.raise_for_status()
    return response.json()

# 发送 GET /tasks/{task_id} 请求, 查询任务当前状态
def get_task_status(task_id: int) -> dict[str, Any]:
    response = requests.get(f"{BASE_URL}/tasks/{task_id}", timeout=5)
    response.raise_for_status()
    return response.json()

# 发送 GET /tasks/{task_id}/result 请求, 查询任务最终结果
def get_task_result(task_id: int) -> dict[str, Any]:
    response = requests.get(f"{BASE_URL}/tasks/{task_id}/result", timeout=5)
    response.raise_for_status()
    return response.json()

# 发送 GET /workers 请求, 查询所有 worker 的状态
def get_workers() -> list[dict[str, Any]]:
    response = requests.get(f"{BASE_URL}/workers", timeout=5)
    response.raise_for_status()
    return response.json()

# 发送 GET /tasks 请求, 查看所有任务列表
def get_tasks() -> list[dict[str, Any]]:
    response = requests.get(f"{BASE_URL}/tasks", timeout=5)
    response.raise_for_status()
    return response.json()